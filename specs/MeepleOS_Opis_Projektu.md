# Propozycja tematu pracy inżynierskiej: MeepleOS

**Autor:** Jakub Płocica  
**Kierunek:** Informatyka, studia stacjonarne I stopnia (inżynierskie), UR  
**Temat pracy:** Projekt i implementacja wieloplatformowego systemu rezerwacji, wypożyczeń i obsługi klienta z funkcjami społecznościowymi dla lokali ze strefami gier planszowych i rozrywki  
**Robocza nazwa projektu:** MeepleOS  

---

## 1. O co chodzi w projekcie?

Chcę stworzyć wieloplatformowy system dla lokali ze strefami gier planszowych (board game pubów i barcade'ów), który kompleksowo likwiduje problem niszczejących i gubiących się gier, stania w kolejce do baru oraz odwiecznego dylematu „w co dzisiaj gramy?”. Gracze mogą sami wypożyczyć grę telefonem przy stole za pomocą tagów NFC/QR (*Self-checkout*) lub tradycyjnie przy ladzie na czytniku USB barmana (obsługiwanym w przeglądarce przez WebHID API bez instalacji sterowników), a w trakcie partii zamawiać napoje kraftowe i jedzenie bezpośrednio ze smartfona prosto na kafelkowy ekran kuchenno-barowy KDS personelu z bieżącym podglądem rachunku stolika. Wprowadzam mechanizm kont cieniowych (*Zero-Friction Shadow Profiles*), dzięki któremu cała ekipa gra wspólnie od razu po wpisaniu maila bez zmuszania znajomych do instalacji apki przy planszy (punkty XP, statystyki i historia partii zbierają się w bazie i migrują po rejestracji w domu tokenem Magic Link, z zachowaniem retencji RODO). Aplikacja mobilna zawiera inteligentnego doradcę doboru gier, który analizuje wspólną historię, gust graczy i poziom trudności, chroni przed wyborem zbyt trudnego tytułu dla początkujących oraz sprawdza na żywo, czy polecana gra fizycznie leży wolna na regale lokalu. Do tego gracz otrzymuje cyfrowy Paszport Gracza z interaktywnym Kołem Mechanik BGG w SVG/D3 odkrywanym z „Fog Of War”, system poziomów XP i rang odblokowujących stałe zniżki na barze, bezpośrednie linki do wideo-zasad na YouTube, moduł fotograficznego zgłaszania braków klocków czy zalanych kart aparatem (WebP) zabezpieczający gracza przed zrzuceniem winy, dynamiczny token QR HMAC-SHA256 rotujący co minutę w 100% offline na wypadek braku NFC oraz centralny backend w .NET z kolorową mapą sali na żywo w SignalR, panelem kwarantanny i blokadą optymistyczną w PostgreSQL uniemożliwiającą dwóm osobom wypożyczenie tego samego fizycznego pudełka naraz.

> **Uwaga sprzętowa (PoC):** Tagi NFC traktuję jako prototyp demonstracyjny (naklejki NTAG213/215 naniesione na pudełka i stolik testowy). Dla osób bez modułu NFC w telefonie przygotowuję pełną alternatywę w postaci dynamicznego kodu QR zabezpieczonego podpisem HMAC-SHA256, który działa w 100% offline i rotuje co minutę.

---

## 2. Podział na moduły i architektura systemu

Projekt dzielę na cztery spójne komponenty:

```
[ Aplikacja Mobilna Gracza ]       [ Panel Bar POS & KDS ]
   (React Native + D3 SVG)             (React 19 + Vite)
             │                                 │
             ▼                                 ▼
   ┌──────────────────────────────────────────────────┐
   │        ASP.NET Core REST API & SignalR Hub       │  ◄── .NET 10 LTS / C# 14
   │     Clean Architecture • CQRS (MediatR) • JWT     │
   └─────────────────────────┬────────────────────────┘
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
   [ PostgreSQL 17/18 ]              [ Moduł Analityczny ]
 (Relacyjna baza w Dockerze)        (Mikroserwis Python / FastAPI)
```

1. **Aplikacja mobilna dla gościa lokalu (React Native + TypeScript):** Osobisty asystent gracza ze skanowaniem NFC, zamawianiem ze stolika, doradcą gier ISI, zgłaszaniem braków aparatem oraz Paszportem Gracza z Kołem Mechanik BGG w SVG/D3.
2. **Ekran personelu / Bar POS & KDS (React 19 + Vite):** Interaktywna mapa sali ze stolikami na żywo (SignalR), kafelkowy ekran zamówień KDS oraz obsługa czytnika USB przy ladzie przez WebHID API bez instalowania sterowników.
3. **Backend (.NET 10 LTS ASP.NET Core API + Docker):** Clean Architecture z CQRS (MediatR), optymistyczne blokady współbieżności i dwukierunkowe huby SignalR.
4. **Moduł analityczny i silnik rekomendacji (Python / FastAPI):** Mikroserwis analityczny zasilany bazą BoardGameGeek.

---

## 3. Pełny wykaz funkcjonalności (Co dokładnie będzie w systemie?)

### 📱 A. Aplikacja mobilna (Dla gracza / bywalca lokalu)

* **Szybki Self-checkout wypożyczenia (NFC & QR):** Zbliżenie telefonu do tagu stolika (potwierdzenie lokalizacji), a następnie do tagu na pudełku gry. System w ułamku sekundy sprawdza dostępność egzemplarza i paruje go z rachunkiem stolika.
* **Hybrydowe wypożyczenia:** Możliwość samodzielnego odbioru przy stole telefonem LUB tradycyjnie przy ladzie, gdzie barman przykłada grę do czytnika USB.
* **Konta Cieniowe (*Zero-Friction Shadow Profiles*):** Założyciel stolika dodaje znajomych, wpisując jedynie ich e-maile lub ksywki. Znajomi nie muszą instalować aplikacji ani rejestrować się przy stole – ich punkty XP i statystyki zbierają się w stanie *Shadow*, a po pobraniu aplikacji w domu cały dorobek migruje się na nowe konto jednym kliknięciem (token Magic Link).
* **Inteligentny Doradca Stolika („W co gramy?” – Moduł ISI):** Przycisk na ekranie stolika generujący spersonalizowane propozycje gier dla obecnej grupy. Analizuje wspólną historię, gust graczy, stosuje strategię kompromisu (*Average*) oraz ochrony przed zbyt trudnym tytułem (*Least Misery*) i **sprawdza na żywo fizyczną dostępność gry na półce lokalu**.
* **Cyfrowy Paszport Gracza i Koło Mechanik BGG:** Interaktywny, wektorowy wykres kołowy hierarchii mechanik gier (*Worker Placement, Deck Building itd.*) w SVG/D3. Działa na zasadzie „mgły wojny” – każda nowo zagrana partia trwale odsłania kolejne segmenty i podnosi wskaźnik eksploracji (np. *„42% Odkryte”*).
* **System Poziomów XP, Rangi i Osiągnięcia:** Punkty doświadczenia za rozegrane partie i zamówienia na barze. Rangi gracza (*Nowicjusz ➔ Amator Kostek ➔ Mistrz Strategii ➔ Arcymistrz BGG*) odblokowujące stałe zniżki na barze i odznaki.
* **Zamawianie gastronomii ze stolika (Mobile Ordering):** Przeglądanie menu lokalu (piwa kraftowe, przekąski, ciepłe dania) i składanie zamówień prosto do baru/kuchni bez stania przy ladzie.
* **Fotograficzne zgłaszanie uszkodzeń i braków (*Photo Evidence*):** Szybkie zdjęcie brakującego pionka czy uszkodzonej planszy kompresowane w telefonie (WebP) i wysyłane do obsługi – chroni gracza przed odpowiedzialnością za cudze zniszczenia.
* **Szybkie zasady i wideo-instrukcje:** Karta wypożyczonej gry zawiera bezpośredni odnośnik do oficjalnego FAQ, skrótu zasad oraz sprawdzonych poradników na YouTube.
* **Dynamiczny token QR z podpisem HMAC:** Awaryjny kod rotujący co 60 sekund z podpisem `HMAC-SHA256`, działający w 100% offline w przypadku braku modułu NFC.

---

### 🖥️ B. Ekran personelu (Bar POS & Kitchen Display System - KDS)

* **Interaktywna mapa sali na żywo (Live Floor Plan):** Graficzny rzut lokalu ze stolikami zmieniającymi kolory na żywo (🟢 *Wolny*, 🔵 *Gra w toku*, 🟡 *Partia przekracza szacowany czas*, 🔴 *Do sprzątnięcia*).
* **Kolejka zamówień gastronomicznych (KDS):** Kafelki z zamówieniami spływającymi z telefonów gości, układające się według czasu wpłynięcia ze zmianą statusu (*Nowe ➔ W przygotowaniu ➔ Wydane*).
* **Stacja barowa RFID (Natywne WebHID API):** Obsługa czytnika USB przy ladzie bezpośrednio z poziomu przeglądarki bez instalowania zewnętrznych sterowników w systemie.
* **Bramka kontroli zwrotów i kwarantanna:** Podgląd historii zgłoszonych zdjęć usterek przy zwrocie gry i opcja przesunięcia wybrakowanego egzemplarza do statusu *Kwarantanna / Do naprawy*.
* **Szczegółowy podgląd rachunku stolika:** Kliknięcie w stolik pokazuje listę obecnych graczy, wypożyczone gry, historię zamówień kuchennych oraz kwotę do rozliczenia.

---

### ⚙️ C. Panel zarządczy (Inwentaryzacja i Baza BGG)

* **Integracja z bazą BoardGameGeek (BGG Sync):** Dodawanie gier po ID z BGG – automatyczne pobieranie okładki, złożoności (*Weight*), kategorii, mechanik i sugerowanego czasu gry.
* **Zarządzanie fizycznymi egzemplarzami (*Asset Health*):** Unikalny identyfikator egzemplarza powiązany z tagiem NFC (np. `COPY-TM-01`), licznik rozegranych partii danego pudełka oraz ewidencja stanu technicznego i historii uszkodzeń.
* **Raporty popularności i utargu:** Zestawienia, które tytuły są najchętniej wypożyczane i które stoliki generują największy obrót.

---

### 🔒 D. Architektura bezpieczeństwa i współbieżność

* **Ochrona przed wyścigiem (*Race Conditions*):** Transakcje w PostgreSQL z blokadą optymistyczną (`xmin` / `RowVersion`) uniemożliwiające dwóm graczom jednoczesne wypożyczenie tego samego fizycznego pudełka.
* **Idempotencja zamówień gastronomicznych:** Klucz `idempotency_key` (UUID) generowany na telefonie zabezpieczający przed podwójnym skasowaniem zamówienia przy zerwaniu WiFi.
* **Retencja i prywatność RODO:** Automatyczne zadanie w tle (Quartz.NET) anonimizujące nieaktywowane konta cieniowe po 90 dniach.

---

### 🎲 E. Moduł funkcji społecznościowych, eventów i czatu (Social & Event Hub)

* **Organizacja i zapisy na turnieje/eventy:** Tworzenie wydarzeń społecznościowych (np. turnieje ligowe, noce premierowe) z limitem miejsc i automatyczną listą rezerwową (Waitlist) chronioną przed Overbookingiem transakcjami blokującymi w PostgreSQL.
* **Protokół meczowy i historia partii (Match History):** Rejestracja wyników zakończonych rozgrywek stolikowych i turniejowych (zwycięzcy, punktacja, czas gry) przekładająca się na naliczanie punktów doświadczenia (XP) w Paszporcie Gracza oraz pozycję w rankingach lokalu (Hall of Fame).
* **Tablica Liderów (Hall of Fame):** Rankingi graczy lokalu w kategoriach gier BGG agregowane wydajnymi widokami zmaterializowanymi w bazie danych.
* **Czat czasu rzeczywistego (WebSockets / SignalR):**
  * *Czat wydarzenia / turnieju:* Komunikacja organizatorów z uczestnikami (`event-{id}`).
  * *Czat stolika i service chat:* Wymiana wiadomości przy stole oraz szybkie prośby do personelu baru na ekran KDS (`table-{id}`).
  * *Tablica LFG (Looking For Group):* Ogłoszenia o poszukiwaniu brakujących graczy do rozpoczęcia partii przy wolnym stoliku.

---

## 4. Część badawczo-eksperymentalna

*(Szczegółowy plan badań z metrykami zaplanowany do pracy dyplomowej)*

1. **Eksperyment 1: Analiza ergonomii i czasu wypożyczenia (HCI):** Porównanie czasu rozpoczęcia gry: Self-checkout NFC przez telefon kontra tradycyjna rejestracja przy barze (seria 20 prób laboratoryjnych z analizą statystyczną).
2. **Eksperyment 2: Testy wydajnościowe backendu i SignalR (k6):** Pomiar latencji p95 i p99 przy symulacji 100 jednoczesnych połączeń WebSockets przesyłających stany sal i zamówienia.
3. **Eksperyment 3: Pojedynek modeli AI (ANFIS vs MLP – Session Overrun Predictor):** Szacowanie rzeczywistego czasu partii i paraliżu decyzyjnego graczy na bazie cech gry z oficjalnego zbioru BoardGameGeek z Kaggle (model neuro-rozmyty ANFIS kontra sztuczna sieć neuronowa MLP).
4. **Eksperyment 4: Ewaluacja strategii doboru gier w module ISI:** Porównanie strategii *Average* oraz *Least Misery* pod kątem zadowolenia grupy i sprawiedliwości rekomendacji.

---

## 5. Dostęp do danych (Zbiór BGG)

Korzystam z publicznego zbioru danych **BoardGameGeek Dataset** z Kaggle:

```json
{
  "bggId": 167791,
  "title": "Terraforming Mars",
  "minPlayers": 1,
  "maxPlayers": 5,
  "playingTimeMinutes": 120,
  "complexityWeight": 3.25,
  "ratingAverage": 8.42,
  "mechanics": ["Drafting", "Hand Management", "Tile Placement"],
  "physicalInventory": {
    "copyId": "COPY-TM-01",
    "nfcTagUid": "04:5A:21:7A:B2:10:80",
    "status": "AvailableOnShelf"
  }
}
```