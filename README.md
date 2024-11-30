## **Guida al build & deploy**
### **Prequisiti**
Assicurarsi che siano installati i seguenti elementi:
- **Docker**
- **Python** con i pacchetti:
  - grpcio
  - grpcio-tools
  - mysql-connector-python
  - yfinance
  - pybreaker (per il Circuit Breaker)    
### **Passaggi**
 ```
1. **Costruire le immagini Docker**
 Eseguire il seguente comando per costruire tutti i servizi:
 ```bash
 docker compose build
 ```
2. **Avviare l'applicazione**
 Avviare tutti i microservizi e il database:
 ```bash
 docker compose up
 ```
3. **Eseguire il client**
 Navigare nella directory del server ed eseguire lo script del client:
 ```bash
 cd server/
 python client.py
 ```
---
## **Riassunto dell'architettura**
Il sistema comprende:
- **Server**: Gestisce le interazioni con gli utenti e le operazioni del database.
- **Data collector**: Recupera periodicamente i dati sugli stocks.
- **Database**: Progettato in mySQL.

Tutti i componenti sono orchestrati utilizzando **Docker Compose** e la comunicazione tra client e server avviene tramite **gRPC**.
