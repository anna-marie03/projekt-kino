from logika import Kino
from constants import MIN_MIEJSCE, MAX_MIEJSCE


def wczytaj_niepuste(komunikat):
    while True:
        txt = input(komunikat).strip()
        if txt:
            return txt
        print("Pole nie może być puste.")


def wczytaj_email():
    while True:
        email = input("Email: ").strip()
        if not email:
            print("Email nie może być pusty.")
            continue
        if "@" not in email:
            print("Email musi zawierać znak @.")
            continue
        return email


def wczytaj_int(komunikat, min_v=None, max_v=None):
    while True:
        try:
            v = int(input(komunikat))
        except ValueError:
            print("To musi być liczba.")
            continue

        if min_v is not None and v < min_v:
            print(f"Wartość musi być >= {min_v}.")
            continue

        if max_v is not None and v > max_v:
            print(f"Wartość musi być <= {max_v}.")
            continue

        return v


def logowanie(kino):
    print("\n=== LOGOWANIE ===")
    print("1. Zaloguj jako klient")
    print("2. Zaloguj jako gość")

    while True:
        wybor = input("Wybierz opcję: ").strip()
        if wybor in ("1", "2"):
            break
        print("Wybierz 1 lub 2.")

    imie = wczytaj_niepuste("Imię: ")
    nazwisko = wczytaj_niepuste("Nazwisko: ")
    email = wczytaj_email()

    klient = kino.zaloguj_lub_utworz_klienta(imie, nazwisko, email)

    if wybor == "1":
        print(f"Zalogowano jako klient: {klient.imie} {klient.nazwisko}")
    else:
        print(f"Zalogowano jako gość: {klient.imie} {klient.nazwisko}")

    return klient


def menu_rezerwacji(klient):
    print("\n===== MENU REZERWACJI =====")
    print(f"Zalogowany: {klient.imie} {klient.nazwisko} | {klient.email}")
    print("1. Wyświetl wszystkie miejsca")
    print("2. Wyświetl dostępne miejsca")
    print("3. Zarezerwuj miejsce")
    print("4. Anuluj moją rezerwację")
    print("5. Pokaż moją historię rezerwacji")
    print("6. Wyloguj")
    print("0. Wyjście")


def main():
    kino = Kino()

    while True:
        klient = logowanie(kino)

        while True:
            menu_rezerwacji(klient)
            wybor = input("Wybierz opcję: ").strip()

            if wybor == "1":
                kino.wyswietl_wszystkie_miejsca()

            elif wybor == "2":
                kino.wyswietl_dostepne_miejsca()

            elif wybor == "3":
                numer = wczytaj_int(
                    f"Numer miejsca ({MIN_MIEJSCE}-{MAX_MIEJSCE}): ",
                    min_v=MIN_MIEJSCE,
                    max_v=MAX_MIEJSCE
                )
                kino.dokonaj_rezerwacji(klient, numer)

            elif wybor == "4":
                numer = wczytaj_int(
                    f"Numer miejsca do anulowania ({MIN_MIEJSCE}-{MAX_MIEJSCE}): ",
                    min_v=MIN_MIEJSCE,
                    max_v=MAX_MIEJSCE
                )
                kino.anuluj_rezerwacje_moje_miejsce(klient, numer)

            elif wybor == "5":
                kino.historia_klienta(klient)

            elif wybor == "6":
                print(f"Wylogowano: {klient.imie} {klient.nazwisko}")
                break

            elif wybor == "0":
                print("Do widzenia!")
                return

            else:
                print("Niepoprawna opcja.")


if __name__ == "__main__":
    main()
