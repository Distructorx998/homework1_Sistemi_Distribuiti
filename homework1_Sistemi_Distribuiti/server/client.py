import grpc
import user_pb2
import user_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = user_pb2_grpc.UserServiceStub(channel)

        while True:
            print("\nMenu:")
            print("1. Aggiungi Nuovo Utente")   
            print("2. Modifica Tiker")
            print("3. Modifica Soglie:")
            print("4. Rimuovi Utente")  
            print("5. Visualizza Ultimo Valore delle Azioni")
            print("6. Calcola Valore Medio delle Azioni ")
            print("7. Visualizza Utente ")
            print("8. Visualizza Tutti gli Utenti")            
            print("9. Esci")    
            
            choice = input("Inserisci la tua scelta: ") 


            match choice:
                case '1':
                    try:
                        email = input("Inserisci email: ")
                        ticker = input("Inserisci ticker: ")
                       
                        low_value_input = input("Inserisci soglia minima (premi invio per non specificare il valore della soglia):")
                        high_value_input = input("Inserisci soglia massima (premi invio per non specificare il valore della soglia):")

                        low_value = float(low_value_input) if low_value_input else None
                        high_value = float(high_value_input) if high_value_input else None
                        
                        # Verifica che la soglia minima non sia maggiore di quella massima
                        if low_value is not None and high_value is not None and low_value > high_value:
                            print("Errore, hai inserito un valore di soglia minima maggiore di quello di soglia massima")
                            break 
                        response = stub.RegisterUser(user_pb2.RegisterUserRequest(email=email, ticker=ticker, low_value=low_value, high_value=high_value))
                        print("Risposta RegisterUser:", response.message)
                    except grpc.RpcError as e:
                        print(f"Errore gRPC: {e.code()} - {e.details()}")

                case '2':
                    try:
                        email = input("Inserisci email: ")
                        ticker = input("Inserisci nuovo ticker: ")
                        
                        # Input per le soglie con gestione del valore di default
                        low_value_input = input("Inserisci soglia minima (premi invio per non specificare il valore della soglia):")
                        high_value_input = input("Inserisci soglia massima (premi invio per non specificare il valore della soglia):")
                        
                        # Gestione della conversione in float, impostando None se il valore è vuoto
                        low_value = float(low_value_input) if low_value_input else None
                        high_value = float(high_value_input) if high_value_input else None
                        
                        # Verifica che la soglia minima non sia maggiore di quella massima
                        if low_value is not None and high_value is not None and low_value > high_value:
                            print("Errore, hai inserito un valore di soglia minima maggiore di quello di soglia massima")
                            break
                        
                        # Chiamata al metodo gRPC per aggiornare l'utente
                        response = stub.UpdateUser(user_pb2.UpdateUserRequest(email=email, ticker=ticker, low_value=low_value, high_value=high_value))
                        print("Risposta UpdateUser:", response.message)
                    
                    except grpc.RpcError as e:
                        print(f"Errore gRPC: {e.code()} - {e.details()}")


                case '3':
                    try:
                        email = input("Inserisci email: ")
                        risposta1= input( "Vuoi Eliminare [y] o Aggiornare [n] la soglia minima? Premere qualsiasi altro tasto per passare all'high_value.")
                        if risposta1== 'y':
                            response = stub.RemoveThreshold(user_pb2.RemoveThresholdRequest(email=email, low_value=0))
                        elif risposta1== 'n':
                            low_value_input = input("Inserisci soglia minima (premi invio per non specificare il valore della soglia):")
                        
                        risposta2= input( "Vuoi Eliminare [y] o Aggiornare [n] la soglia massima?")
                        if risposta2== 'y':
                            response = stub.RemoveThreshold(user_pb2.RemoveThresholdRequest(email=email, high_value=0))
                        elif risposta2== 'n':
                            high_value_input = input("Inserisci soglia massima (premi invio per non specificare il valore della soglia):")
                    
                                        
                        # Input per le soglie con gestione del valore di default
                        
                        # Gestione della conversione in float, impostando None se il valore è vuoto
                        low_value = float(low_value_input) if low_value_input else None
                        high_value = float(high_value_input) if high_value_input else None
                        
                        # Verifica che la soglia minima non sia maggiore di quella massima
                        if low_value is not None and high_value is not None and low_value > high_value:
                            print("Errore, hai inserito un valore di soglia minima maggiore di quello di soglia massima")
                            break
                        
                        # Chiamata al metodo gRPC per aggiornare l'utente
                        response = stub.UpdateThreshold(user_pb2.UpdateThresholdRequest(email=email, low_value=low_value, high_value=high_value))
                        print("Risposta UpdateThreshold:", response.message)
                    
                    except grpc.RpcError as e:
                        print(f"Errore gRPC: {e.code()} - {e.details()}")



                case '4':
                    try:
                        email = input("Inserisci email: ")
                        response = stub.DeleteUser(user_pb2.DeleteUserRequest(email=email))
                        print("Risposta DeleteUser:", response.message)
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

                case '8':
                    try:
                        print("Richiesta di tutti i dati al server in corso...")
                        response = stub.GetAllData(user_pb2.Empty())
                        print("Risposta Tutti Gli Utenti:")
                        if not response.data:
                            print("Nessun dato trovato.")
                        else:
                            for data in response.data:
                                print(data)
                    except grpc.RpcError as e:
                        print(f"Errore gRPC: {e.code()} - {e.details()}")


                    
                
                
                case '9':
                    print("Uscita in corso...")
                    break

                case _:
                    print("Inserisci un nuemro da 1 a 7.")

if __name__ == "__main__":
    run()
