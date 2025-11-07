import os
from datetime import datetime


#KLASY

class Pokoj:
    def __init__(self, numerPokoju, pojemnosc, cenaDoba):
        self.__numerPokoju = numerPokoju.strip()
        self.__pojemnosc = int(pojemnosc)
        self.__cenaDoba = float(cenaDoba)

    def __repr__(self):
        return f"Pokój {self.__numerPokoju} ({self.__pojemnosc} os., {self.__cenaDoba} zł/doba)"

    def getNumer(self):
        return self.__numerPokoju

    def getCena(self):
        return self.__cenaDoba

    def getPojemnosc(self):
        return self.__pojemnosc


class Klient:
    def __init__(self, id, imie, nazwisko, numerTelefonu):
        self.__id = id.strip()
        self.__imie = imie.strip()
        self.__nazwisko = nazwisko.strip()
        self.__numerTelefonu = numerTelefonu.strip()

    def __repr__(self):
        return f"{self.__imie} {self.__nazwisko} (ID: {self.__id})"

    def getId(self):
        return self.__id

    def getNumerTelefonu(self):
        return self.__numerTelefonu

    def getDane(self):
        return self.__id, self.__imie, self.__nazwisko, self.__numerTelefonu


class Rezerwacja:
    def __init__(self, id, idKlienta, numerPokoju, dataOd, dataDo):
        self.__id = id.strip()
        self.__idKlienta = idKlienta.strip()
        self.__numerPokoju = numerPokoju.strip()
        self.__dataOd = dataOd.strip()
        self.__dataDo = dataDo.strip()

    def __repr__(self):
        return f"Rezerwacja {self.__id}: klient {self.__idKlienta}, pokój {self.__numerPokoju}, {self.__dataOd} - {self.__dataDo}"

    def getId(self):
        return self.__id

    def getNumerPokoju(self):
        return self.__numerPokoju

    def getIdKlienta(self):
        return self.__idKlienta

    def getOkres(self):
        return self.__dataOd, self.__dataDo

    def getDane(self):
        return self.__id, self.__idKlienta, self.__numerPokoju, self.__dataOd, self.__dataDo


class Admin:
    def __init__(self, id, imie, nazwisko, haslo):
        self.__id = id.strip()
        self.__imie = imie.strip()
        self.__nazwisko = nazwisko.strip()
        self.__haslo = haslo.strip()

    def getId(self):
        return self.__id

    def getHaslo(self):
        return self.__haslo

    def __repr__(self):
        return f"Admin {self.__imie} {self.__nazwisko} (ID: {self.__id})"


#PENSJONAT

class Pensjonat:
    def __init__(self):
        self.__pokoje = []
        self.__klienci = []
        self.__rezerwacje = []
        self.__admini = []

    # ---- Wczytywanie danych ----
    def odczytajPokoje(self, nazwaPliku):
        if not os.path.exists(nazwaPliku):
            with open(nazwaPliku, 'w', encoding='utf-8') as f:
                f.write("101;2;150\n102;4;250\n103;1;100\n")
        with open(nazwaPliku, encoding='utf-8') as f:
            for linia in f:
                numerPokoju, pojemnosc, cenaDoba = linia.strip().split(';')
                self.__pokoje.append(Pokoj(numerPokoju, pojemnosc, cenaDoba))

    def odczytajKlientow(self, nazwaPliku):
        if not os.path.exists(nazwaPliku):
            with open(nazwaPliku, 'w', encoding='utf-8') as f:
                f.write("1;Jan;Kowalski;123456789\n2;Anna;Nowak;987654321\n")
        with open(nazwaPliku, encoding='utf-8') as f:
            for linia in f:
                id, imie, nazwisko, tel = linia.strip().split(';')
                self.__klienci.append(Klient(id, imie, nazwisko, tel))

    def odczytajRezerwacje(self, nazwaPliku):
        if not os.path.exists(nazwaPliku):
            open(nazwaPliku, 'w', encoding='utf-8').close()
        with open(nazwaPliku, encoding='utf-8') as f:
            for linia in f:
                if not linia.strip():
                    continue
                id, idK, pok, od, do = linia.strip().split(';')
                self.__rezerwacje.append(Rezerwacja(id, idK, pok, od, do))

    def odczytajAdminow(self, nazwaPliku):
        if not os.path.exists(nazwaPliku):
            with open(nazwaPliku, 'w', encoding='utf-8') as f:
                f.write("1;Adam;Nowak;admin123\n2;Ewa;Kowalczyk;haslo2025\n")
        with open(nazwaPliku, encoding='utf-8') as f:
            for linia in f:
                id, imie, nazwisko, haslo = linia.strip().split(';')
                self.__admini.append(Admin(id, imie, nazwisko, haslo))

    # ---- Zapis danych ----
    def zapiszKlientow(self, plik="klienci.txt"):
        with open(plik, 'w', encoding='utf-8') as f:
            for k in self.__klienci:
                id, imie, nazw, tel = k.getDane()
                f.write(f"{id};{imie};{nazw};{tel}\n")

    def zapiszRezerwacje(self, plik="rezerwacje.txt"):
        with open(plik, 'w', encoding='utf-8') as f:
            for r in self.__rezerwacje:
                id, idK, pok, od, do = r.getDane()
                f.write(f"{id};{idK};{pok};{od};{do}\n")

    # ---- Logika ----
    def znajdzKlienta(self, idLubTel):
        for k in self.__klienci:
            if k.getId() == idLubTel or k.getNumerTelefonu() == idLubTel:
                return k
        return None

    def znajdzAdmina(self, id, haslo):
        for a in self.__admini:
            if a.getId() == id and a.getHaslo() == haslo:
                return a
        return None

    def wolnePokoje(self, dataOd, dataDo):
        dataOd = datetime.strptime(dataOd, "%Y-%m-%d")
        dataDo = datetime.strptime(dataDo, "%Y-%m-%d")
        zajete = set()
        for r in self.__rezerwacje:
            od, do = r.getOkres()
            od = datetime.strptime(od, "%Y-%m-%d")
            do = datetime.strptime(do, "%Y-%m-%d")
            if not (dataDo <= od or dataOd >= do):
                zajete.add(r.getNumerPokoju())
        return [p for p in self.__pokoje if p.getNumer() not in zajete]

    def rezerwacjeKlienta(self, idKlienta):
        return [r for r in self.__rezerwacje if r.getIdKlienta() == idKlienta]

    def dodajRezerwacje(self, idKlienta, numerPokoju, dataOd, dataDo):
        idNowe = str(len(self.__rezerwacje) + 1)
        self.__rezerwacje.append(Rezerwacja(idNowe, idKlienta, numerPokoju, dataOd, dataDo))
        self.zapiszRezerwacje()
        print("✅ Rezerwacja dodana i zapisana w pliku.")

    def usunRezerwacje(self, idRezerwacji):
        self.__rezerwacje = [r for r in self.__rezerwacje if r.getId() != idRezerwacji]
        self.zapiszRezerwacje()
        print("✅ Rezerwacja usunięta i zapis zaktualizowany.")

    def dodajKlienta(self, id, imie, nazwisko, telefon):
        self.__klienci.append(Klient(id, imie, nazwisko, telefon))
        self.zapiszKlientow()
        print("✅ Klient dodany i zapisany do pliku.")

    def usunKlienta(self, id):
        self.__klienci = [k for k in self.__klienci if k.getId() != id]
        self.__rezerwacje = [r for r in self.__rezerwacje if r.getIdKlienta() != id]
        self.zapiszKlientow()
        self.zapiszRezerwacje()
        print("✅ Klient i jego rezerwacje usunięte z plików.")


# =================== MENU ===================

def menu_klient(pensjonat, klient):
    while True:
        print(f"\n👤 Witaj, {klient}!")
        print("1. Pokaż wolne pokoje")
        print("2. Zrób rezerwację")
        print("3. Moje rezerwacje")
        print("0. Wyloguj")
        wybor = input("> ")

        if wybor == "1":
            od = input("Data od (YYYY-MM-DD): ")
            do = input("Data do (YYYY-MM-DD): ")
            wolne = pensjonat.wolnePokoje(od, do)
            if not wolne:
                print("Brak wolnych pokoi w tym terminie.")
            for p in wolne:
                print(p)
        elif wybor == "2":
            od = input("Data od (YYYY-MM-DD): ")
            do = input("Data do (YYYY-MM-DD): ")
            wolne = pensjonat.wolnePokoje(od, do)
            for p in wolne:
                print(p)
            nr = input("Numer pokoju do rezerwacji: ")
            pensjonat.dodajRezerwacje(klient.getId(), nr, od, do)
        elif wybor == "3":
            for r in pensjonat.rezerwacjeKlienta(klient.getId()):
                print(r)
        elif wybor == "0":
            break


def menu_admin(pensjonat):
    while True:
        print("\n🛠️ PANEL ADMINA")
        print("1. Usuń klienta")
        print("2. Dodaj klienta")
        print("3. Usuń rezerwację")
        print("4. Pokaż wszystko")
        print("0. Wyloguj")
        wybor = input("> ")

        if wybor == "1":
            id = input("Podaj ID klienta: ")
            pensjonat.usunKlienta(id)
        elif wybor == "2":
            id = input("ID: ")
            imie = input("Imię: ")
            nazwisko = input("Nazwisko: ")
            tel = input("Telefon: ")
            pensjonat.dodajKlienta(id, imie, nazwisko, tel)
        elif wybor == "3":
            idr = input("Podaj ID rezerwacji do usunięcia: ")
            pensjonat.usunRezerwacje(idr)
        elif wybor == "4":
            pensjonat.wypiszKlientow()
            pensjonat.wypiszPokoje()
            pensjonat.wypiszRezerwacje()
        elif wybor == "0":
            break


# =================== GŁÓWNY PROGRAM ===================

def main():
    pensjonat = Pensjonat()
    pensjonat.odczytajPokoje("pokoje.txt")
    pensjonat.odczytajKlientow("klienci.txt")
    pensjonat.odczytajRezerwacje("rezerwacje.txt")
    pensjonat.odczytajAdminow("admini.txt")

    while True:
        print("\n==== 🏨 PENSJONAT ====")
        print("1. Logowanie klienta")
        print("2. Logowanie admina")
        print("0. Wyjście")
        wybor = input("> ")

        if wybor == "1":
            dane = input("Podaj ID lub numer telefonu: ")
            klient = pensjonat.znajdzKlienta(dane)
            if klient:
                menu_klient(pensjonat, klient)
            else:
                print("Nie znaleziono klienta.")
        elif wybor == "2":
            id_admina = input("Podaj ID admina: ")
            haslo = input("Podaj hasło: ")
            admin = pensjonat.znajdzAdmina(id_admina, haslo)
            if admin:
                menu_admin(pensjonat)
            else:
                print("Błędne dane logowania.")
        elif wybor == "0":
            print("👋 Do zobaczenia!")
            break


main()
