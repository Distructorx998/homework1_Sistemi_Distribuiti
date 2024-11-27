import grpc
import user_pb2
import user_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = user_pb2_grpc.UserServiceStub(channel)

        while True:
            print("\nMenu:")
            print("1. Aggiungi Nuovo Utente")   
            print("2. Modifica Informazioni Utente")    
            print("3. Rimuovi Utente")  
            print("4. Visualizza Tutti i Dati") 
            print("5. Visualizza Ultimo Valore delle Azioni")
            print("6. Calcola Valore Medio delle Azioni ")
            print("7. Esci")    
            
            choice = input("Inserisci la tua scelta: ") 


            match choice:
                case '1':
                    try:
                        email = input("Inserisci email: ")
                        ticker = input("Inserisci ticker: ")
                        response = stub.RegisterUser(user_pb2.RegisterUserRequest(email=email, ticker=ticker))
                        print("Risposta RegisterUser:", response.message)
                    except grpc.RpcError as e:
                        print(f"Errore gRPC: {e.code()} - {e.details()}")

                case '2':
                    try:
                        email = input("Inserisci email: ")
                        ticker = input("Inserisci nuovo ticker: ")
                        response = stub.UpdateUser(user_pb2.UpdateUserRequest(email=email, ticker=ticker))
                        print("Risposta UpdateUser:", response.message)
                    except grpc.RpcError as e:
                        print(f"Errore gRPC: {e.code()} - {e.details()}")

                case '3':
                    try:
                        email = input("Inserisci email: ")
                        response = stub.DeleteUser(user_pb2.DeleteUserRequest(email=email))
                        print("Risposta DeleteUser:", response.message)
                    except grpc.RpcError as e:
                        print(f"Errore gRPC: {e.code()} - {e.details()}")

                case '4':
                    try:
                        response = stub.GetAllData(user_pb2.Empty())
                        print("Risposta AllData:")
                        for data in response.data:
                            print(data)
                    except grpc.RpcError as e:
                        print(f"Errore gRPC: {e.code()} - {e.details()}")

                case '5':
                    try:
                        email = input("Inserisci l'email: ")
                        response = stub.GetLastStockValue(user_pb2.EmailRequest(email=email))
                        print("Risposta LastStockValue:", response.message, "Valore:", response.value)
                    except grpc.RpcError as e:
                        print(f"Errore gRPC: {e.code()} - {e.details()}")

                case '6':
                    try:
                        email = input("Inserisci email: ")
                        count = int(input("Inserisci il numero di valori per la media: "))
                        response = stub.GetAverageStockValue(user_pb2.AverageStockRequest(email=email, count=count))
                        print("Risposta AverageStockValue:", response.message, "Valore:", response.value)
                    except grpc.RpcError as e:
                        print(f"Errore gRPC: {e.code()} - {e.details()}")

                case '7':
                    print("Uscita in corso...")
                    break

                case _:
                    print("Inserisci un nuemro da 1 a 7.")

if __name__ == "__main__":
    run()
