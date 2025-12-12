from constants import CENA_ZWYKLE, CENA_VIP, CENA_NIEPELNOSPRAWNI


class MiejsceWKinie:
    def __init__(self, numer, cena, dostepne=True):
        self.numer = numer
        self.cena = cena
        self.dostepne = dostepne

    def opisz(self):
        status = "dostępne" if self.dostepne else "zajęte"
        return f"Miejsce {self.numer} | cena: {self.cena} zł | {status}"

    def zarezerwuj(self):
        self.dostepne = False

    def anuluj_rezerwacje(self):
        self.dostepne = True


class MiejsceZwykle(MiejsceWKinie):
    def __init__(self, numer):
        super().__init__(numer, CENA_ZWYKLE)

    def opisz(self):
        return "[ZWYKŁE] " + super().opisz()


class MiejsceVIP(MiejsceWKinie):
    def __init__(self, numer):
        super().__init__(numer, CENA_VIP)

    def opisz(self):
        return "[VIP] " + super().opisz()


class MiejsceDlaNiepelnosprawnych(MiejsceWKinie):
    def __init__(self, numer):
        super().__init__(numer, CENA_NIEPELNOSPRAWNI)

    def opisz(self):
        return "[NIEPEŁNOSPRAWNI] " + super().opisz()


class Rezerwacja:
    def __init__(self, id_rezerwacji, klient_id, numer_miejsca, cena_koncowa, aktywna=True):
        self.id_rezerwacji = id_rezerwacji
        self.klient_id = klient_id
        self.numer_miejsca = numer_miejsca
        self.cena_koncowa = cena_koncowa
        self.aktywna = aktywna

    def anuluj(self):
        self.aktywna = False


class Klient:
    def __init__(self, id_klienta, imie, nazwisko, email=""):
        self.id_klienta = id_klienta
        self.imie = imie
        self.nazwisko = nazwisko
        self.email = email
        self.historia_rezerwacji = []  # lista ID rezerwacji

    def dodaj_rezerwacje(self, id_rez):
        self.historia_rezerwacji.append(id_rez)
