from fastapi import FastAPI
import uvicorn
# from terminal.bank_communication.card_reader import read_card


# Dodaj tutaj logikę nasłuchiwania na przesyłaną kwotę od kasy na porcie innym niż 8000
# Po przesłaniu danych odpal tu metodę read_card(value)
# Operujemy na groszach, więc wszystkie wartości najlepiej tak przechowuj, będziemy je zamieniać na zł na wyświetlaczu

app = FastAPI()

@app.post("/cart/pay")
def pay(money: int) -> bool:
    print(f"Terminal received {money} amount of money")
    # return read_card(value=money)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)