from concurrent import futures
import grpc
import user_pb2
import user_pb2_grpc
import mysql.connector
import logging

def normalize_email(email):
    local, domain = email.lower().split('@')
    
    if domain in ['gmail.com', 'googlemail.com']:
        local = local.replace('.', '')
        local = local.split('+')[0]
        
    return f"{local}@{domain}"




class UserService(user_pb2_grpc.UserServiceServicer):

    def __init__(self):
        self.conn = mysql.connector.connect(
            host="db",
            user="user",
            password="password",
            database="users"
        )
        self.requestRegister = {}
        self.requestUpdate = {}
        self.requestDelete = {}
        self.create_table()
        logging.basicConfig(level=logging.INFO)

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                          (email VARCHAR(255) PRIMARY KEY, ticker VARCHAR(255))''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS stock_prices
                          (id INT AUTO_INCREMENT PRIMARY KEY, email VARCHAR(255), ticker VARCHAR(255), price FLOAT, timestamp TIMESTAMP, FOREIGN KEY (email) REFERENCES users(email))''')
        cursor.close()

    def RegisterUser(self, request, context):
        normalized_email = normalize_email(request.email)
        try:
            if normalized_email in self.requestRegister:
                if self.requestRegister[normalized_email] == 0:
                    return user_pb2.RegisterUserResponse(message="Registration in process...")
                elif self.requestRegister[normalized_email] == 1:
                    return user_pb2.RegisterUserResponse(message="User already registered successfully")

            self.requestRegister[normalized_email] = 0
            cursor = self.conn.cursor()
            try:
                cursor.execute("INSERT INTO users (email, ticker) VALUES (%s, %s)", 
                               (normalized_email, request.ticker))
                self.conn.commit()
                self.requestRegister[normalized_email] = 1
                if normalized_email in self.requestDelete:
                    self.requestDelete.pop(normalized_email, None)
                logging.info(f"User {normalized_email} registered successfully.")
                return user_pb2.RegisterUserResponse(message="User registered successfully")
            except mysql.connector.Error as db_err:
                self.conn.rollback()
                self.requestRegister.pop(normalized_email, None) 
                logging.error(f"Database error: {db_err}")
                return user_pb2.RegisterUserResponse(message="An error occurred during registration.")
            finally:
                cursor.close()
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return user_pb2.RegisterUserResponse(message="An unexpected error occurred.")

    def UpdateUser(self, request, context):
        normalized_email = normalize_email(request.email)
        key = (normalized_email, request.ticker)  

        try:
            if key in self.requestUpdate:
             if self.requestUpdate[key] == 0:
                return user_pb2.UpdateUserResponse(message="Update in process...")
             elif self.requestUpdate[key] == 1:
                return user_pb2.UpdateUserResponse(message="User already updated successfully")

            keys_to_delete = [k for k in self.requestUpdate if k[0] == normalized_email]
            for k in keys_to_delete:
                del self.requestUpdate[k]

            self.requestUpdate[key] = 0

            cursor = self.conn.cursor()
            try:
                cursor.execute("UPDATE users SET ticker = %s WHERE email = %s",
                               (request.ticker, normalized_email))
                self.conn.commit()
                self.requestUpdate[key] = 1
                return user_pb2.UpdateUserResponse(message="User updated successfully")
            except mysql.connector.Error as db_err:
                self.conn.rollback()
                logging.error(f"Database error: {db_err}")
                return user_pb2.UpdateUserResponse(message="An error occurred during update.")
            finally:
                cursor.close()
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return user_pb2.UpdateUserResponse(message="An unexpected error occurred.")


    def DeleteUser(self, request, context):
        normalized_email = normalize_email(request.email)
        try:
            if normalized_email in self.requestDelete:
                if self.requestDelete[normalized_email] == 0:
                    return user_pb2.DeleteUserResponse(message="Deletion in process...")
                elif self.requestDelete[normalized_email] == 1:
                    return user_pb2.DeleteUserResponse(message="User already deleted successfully")

            self.requestDelete[normalized_email] = 0

            cursor = self.conn.cursor()
            try:
                cursor.execute("DELETE FROM users WHERE email = %s", (normalized_email,))
                self.conn.commit()
                self.requestDelete[normalized_email] = 1
                if normalized_email in self.requestRegister:
                    self.requestRegister.pop(normalized_email,None)
                return user_pb2.DeleteUserResponse(message="User deleted successfully")
            except mysql.connector.Error as db_err:
                self.conn.rollback()
                self.requestDelete.pop(normalized_email,None) 
                logging.error(f"Database error: {db_err}")
                return user_pb2.DeleteUserResponse(message="An error occurred during deletion. ") 
            finally:
                cursor.close()
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return user_pb2.DeleteUserResponse(message="An unexpected error occurred.")


    def GetAllData(self, request, context):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED") 
            tables = cursor.fetchall()
            data = []
            for table in tables:
                cursor.execute(f"SELECT * FROM {table[0]}")
                rows = cursor.fetchall()
                data.append(f"Table: {table[0]}")
                for row in rows:
                    data.append(str(row))
            return user_pb2.AllDataResponse(data=data)
        except mysql.connector.Error as db_err:
            logging.error(f"Database error: {db_err}")
            return user_pb2.AllDataResponse(data=["An error occurred while retrieving data."])
        finally:
            cursor.close()

    def GetLastStockValue(self, request, context):
        normalized_email = normalize_email(request.email)
        cursor = self.conn.cursor()
        try:
            cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED") 
            cursor.execute("SELECT price FROM stock_prices WHERE email = %s ORDER BY timestamp DESC LIMIT 1", (normalized_email,))
            result = cursor.fetchone()
            if result:
                return user_pb2.StockValueResponse(message="Last stock value retrieved successfully", value=result[0])
            else:
                return user_pb2.StockValueResponse(message="No stock value found for the given email", value=0.0)
        except mysql.connector.Error as db_err:
            logging.error(f"Database error: {db_err}")
            return user_pb2.StockValueResponse(message="An error occurred while retrieving the last stock value.", value=0.0)
        finally:
            cursor.close()


    def GetAverageStockValue(self, request, context):
        normalized_email = normalize_email(request.email)
        cursor = self.conn.cursor()
        try:
            cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED") 
            cursor.execute("SELECT ticker FROM users WHERE email = %s", (normalized_email,))
            user_ticker = cursor.fetchone()
            
            if user_ticker:
                cursor.execute("SELECT price FROM stock_prices WHERE email = %s AND ticker = %s ORDER BY timestamp DESC LIMIT %s", 
                            (normalized_email, user_ticker[0], request.count))
                results = cursor.fetchall()
                if results:
                    average_value = sum([r[0] for r in results]) / len(results)
                    return user_pb2.StockValueResponse(message="Average stock value calculated successfully", value=average_value)
                else:
                    return user_pb2.StockValueResponse(message="No stock values found for the given email and ticker", value=0.0)
            else:
                return user_pb2.StockValueResponse(message="No ticker found for the given email", value=0.0)
        except mysql.connector.Error as db_err:
            logging.error(f"Database error: {db_err}")
            return user_pb2.StockValueResponse(message="An error occurred while calculating the average stock value.", value=0.0)
        finally:
            cursor.close()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
    
if __name__ == '__main__':
    serve()