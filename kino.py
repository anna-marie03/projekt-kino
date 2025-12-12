from modele import Klient
from logika import Kino


# ============ LOGOWANIE / TWORZENIE KLIENTA ============

def logowanie_klienta(kino: Kino) -> Klient:
    while True:
        print("\n=== Logowanie Klienta ===")
        try:
            id_klienta = int(input("Podaj ID klienta: "))
        except ValueError:
            print("Niepoprawny ID.")
            continue

        imie = input("Podaj imię: ").strip()
        nazwisko = input("Podaj nazwisko: ").strip()
        email = input("Podaj email: ").strip()

        klient = kino.znajdz_klienta(id_klienta)

        if klient:
            if (
                klient.imie == imie
                and klient.nazwisko == nazwisko
                and klient.email == email
            ):
                print("Zalogowano pomyślnie.\n")
                return klient
            else:
                print("Dane niezgodne z istniejącym klientem.")
        else:
            nowy = Klient(id_klienta, imie, nazwisko, email)
            kino.dodaj_klienta(nowy)
            print("Utworzono nowego klienta i zalogowano.\n")
            return nowy


def klient_do_rezerwacji_jako_gosc(kino: Kino) -> Klient:
    print("\n=== Rezerwacja jako niezalogowany klient ===")
    return logowanie_klienta(kino)


# ============ MENU ============

def wyswietl_menu(aktualny_klient: Klient | None):
    print("\n===== SYSTEM REZERWACJI KINA =====")

    if aktualny_klient:
        print(f"(Zalogowany: {aktualny_klient.imie} {aktualny_klient.nazwisko} | ID: {aktualny_klient.id_klienta})")
    else:
        print("(Brak zalogowanego klienta – możesz rezerwować jako gość)")

    print("1. Zaloguj klienta")
    print("2. Wyświetl wszystkie miejsca")
    print("3. Dokonaj rezerwacji")
    print("4. Anuluj rezerwację")
    print("5. Historia rezerwacji klienta")
    print("6. Zapis do pliku TXT")
    print("7. Wyloguj")
    print("0. Wyjście")


def main():
    kino = Kino()
    aktualny_klient: Klient | None = None

    while True:
        wyswietl_menu(aktualny_klient)
        wybor = input("Wybierz opcję: ")

        # ---- logowanie ----

        if wybor == "1":
            aktualny_klient = logowanie_klienta(kino)

        # ---- miejsca ----

        elif wybor == "2":
            kino.wyswietl_dostepne_miejsca()

        # ---- rezerwacja ----

        elif wybor == "3":
            try:
                numer = int(input("Podaj numer miejsca: "))
            except ValueError:
                print("Niepoprawny numer!")
                continue

            if aktualny_klient:
                id_kl = aktualny_klient.id_klienta
            else:
                gosc = klient_do_rezerwacji_jako_gosc(kino)
                id_kl = gosc.id_klienta

            kino.dokonaj_rezerwacji(id_kl, numer)

        # ---- anulowanie ----

        elif wybor == "4":
            try:
                id_rez = int(input("Podaj ID rezerwacji: "))
            except ValueError:
                print("Niepoprawne ID.")
                continue

            kino.anuluj_rezerwacje(id_rez)

        # ---- historia ----

        elif wybor == "5":
            try:
                id_klienta = int(input("Podaj ID klienta: "))
            except ValueError:
                print("Niepoprawne ID.")
                continue

            kino.wyswietl_historie_klienta(id_klienta)

        # ---- zapis ----

        elif wybor == "6":
            kino.zapisz_dane()

        # ---- wylogowanie ----

        elif wybor == "7":
            if aktualny_klient is None:
                print("Nikt nie jest zalogowany.")
            else:
                print(f"Wylogowano: {aktualny_klient.imie} {aktualny_klient.nazwisko}")
                aktualny_klient = None

        # ---- wyjście ----

        elif wybor == "0":
            print("Do widzenia!")
            break

        else:
            print("Niepoprawna opcja.")

if __name__ == "__main__":
    main()