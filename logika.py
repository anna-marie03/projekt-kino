import os

from modele import (
    MiejsceZwykle,
    MiejsceVIP,
    MiejsceDlaNiepelnosprawnych,
    Klient,
    Rezerwacja,
)

#tutaj zaczyna się tworzenie miejsc
class Kino:
    def __init__(self):
        self.miejsca = {}
        self.klienci = {}
        self.rezerwacje = {}
        self._kolejny_id_rezerwacji = 1

        self._zainicjalizuj_miejsca()

    # ------------------ Inicjalizacja miejsc ------------------

    def _zainicjalizuj_miejsca(self):
        for i in range(1, 21):
            self.miejsca[i] = MiejsceZwykle(i)
        for i in range(21, 26):
            self.miejsca[i] = MiejsceVIP(i)
        for i in range(26, 31):
            self.miejsca[i] = MiejsceDlaNiepelnosprawnych(i)

    # ------------------ Operacje podstawowe ------------------

    def wyswietl_dostepne_miejsca(self):
        print("\n--- LISTA MIEJSC ---")
        for m in self.miejsca.values():
            print(m.opisz())

    def znajdz_miejsce(self, numer):
        return self.miejsca.get(numer)

    def dodaj_klienta(self, klient: Klient):
        self.klienci[klient.id_klienta] = klient

    def znajdz_klienta(self, id_klienta):
        return self.klienci.get(id_klienta)

    def _next_rezerwacja_id(self):
        rid = self._kolejny_id_rezerwacji
        self._kolejny_id_rezerwacji += 1
        return rid

    # ------------------ REZERWACJE ------------------

    def dokonaj_rezerwacji(self, id_klienta, numer_miejsca):
        klient = self.znajdz_klienta(id_klienta)
        miejsce = self.znajdz_miejsce(numer_miejsca)

        if klient is None:
            print("Klient nie istnieje!")
            return None

        if miejsce is None:
            print("Nie ma takiego miejsca!")
            return None

        if not miejsce.dostepne:
            print("To miejsce jest zajęte!")
            return None

        miejsce.zarezerwuj()
        id_rez = self._next_rezerwacja_id()

        rez = Rezerwacja(
            id_rezerwacji=id_rez,
            klient_id=id_klienta,
            numer_miejsca=numer_miejsca,
            cena_koncowa=miejsce.cena,
            aktywna=True,
        )

        self.rezerwacje[id_rez] = rez
        klient.dodaj_rezerwacje(id_rez)

        print(f"Rezerwacja udana! ID: {id_rez}")

        # AUTOMATYCZNY ZAPIS PO REZERWACJI
        self.zapisz_dane()

        return id_rez

    def anuluj_rezerwacje(self, id_rezerwacji):
        rez = self.rezerwacje.get(id_rezerwacji)

        if rez is None:
            print("Brak takiej rezerwacji.")
            return

        if not rez.aktywna:
            print("Ta rezerwacja już jest anulowana.")
            return

        miejsce = self.miejsca.get(rez.numer_miejsca)
        if miejsce:
            miejsce.anuluj_rezerwacje()

        rez.anuluj()
        print("Rezerwacja została anulowana.")

        # AUTOMATYCZNY ZAPIS PO ANULOWANIU
        self.zapisz_dane()

    def wyswietl_historie_klienta(self, id_klienta):
        klient = self.znajdz_klienta(id_klienta)

        if klient is None:
            print("Nie znaleziono klienta.")
            return

        print(f"\nHistoria rezerwacji dla: {klient.imie} {klient.nazwisko}")

        if not klient.historia_rezerwacji:
            print("Brak rezerwacji.")
            return

        for id_rez in klient.historia_rezerwacji:
            rez = self.rezerwacje.get(id_rez)
            if rez is None:
                continue
            status = "AKTYWNA" if rez.aktywna else "ANULOWANA"
            print(
                f"ID: {rez.id_rezerwacji} | miejsce: {rez.numer_miejsca} "
                f"| cena: {rez.cena_koncowa} zł | {status}"
            )

    # ------------------ ZAPIS DO PLIKU TXT ------------------

    def zapisz_dane(self):
        """
        Plik ma mieć format:

        zarezerwowano|id_rez|id_klienta|imie|nazwisko|email|numer_miejsca|cena
        anulowano|id_rez|id_klienta|imie|nazwisko|email|numer_miejsca|cena

        Dla każdej rezerwacji:
        - linia 'zarezerwowano'
        - JEŚLI jest anulowana'
        """

        sciezka = os.path.join(os.getcwd(), "rezerwacje.txt")

        with open(sciezka, "w", encoding="utf-8") as f:
            for rez in self.rezerwacje.values():
                klient = self.klienci.get(rez.klient_id)
                if klient is None:
                    continue

                # Zawsze linia zarezerwowano
                f.write(
                    f"zarezerwowano|"
                    f"{rez.id_rezerwacji}|{klient.id_klienta}|"
                    f"{klient.imie}|{klient.nazwisko}|{klient.email}|"
                    f"{rez.numer_miejsca}|{rez.cena_koncowa}\n"
                )

                # Jeśli anulowana → dopisz linię anulowano
                if not rez.aktywna:
                    f.write(
                        f"anulowano|"
                        f"{rez.id_rezerwacji}|{klient.id_klienta}|"
                        f"{klient.imie}|{klient.nazwisko}|{klient.email}|"
                        f"{rez.numer_miejsca}|{rez.cena_koncowa}\n"
                    )

        print("Zapisano dane do pliku rezerwacje.txt.")
