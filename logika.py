import os
from modele import (
    MiejsceZwykle,
    MiejsceVIP,
    MiejsceDlaNiepelnosprawnych,
    Rezerwacja,
    Klient,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REZERWACJE_PLIK = os.path.join(BASE_DIR, "rezerwacje.txt")
REZERWACJE_BACKUP = os.path.join(BASE_DIR, "rezerwacje_backup.txt")


class Kino:
    def __init__(self):
        self.miejsca = {}      # numer_miejsca -> Miejsce
        self.klienci = {}      # id_klienta -> Klient
        self.rezerwacje = {}   # id_rezerwacji -> Rezerwacja

        self._kolejny_id_rezerwacji = 1
        self._kolejny_id_klienta = 1

        self._zainicjalizuj_miejsca()
        self.wczytaj_dane()

    # ------------------ MIEJSCA ------------------

    def _zainicjalizuj_miejsca(self):
        for i in range(1, 21):
            self.miejsca[i] = MiejsceZwykle(i)
        for i in range(21, 26):
            self.miejsca[i] = MiejsceVIP(i)
        for i in range(26, 31):
            self.miejsca[i] = MiejsceDlaNiepelnosprawnych(i)

    def wyswietl_wszystkie_miejsca(self):
        print("\n--- WSZYSTKIE MIEJSCA ---")
        for m in self.miejsca.values():
            print(m.pokaz_informacje_o_miejscu())

    def wyswietl_dostepne_miejsca(self):
        print("\n--- DOSTĘPNE MIEJSCA ---")
        znaleziono = False
        for m in self.miejsca.values():
            if m.dostepne:
                print(m.pokaz_informacje_o_miejscu())
                znaleziono = True
        if not znaleziono:
            print("Brak dostępnych miejsc.")

    # ------------------ KLIENCI ------------------

    def znajdz_klienta_po_emailu(self, email):
        email = email.strip().lower()
        for k in self.klienci.values():
            if k.email.lower() == email:
                return k
        return None

    def zaloguj_lub_utworz_klienta(self, imie, nazwisko, email):
        istnieje = self.znajdz_klienta_po_emailu(email)
        if istnieje:
            return istnieje

        klient = Klient(self._kolejny_id_klienta, imie, nazwisko, email)
        self.klienci[klient.id_klienta] = klient
        self._kolejny_id_klienta += 1
        return klient

    # ------------------ REZERWACJE ------------------

    def dokonaj_rezerwacji(self, klient, numer_miejsca):
        miejsce = self.miejsca.get(numer_miejsca)

        if miejsce is None:
            print("Nie ma takiego miejsca.")
            return None

        if not miejsce.dostepne:
            print("To miejsce jest już zajęte.")
            return None

        miejsce.zarezerwuj()

        id_rez = self._kolejny_id_rezerwacji
        self._kolejny_id_rezerwacji += 1

        rez = Rezerwacja(
            id_rezerwacji=id_rez,
            klient_id=klient.id_klienta,
            numer_miejsca=numer_miejsca,
            cena_koncowa=miejsce.cena,
            aktywna=True
        )

        self.rezerwacje[id_rez] = rez
        klient.dodaj_rezerwacje(id_rez)

        print(f"Zarezerwowano miejsce {numer_miejsca} (ID rezerwacji: {id_rez})")
        self.zapisz_dane()
        return id_rez

    def anuluj_rezerwacje_moje_miejsce(self, klient, numer_miejsca):
        for id_rez in klient.historia_rezerwacji:
            rez = self.rezerwacje.get(id_rez)
            if rez and rez.aktywna and rez.numer_miejsca == numer_miejsca:
                rez.anuluj()

                miejsce = self.miejsca.get(numer_miejsca)
                if miejsce:
                    miejsce.anuluj_rezerwacje()

                print(f"Anulowano rezerwację miejsca {numer_miejsca} (ID rezerwacji: {id_rez})")
                self.zapisz_dane()
                return True

        print("Nie masz aktywnej rezerwacji na to miejsce.")
        return False

    # ------------------ HISTORIA ------------------

    def historia_klienta(self, klient):
        print("\n--- TWOJA HISTORIA REZERWACJI ---")

        if not klient.historia_rezerwacji:
            print("Brak rezerwacji.")
            return

        for id_rez in klient.historia_rezerwacji:
            rez = self.rezerwacje.get(id_rez)
            if rez is None:
                continue

            status_txt = "zarezerwowano" if rez.aktywna else "anulowano"
            print(
                f"{klient.imie} | {klient.nazwisko} | {klient.email} | "
                f"Miejsce: {rez.numer_miejsca} | Cena: {rez.cena_koncowa} zł | Status: {status_txt}"
            )

    # ------------------ ZAPIS / ODCZYT ------------------

    def zapisz_dane(self):
        """
        Format:
        status|id_klienta|imie|nazwisko|email|id_rezerwacji|numer_miejsca|cena
        """
        linie = []
        for rez in self.rezerwacje.values():
            klient = self.klienci.get(rez.klient_id)
            if klient is None:
                continue

            status_txt = "zarezerwowano" if rez.aktywna else "anulowano"
            linie.append(
                f"{status_txt}|{klient.id_klienta}|{klient.imie}|{klient.nazwisko}|{klient.email}|"
                f"{rez.id_rezerwacji}|{rez.numer_miejsca}|{rez.cena_koncowa}\n"
            )

        with open(REZERWACJE_PLIK, "w", encoding="utf-8") as f:
            f.writelines(linie)

        with open(REZERWACJE_BACKUP, "w", encoding="utf-8") as f:
            f.writelines(linie)

    def wczytaj_dane(self):
        # jeśli brak rezerwacje.txt -> wczytaj backup
        sciezka = REZERWACJE_PLIK if os.path.exists(REZERWACJE_PLIK) else REZERWACJE_BACKUP
        if not os.path.exists(sciezka):
            return

        with open(sciezka, "r", encoding="utf-8") as f:
            for linia in f:
                linia = linia.strip()
                if not linia:
                    continue

                czesci = linia.split("|")

                # STARY FORMAT (7 pól): bez ceny
                if len(czesci) == 7:
                    status_txt, id_kl, imie, nazwisko, email, id_rez, numer_miejsca = czesci
                    cena = None

                # NOWY FORMAT (8 pól): z ceną
                elif len(czesci) == 8:
                    status_txt, id_kl, imie, nazwisko, email, id_rez, numer_miejsca, cena = czesci
                else:
                    # linia uszkodzona
                    continue

                try:
                    id_kl = int(id_kl)
                    id_rez = int(id_rez)
                    numer_miejsca = int(numer_miejsca)
                except ValueError:
                    continue

                # pomijamy rezerwacje na nieistniejące miejsca
                if numer_miejsca not in self.miejsca:
                    continue

                aktywna = (status_txt == "zarezerwowano")


                if cena is None:
                    cena_float = self.miejsca[numer_miejsca].cena
                else:
                    try:
                        cena_float = float(cena)
                    except ValueError:
                        cena_float = self.miejsca[numer_miejsca].cena

                # klient
                if id_kl not in self.klienci:
                    self.klienci[id_kl] = Klient(id_kl, imie, nazwisko, email)
                self._kolejny_id_klienta = max(self._kolejny_id_klienta, id_kl + 1)

                # rezerwacja
                rez = Rezerwacja(
                    id_rezerwacji=id_rez,
                    klient_id=id_kl,
                    numer_miejsca=numer_miejsca,
                    cena_koncowa=cena_float,
                    aktywna=aktywna
                )
                self.rezerwacje[id_rez] = rez
                self.klienci[id_kl].dodaj_rezerwacje(id_rez)

                # stan miejsca
                if aktywna:
                    self.miejsca[numer_miejsca].zarezerwuj()
                else:
                    self.miejsca[numer_miejsca].anuluj_rezerwacje()

                # liczniki
                self._kolejny_id_rezerwacji = max(self._kolejny_id_rezerwacji, id_rez + 1)
