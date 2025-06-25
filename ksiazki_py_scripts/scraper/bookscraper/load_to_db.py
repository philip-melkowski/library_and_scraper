import json
import requests
import os

# === KONFIGURACJA ===
BASE_URL = "http://localhost:8080/api"
LOGIN = "admin"
HASLO = "admin"
BOOKS_FILE = os.path.join(os.path.dirname(__file__), "jsonl/books.jsonl")
AUTH = (LOGIN, HASLO)
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# === SZUKAJ AUTORA ===
def znajdz_autora(imie, nazwisko):
    res = requests.get(f"{BASE_URL}/autorzy/szukajByImieNazwisko",
                       params={"imie": imie, "nazwisko": nazwisko},
                       auth=AUTH, headers=HEADERS)
    if res.status_code == 200:
        return res.json()
    return None

# === DODAJ AUTORA ===
def dodaj_autora(imie, nazwisko):
    payload = {"imie": imie, "nazwisko": nazwisko}
    res = requests.post(f"{BASE_URL}/autorzy",
                        json=payload, auth=AUTH, headers=HEADERS)

    if res.status_code == 201:
        return res.json()
    elif res.status_code == 409:
        print(f"⚠️ Autor już istnieje: {imie} {nazwisko}")
        return znajdz_autora(imie, nazwisko)

    print(f"❌ Nie udało się dodać autora: {imie} {nazwisko}")
    print(f"   → Kod HTTP: {res.status_code}")
    print(f"   → Treść odpowiedzi: {res.text}")
    return None

# === DODAJ KSIĄŻKĘ ===
def dodaj_ksiazke(tytul, autor_id):
    payload = {
        "tytul": tytul,
        "autor": {
            "id": autor_id
        }
    }
    res = requests.post(f"{BASE_URL}/ksiazki",
                        json=payload, auth=AUTH, headers=HEADERS)
    if res.status_code == 201:
        print(f"✅ Dodano książkę: {tytul}")
    else:
        print(f"❌ Błąd przy dodawaniu książki: {tytul}")
        print(f"   → Kod: {res.status_code}")
        print(f"   → Odpowiedź: {res.text}")

# === GŁÓWNA FUNKCJA ===
def main():
    if not os.path.exists(BOOKS_FILE):
        print("⚠️ Plik books.jsonl nie istnieje.")
        return

    with open(BOOKS_FILE, "r", encoding="utf-8") as file:
        for line in file:
            book = json.loads(line.strip())
            imie = book["autorImie"]
            nazwisko = book["autorNazwisko"]
            tytul = book["tytul"]

            autor = znajdz_autora(imie, nazwisko)
            if not autor:
                autor = dodaj_autora(imie, nazwisko)
            print(f"🧪 Autor dodany/zwrócony: {autor}")
            if autor:
                dodaj_ksiazke(tytul, autor["id"])

if __name__ == "__main__":
    main()