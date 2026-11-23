# Funkcjonalności w projekcie MeepleOS

**Autor:** Jakub Płocica  
**Temat pracy:** Projekt i implementacja wieloplatformowego systemu rezerwacji, wypożyczeń i obsługi klienta z funkcjami społecznościowymi dla lokali ze strefami gier planszowych i rozrywki  
**Łączna liczba funkcjonalności:** 109  

---

## Podsumowanie MoSCoW

| Priorytet MoSCoW | Liczba funkcji |
|---|:---:|
| **Must Have** | 61 |
| **Should Have** | 37 |
| **Could Have** | 11 |
| **RAZEM** | **109** |

---


## 1. Autoryzacja i sesje

| ID & Nazwa | [AUTH-01] Rejestracja |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej |
| **Co robi** | Użytkownik podaje: mail,  hasło, pseudonim, data urodzenia, imię, nazwisko, numer telefonu. Backend tworzy konto i odsyła tokeny JWT. |
| **Kluczowe mechanizmy** | Hashowanie haseł używając BCrypt, walidacja unikalności e-maila w PostgreSQL, ochrona przed botami (Rate Limiting).|
| **Wstępny MoSCoW** | **Must have** – bez konta nie ma identyfikacji gracza. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [AUTH-02] Weryfikacja adresu e-mail |
|---|---|
| **Kto i gdzie** | Użytkownik wpisuje kod z maila w aplikacje mobilną |
| **Co robi** | Użytkownik po poprawnym zarejestrowaniu otrzymuje na skrzynkę pocztową kod weryfikacyjny do wpisania w aplikacji. |
| **Kluczowe mechanizmy** | Wszytsko odbywa się w izolowanej technologii MailTrap, wiadomość z kodem zostaje wysłana na podaną przez użytkownika skrzynkę pocztową. Kod zostaje dodany do bazy danych PostgreSQL i weryfikowany z podanym w aplikacji przez użytkownika |
| **Wstępny MoSCoW** | **Should Have** - Aplikacja jest w stanie funkcjonować bez weryfikacji natomiast jest to proste do implementacji|

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [AUTH-03] Logowanie standardowe |
|---|---|
| **Kto i gdzie** | Użytkownik w apliakacji mobilnej |
| **Co robi** | Użytkownik loguje się podanym przy rejestracji adresem e-mail/loginem oraz hasłem. Ma możliwość opcji niewylogowywania. Przy poprawnym wprowadzeniu danych użytkownik zostaje zalogowany na dashboard |
| **Kluczowe mechanizmy** | Credentiale zostaną wysłane do sprawdzenia z danymi w bazie PostgreSQL, BCrypt weryfikuje poprawność wprowadzonego hasła do zahashowanej wersji z bazy danych. Limit 5 błędnych prób (blokada brute-force). Jeśli użytkownik zaznaczy opcje "zapamiętaj mnie" do bazy zostanie wysłany Refresh Token na okres 30 dni. Po porpawnym zalogowaniu do Storage Memory zostaje przesłany token JWT na okres 60 minut|
| **Wstępny MoSCoW** | **Must Have** - bez logowania nie będzie aplikacji |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [AUTH-04] Logowanie alternatywne |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej |
| **Co robi** | Użytkownik podczas rejestracji/logowania ma możliwośc zalogowania się używająć konta google/apple  |
| **Kluczowe mechanizmy** | Cała weryfikacja przebiega przy użyciu OAuth |
| **Wstępny MoSCoW** | **Could Have** - jest to fajny smaczek, natomiast zwykłe logowanie/rejestracja wystarczy |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [AUTH-05] Odzyskiwanie hasła |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej |
| **Co robi** | Użytkownik przy kliknięciu w przycisk "Odzyskaj hasło" podaje adres e-mail na który zostanie wysłany kod autoryzacyjny zmiany hasła do wpisania w aplikacji. Kod ten zostanie także wysłany do bazy danych i po wpisaniu przez użytkownika porównane ze sobą. |
| **Kluczowe mechanizmy** | Mail zostanie wysłany przez MailTrap z kodem który zostanie dodany do bazy PostgreSQL, następnie po wprowadzeniu go przez użytkownika zwalidowany z istniejącym w bazie danych. Limit 5 błędnych prób (blokada brute-force) oraz TTL = 3 minuty. Po poprawnym wyniku użytkownik ma możliwość podania nowego hasła |
| **Wstępny MoSCoW** | **Must Have** - standard, łatwe do implementacji |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [AUTH-06] Wylogowanie |
|---|---|
| **Kto i gdzie** | Użytkownik w apliakcji mobilnej |
| **Co robi** | Zalogowany użytkownik ma możliwość wylogowania się, co skutkuje skasowaniem Tokenu JWT oraz Refresh Token |
| **Kluczowe mechanizmy** | Wylogowanie kasuje z Storage Memory Token JWT oraz Refresh Token z bazy danych |
| **Wstępny MoSCoW** | **Must Have** - bez wylogowania obsługa aplikacji będzie ciężka |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [AUTH-07] Automatyczne odświeżanie sesji |
|---|---|
| **Kto i gdzie** | Aplikacja sama w sobie |
| **Co robi** | Aplikacja w tle monitoruje czas życia tokena JWT. Gdy zbliża się do wygaśnięcia (<10 min), automatycznie wysyła Refresh Token do backendu i pobiera nowy JWT bez wylogowywania gracza i bez przerywania rozgrywki. |
| **Kluczowe mechanizmy** | Interceptor HTTP w aplikacji mobilnej (Axios/Fetch), endpoint /api/auth/refresh w ASP.NET Core, technika Refresh Token Rotation w PostgreSQL (zabezpieczenie przed kradzieżą tokena). |
| **Wstępny MoSCoW** | **Must Have** - warto mieć, nie będzie tak cześto problemu z unautorized |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [AUTH-08] Weryfikacja użytkownika przy POS |
|---|---|
| **Kto i gdzie** | Użytkownik przy ladzie podaje swoje dane które wprowadza/skanuje pracownik baru |
| **Co robi** | Użytkownik przy ladzie podaje adres e-mail/login/imie i nazwisko/numer telefonu LUB kod QR wygenerowany w zalogowanym koncie pracownik baru jest w stanie zweryfikować użytkownika |
| **Kluczowe mechanizmy** | pracownik na barze skanuje/wprowadza dane użytkownika, baza danych oddaje jego wszystkie dane. |
| **Wstępny MoSCoW** | **Must Have** - jedno z głównych funkcjonalnośći aplikacji|

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [AUTH-09] Shadow Account |
|---|---|
| **Kto i gdzie** | Użytkownik przy ladzie lub host w tworzeniu grupy |
| **Co robi** | Użytkownik przy ladzie podaje maila na który przyjdzie link do utworzenia konta. Wszystkie dane i tak zosają wysłane do bazy danych|
| **Kluczowe mechanizmy** | Użytkownik lub host "tworzą" konto widmo które zbiera dane i wysyla je do bazy danych. Hangfire po 30 dniach kasuje dane jeśli konto nie zostanie utworzone |
| **Wstępny MoSCoW** | **Must Have** - trzeba dodać, bo nie każdy chce sie bawić od razu w zakładanie konta |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [AUTH-10] Role i uprawnienia |
|---|---|
| **Kto i gdzie** | System sam określa jaki user sie loguje |
| **Co robi** | System pilnuje, żeby zwykły gracz ze swojego telefonu nie mógł wejść do panelu barmana, nie mógł anulować cudzego rachunku ani zmienić statusu gry na "Kwarantanna". |
| **Kluczowe mechanizmy** | Role zaszyte w tokenie JWT (tzw. Claims), atrybut [Authorize(Roles = "Staff,Manager")] w ASP.NET Core na endpointach API |
| **Wstępny MoSCoW** | **Must Have** - bez tego sytem jest dziurawy jak sito |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [AUTH-11] Usunięcie konta |
|---|---|
| **Kto i gdzie** | Użytkownik w opcjach może usunąć swoje konto lub administrator |
| **Co robi** | Użytkownik klika "Usuń konto". System anonimizuje jego dane (mail zamienia na deleted_user_5@anon.local, usuwa imię, nazwisko, telefon), ale zachowuje zanonimizowaną historię partii dla statystyk lokalu. |
| **Kluczowe mechanizmy** | Soft Delete, twarda anonimizacja danych osobowych, unieważnienie wszystkich tokenów w bazie. |
| **Wstępny MoSCoW** | **Should Have** - bez tego sytem da rade działać, ale warto mieć |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [AUTH-12] Blokada konta użytkownika |
|---|---|
| **Kto i gdzie** | Manager / Administrator w panelu webowym |
| **Co robi** | Nałożenie czasowej lub stałej blokady na konto gracza za wandalizm gier, ucieczkę bez płacenia rachunku lub agresywne zachowanie. Zablokowany użytkownik nie może otworzyć sesji ani złożyć rezerwacji. |
| **Kluczowe mechanizmy** | Flaga `IsBanned`, unieważnienie aktywnych tokenów JWT i blokada autoryzacji w API. |
| **Wstępny MoSCoW** | **Must Have** – ochrona lokalu przed toksykami |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

## 2. Profil i bezpieczeństwo konta

| ID & Nazwa | [PROF-01] Podgląd i edycja profilu |
|---|---|
| **Kto i gdzie** | Użytkownik w informacjach o koncie lub administrator |
| **Co robi** | Użytkownik przechodzi w aplikacji moblinej do zakładki "Twoje Konto" gdzie ma wszystkie swoje informacje oraz możliwośc ich edycji |
| **Kluczowe mechanizmy** | Pobieranie danych z bazy PostgrSQL i edycja PATCHem |
| **Wstępny MoSCoW** | **Must Have** - warto dodawać edycje |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [PROF-02] Zmiana hasła |
|---|---|
| **Kto i gdzie** | Użytkownik w opcjch konta lub administrator |
| **Co robi** | Użytkownik klika "Zmień hasło", wyskakuje mu popup z wpisaniem starego oraz nowego hasła, jeśli dane sie zgadzają, hasło zostaje zmienione |
| **Kluczowe mechanizmy** | Walidator sprawdza czy podane hasło jest poprawne, jeśli tak zmienia je w bazie danych |
| **Wstępny MoSCoW** | **Must Have** - standard |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [PROF-03] Zmiana adresu e-mail |
|---|---|
| **Kto i gdzie** | Użytkownik w opcjach konta lub administrator |
| **Co robi** | Użytkownik klika "Zmień adres e-mail" wyskakuje popup z wpisaniem nowego adresu. Na podany adres przychodzi wiadomosć MailTrapem z kodem do wpisania w aplikacji, dodaje się on także do bazy. Jeśli dane sie zgadzają, adres zostaje zmieniony |
| **Kluczowe mechanizmy** | MailTrap wysyła mail na nową skrzynkę pocztową, do bazy dodajemy ten sam kod co w mailu i sprawdzamy ich poprawnośc po wpisaniu przez użytkownika |
| **Wstępny MoSCoW** | **Should Have** - bez tego sytem da rade działać, ale warto mieć |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [PROF-04] Podgląd aktywnych sesji i wylogowanie z innych urządzeń |
|---|---|
| **Kto i gdzie** | Użytkownik w informacjach konta lub administrator |
| **Co robi** | Użytkownik klika "Wyświetl zalogowane urządzenia". System wyświetla na jakich urządzeniach i o której ostatnio był zalogowany użytkownik, ma tu możliwośc wylogowania sie z wybranych sesji |
| **Kluczowe mechanizmy** | Tabela sesji powiązana z Refresh Tokenami, odczyt nazwy urządzenia i IP z nagłówka User-Agent, unieważnianie tokena w bazie (IsRevoked = true) skutkujące wylogowaniem urządzenia przy kolejnym odpytaniu API. |
| **Wstępny MoSCoW** | **Could Have** - fajny smaczek, zwiększa bezpieczeństwo ale nie jest wymagane w takiej aplikacji |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [PROF-05] Dynamiczny kod QR gracza w profilu |
|---|---|
| **Kto i gdzie** | Użytkownik w głównej stronie aplikacji (coś jak w aplikacji Żappka) |
| **Co robi** | Użytkownik klika w zakładkę "Mój kod QR", po czym może pokazać ją do zeskanowania bariście w celu zweryfikowania konta |
| **Kluczowe mechanizmy** | Generowanie kodu QR w 100% offline z podpisem kryptograficznym HMAC-SHA256 i timestampem ważności (TTL = 60 sekund), biblioteka react-native-qrcode-svg, weryfikacja podpisu i czasu na backendzie (odporność na screenshoty). |
| **Wstępny MoSCoW** | **Must Have** - jedna z głównych funkcjonalności |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [PROF-06] Eksport danych konta i historii partii |
|---|---|
| **Kto i gdzie** | Użytkownik w informacjach konta ma zakładkę historia |
| **Co robi** | Użytkownik klika „Pobierz moje dane” i dostaje wygenerowany plik .json z całą swoją historią partii, ocenami gier i zamówieniami, który może zapisać w telefonie. |
| **Kluczowe mechanizmy** | Serializacja danych użytkownika z PostgreSQL do formatu JSON/ZIP w ASP.NET Core, pobranie pliku na telefon. |
| **Wstępny MoSCoW** | **Should Have** - bez tego sytem da rade działać, ale warto mieć |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [PROF-07] Lista zaufanych współgraczy |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej |
| **Co robi** | Możliwość dodawania stałych znajomych do listy przyjaciół. Przy otwieraniu sesji stolika host może jednym kliknięciem dodać całą swoją stałą „ekipę planszówkową” zamiast wpisywać każdego z osobna. |
| **Kluczowe mechanizmy** | Relacja `UserFriends` oraz `PlayerSquads` w bazie danych PostgreSQL. |
| **Wstępny MoSCoW** | **Should Have** – podnosi ergonomię korzystania z aplikacji. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

## 3. Stoliki i sesje grupowe

| ID & Nazwa | [TAB-01] Otwarcie sesji stolika przez NFC |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej |
| **Co robi** | Użytkownik z otwartą aplikacją przykłada telefon do naklejki NFC na stoliku, a ta paruje go z tym stolikiem i tworzy nową sesję (użytkownik staje się Hostem). |
| **Kluczowe mechanizmy** | Naklejka NFC przechowuje tylko numer stolika (TableId). Backend w ASP.NET Core sprawdza w PostgreSQL czy stolik jest wolny i tworzy sesję w bazie. |
| **Wstępny MoSCoW** | **Must Have** - Jedna z ważniejszych funkcjonalności |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [TAB-02] Alternatywne zajęcie stolika (Skan QR / Kod PIN stolika) |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej |
| **Co robi** | Działa tak samo jak wersja z NFC, ale dla telefonów bez NFC. Użytkownik skanuje kod QR aparatem lub wpisuje 4-cyfrowy kod z naklejki na stoliku. |
| **Kluczowe mechanizmy** | Wysłanie TableId lub PINu do backendu i weryfikacja w bazie czy stolik jest wolny. |
| **Wstępny MoSCoW** | **Must Have** - Jedna z ważniejszych funkcjonalności |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [TAB-03] Dołączanie graczy do otwartej sesji stolika |
|---|---|
| **Kto i gdzie** | Użytkownik-Host w aplikacji lub zalogowani Użytkownicy którzy chcą dołączyć |
| **Co robi** | Host może zaprosić znajomych po mailu, numerze telefonu lub pseudonimie. Zalogowani użytkownicy mogą też sami dołączyć skanując ten sam stolik lub wpisując kod sesji. |
| **Kluczowe mechanizmy** | Dodanie ID użytkownika do trwającej sesji w tabeli powiązań w PostgreSQL. |
| **Wstępny MoSCoW** | **Must Have** - Jedna z głównych funkcjonalności |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [TAB-04] Dodanie Shadow Profile do sesji przez Hosta |
|---|---|
| **Kto i gdzie** | Użytkownik-Host w widoku sesji |
| **Co robi** | Host może dodać do stolika znajomego bez konta, wpisując sam jego e-mail. Kumpel zbiera punkty do odebrania w domu. |
| **Kluczowe mechanizmy** | Utworzenie rekordu Shadow User w bazie i powiązanie go z obecną sesją stolika. |
| **Wstępny MoSCoW** | **Must Have** - Fajny smaczek, łatwo zrobić |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [TAB-05] Synchronizacja stanu stolika na żywo (SignalR) |
|---|---|
| **Kto i gdzie** | Wszyscy użytkownicy przy danym stoliku w aplikacji mobilnej |
| **Co robi** | Wszystko co dzieje się przy stole (nowy gracz, wypożyczona gra, zamówienie z baru) od razu wyświetla się u każdego na ekranie bez odświeżania. |
| **Kluczowe mechanizmy** | SignalR wysyła eventy przez WebSockets do wszystkich podłączonych do tego stolika, apka mobilna od razu aktualizuje widok. |
| **Wstępny MoSCoW** | **Must Have** - bez tego aplikacja nie ma sensu w grupie |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [TAB-06] Przekazanie roli Hosta lub opuszczenie sesji przez gracza |
|---|---|
| **Kto i gdzie** | Użytkownik w widoku sesji |
| **Co robi** | Host może przekazać rolę hosta innemu zalogowanemu graczowi. Każdy gracz może w dowolnym momencie opuścić sesję, a jego dotychczasowe punkty i zamówienia zostają zapisane. |
| **Kluczowe mechanizmy** | Zmiana roli usera w bazie na hosta. Dla wychodzącego użytkownika zapisuje się czas wyjścia, a reszta grupy dostaje info przez SignalR. |
| **Wstępny MoSCoW** | **Should Have** (oddanie roli), **Must Have** (opuszczenie sesji) |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [TAB-07] Manualna obsługa i łączenie stolików na terminalu POS |
|---|---|
| **Kto i gdzie** | Barman przy terminalu POS |
| **Co robi** | Barman w aplikacji POS ma pełną kontrolę nad stolikami: może ręcznie otworzyć/zamknąć sesję gościom bez telefonu oraz połączyć dwa małe stoliki w jeden duży dla większej ekipy. |
| **Kluczowe mechanizmy** | Łączenie stolików w bazie danych w jedną wspólną sesję wirtualną, interaktywna mapa sali w React 19 aktualizowana na żywo. |
| **Wstępny MoSCoW** | **Should Have** - bez tego system da radę działać, ale bardzo ułatwia pracę barmanowi |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [TAB-08] Zakończenie sesji stolika i zwolnienie miejsca |
|---|---|
| **Kto i gdzie** | Użytkownik-Host w widoku sesji |
| **Co robi** | Host klika zakończ sesję. System sprawdza czy oddano gry i opłacono rachunek, zamyka sesję, a stolik u barmana zmienia kolor na "Do sprzątnięcia". Gracze dostają podsumowanie ze zdobytym XP i opcją oceny gier. |
| **Kluczowe mechanizmy** | Blokada zamknięcia sesji jeśli są nieoddane gry lub nieopłacony rachunek. Zmiana statusu stolika na NeedsCleaning i wysłanie powiadomienia do obsługi przez SignalR. |
| **Wstępny MoSCoW** | **Must Have** - główne zamknięcie obiegu stolika |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [TAB-09] Zarządzanie stolikami lokalu |
|---|---|
| **Kto i gdzie** | Administrator / Manager w panelu webowym |
| **Co robi** | Manager może dodawać nowe stoliki, ustalać ich numerację, liczbę miejsc, przypisywać do strefy (np. Sala Główna, Ogródek) oraz usuwać lub wyłączać stoliki z użytku. |
| **Kluczowe mechanizmy** | Zwykły CRUD w PostgreSQL, soft-delete (dezaktywacja stolika) żeby nie uszkodzić historii starych gier i rachunków powiązanych z tym meblem. |
| **Wstępny MoSCoW** | **Must Have** - bez tego nie da się skonfigurować lokalu |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [TAB-10] Parowanie naklejek NFC i generowanie kodów QR stolików |
|---|---|
| **Kto i gdzie** | Administrator / Manager w panelu webowym |
| **Co robi** | Manager przykłada nową naklejkę NFC do czytnika USB żeby przypisać ją do danego stolika oraz klika "Drukuj kod QR", żeby nakleić go na blat dla ludzi bez NFC. |
| **Kluczowe mechanizmy** | Zapisanie UID fizycznego taga NFC do rekordu stolika w bazie, generowanie obrazka QR z bezpośrednim linkiem do otwarcia sesji. |
| **Wstępny MoSCoW** | **Must Have** - narzędzie potrzebne do fizycznego przygotowania stolików w lokalu |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [TAB-11] Wizualny edytor rzutu sali lokalu  |
|---|---|
| **Kto i gdzie** | Manager / Administrator w panelu webowym |
| **Co robi** | Manager może przeciągać metodą Drag & Drop stoliki na wirtualnej siatce sali, definiować kształty, obracać meble, wyznaczać ściany, bar, toalety i strefy akustyczne. |
| **Kluczowe mechanizmy** | Biblioteka canvas/SVG (Konva.js) w React 19, zapis koordynatów stolików w formacie JSON w PostgreSQL. |
| **Wstępny MoSCoW** | **Could Have** – Edytor rzutu sali jest świetnym bajerem, ale do MVP wystarczy statyczny podgląd stolików. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [TAB-12] Przeniesienie sesji między stolikami |
|---|---|
| **Kto i gdzie** | Barman na terminalu POS lub Host za zgodą personelu |
| **Co robi** | Gdy ekipa chce przesiąść się na większy stolik, system przenosi całą otwartą sesję (graczy, wypożyczone gry, otwarty rachunek) na nowy numer stolika. |
| **Kluczowe mechanizmy** | Transakcyjna zmiana klucza obcego `TableId` w rekordzie sesji w PostgreSQL z weryfikacją wolnego miejsca, powiadomienie SignalR. |
| **Wstępny MoSCoW** | **Must Have** – codzienna sytuacja w zatłoczonym lokalu. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [TAB-13] Zmiana statusu stolika na „Awaria / Wyłączony z użytku” |
|---|---|
| **Kto i gdzie** | Barman na terminalu POS |
| **Co robi** | W przypadku uszkodzenia krzesła, zalania blatu lub rezerwacji na wyłączność barman oznacza stolik jako `OutOfOrder`. Stolik staje się niedostępny do zajęcia przez NFC/QR. |
| **Kluczowe mechanizmy** | Aktualizacja flagi statusu stolika w bazie, odrzucanie żądań parowania kodem 423 Locked. |
| **Wstępny MoSCoW** | **Should Have** – zapobiega siadaniu gości przy uszkodzonych meblach. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

## 4. Gry planszowe, BGG i obieg wypożyczeń

| ID & Nazwa | [GAME-01] Integracja z bazą BoardGameGeek |
|---|---|
| **Kto i gdzie** | Administrator / Manager w panelu webowym |
| **Co robi** | Manager wpisuje ID gry z BGG lub jej tytuł, a system automatycznie pobiera okładkę, czas gry, wagę trudności, kategorie i dozwoloną liczbę graczy. |
| **Kluczowe mechanizmy** | Pobieranie danych z publicznego API BGG (XML/JSON), parsowanie i zapis do tabeli Games w PostgreSQL. |
| **Wstępny MoSCoW** | **Must Have** - ręczne wpisywanie setek gier i mechanik zajęłoby wieczność |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [GAME-02] Ewidencja fizycznych egzemplarzy |
|---|---|
| **Kto i gdzie** | Administrator / Manager w panelu webowym i przy czytniku USB |
| **Co robi** | Manager tworzy fizyczne kopie gier (np. 3 pudełka Catana: CATAN-01, CATAN-02), przypisuje do nich naklejki NFC i półkę na regale (np. Regał A, Półka 2). |
| **Kluczowe mechanizmy** | Relacja jeden-do-wielu (jedna gra ma wiele fizycznych egzemplarzy), przypisanie UID tagu NFC i licznik rozegranych partii danego pudełka. |
| **Wstępny MoSCoW** | **Must Have** - lokal musi wiedzieć ile fizycznych pudełek ma na stanie |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [GAME-03] Przeglądanie katalogu gier w lokalu |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej |
| **Co robi** | Gracz przegląda listę gier z filtrami: liczba graczy, czas partii, poziom trudności (waga BGG) oraz filtr "tylko aktualnie wolne na półce". |
| **Kluczowe mechanizmy** | Zapytanie GET do API z filtrowaniem w PostgreSQL, sprawdzanie na żywo czy dany egzemplarz ma status AvailableOnShelf. |
| **Wstępny MoSCoW** | **Must Have** - podstawa wyboru gry przez gości |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [GAME-04] Samodzielne wypożyczenie gry przez NFC przy stole |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej przy aktywnym stoliku |
| **Co robi** | Gracz bierze pudełko z półki, przykłada telefon do naklejki NFC na grze. Gra zostaje przypisana do jego stolika, a u barmana stolik zmienia status. |
| **Kluczowe mechanizmy** | Walidacja czy gracz ma otwartą sesję stolika, sprawdzenie czy egzemplarz jest wolny i zmiana statusu w bazie na CheckedOut. |
| **Wstępny MoSCoW** | **Must Have** - kluczowy ficzer eliminujący kolejki do baru |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [GAME-05] Alternatywne wypożyczenie gry (Skan QR / Barman przy POS) |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej lub Barman przy terminalu POS |
| **Co robi** | Gdy telefon nie ma NFC, gracz skanuje kod QR z pudełka aparatem. Jeśli gracz w ogóle nie ma telefonu, barman kładzie pudełko na czytniku USB przy ladzie i przypisuje do stolika na POS. |
| **Kluczowe mechanizmy** | Czytnik USB RFID/NFC działający w standardzie emulacji klawiatury (Keyboard Wedge / Plug & Play) wprowadzający UID tagu bezpośrednio do aktywnego formularza w React POS lub endpoint API rejestrujący skan kodu QR z pudełka aparatem w aplikacji mobilnej. |
| **Wstępny MoSCoW** | **Must Have** - fallback dla ludzi bez NFC lub bez aplikacji |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [GAME-06] Zabezpieczenie przed wyścigiem (Blokada współbieżności) |
|---|---|
| **Kto i gdzie** | System w backendzie |
| **Co robi** | Jeśli dwóch graczy w tej samej sekundzie zbliży telefon do tego samego pudełka gry, system wypożycza grę tylko jednemu, a drugiemu wyświetla błąd że gra została już zajęta. |
| **Kluczowe mechanizmy** | Blokada optymistyczna w PostgreSQL (RowVersion / xmin) uniemożliwiająca podwójne wypożyczenie tego samego egzemplarza (zwraca błąd 409 Conflict). |
| **Wstępny MoSCoW** | **Must Have** - bez tego dwie osoby mogłyby wypożyczyć to samo fizyczne pudełko |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [GAME-07] Zgłoszenie braków i uszkodzeń aparatem |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej w ciągu 10 minut od wypożyczenia |
| **Co robi** | Po otwarciu pudełka gracz widzi brakujący pionek lub zalaną planszę. Robi zdjęcie w aplikacji i wysyła zgłoszenie, dzięki czemu obsługa wie, że to nie on zniszczył grę. |
| **Kluczowe mechanizmy** | Kompresja zdjęcia w telefonie do WebP, wysłanie do API i przypięcie do danego wypożyczenia w bazie, powiadomienie na POS barmana. |
| **Wstępny MoSCoW** | **Should Have** - świetny mechanizm zabezpieczający gracza i lokal, ale system ruszy też bez tego |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [GAME-08] Hub aktywnej partii |
|---|---|
| **Kto i gdzie** | Wszyscy gracze przy danym stoliku w aplikacji mobilnej |
| **Co robi** | Ekran trwającej gry ze stoperem czasu partii, linkami do zasad na YouTube w 3 minuty, cyfrową instrukcją PDF oraz wirtualną kostką do rzucania w razie zgubionych kości. |
| **Kluczowe mechanizmy** | Licznik czasu w aplikacji, zapisywanie timestampu startu partii w bazie, linki do zewnętrznych wideoporadników. |
| **Wstępny MoSCoW** | **Should Have** - duża wygoda dla graczy żeby nie szukać zasad w internecie |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [GAME-09] Zwrot gry przy ladzie i bramka inspekcji |
|---|---|
| **Kto i gdzie** | Barman przy terminalu POS |
| **Co robi** | Gracz odnosi grę do baru. Barman kładzie pudełko na czytniku USB. System zamyka wypożyczenie, a barman zatwierdza: "Gra sprawna (wraca na półkę)" lub "Gra uszkodzona (kwarantanna)". |
| **Kluczowe mechanizmy** | Odczyt UID tagu z pudełka przez czytnik USB RFID w trybie emulacji klawiatury (Keyboard Wedge / Plug & Play), zamknięcie rekordu w tabeli rentals, powiązanie z ewentualnymi zdjęciami szkód (tabela rental_damage_photos), naliczenie punktów XP graczom i aktualizacja statusu egzemplarza w PostgreSQL. |
| **Wstępny MoSCoW** | **Must Have** - bez zwrotu gra na zawsze wisiałaby jako wypożyczona |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [GAME-10] Panel kwarantanny i naprawy gier |
|---|---|
| **Kto i gdzie** | Administrator / Obsługa w panelu webowym |
| **Co robi** | Lista gier wycofanych z półki. Pracownik widzi co jest uszkodzone (np. "brak 2 zielonych pionków"), może odznaczyć naprawę i przywrócić grę do wypożyczeń. |
| **Kluczowe mechanizmy** | Status InQuarantine na poziomie egzemplarza w bazie, historia zgłoszonych usterek i zdjęć. |
| **Wstępny MoSCoW** | **Should Have** - bez tego da radę działać, ale bardzo ułatwia serwis gier w lokalu |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [GAME-11] Ręczne dodawanie gry do katalogu |
|---|---|
| **Kto i gdzie** | Menadżer / Admin w panelu webowym |
| **Co robi** | Menadżer może dodać grę całkowicie ręcznie przez formularz (gdy gry nie ma na BGG lub API ma awarię): wpisuje tytuł, liczbę graczy, czas gry, trudność, wybiera tagi mechanik i wgrywa zdjęcie okładki z dysku. |
| **Kluczowe mechanizmy** | Endpoint w ASP.NET Core z autoryzacją ról (Admin ma pełnego CRUD-a), walidacja formularza FluentValidation, zapis pliku okładki na serwerze. |
| **Wstępny MoSCoW** | **Must Have** - niezbędna alternatywa dla automatycznego BGG Sync |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [GAME-12] Obsługa dodatków i rozszerzeń do gier |
|---|---|
| **Kto i gdzie** | Gracz w aplikacji mobilnej oraz Manager w panelu |
| **Co robi** | Gry w katalogu mają powiązane kompatybilne dodatki (np. Catan + Żeglarze). Gracz widzi, czy dodatek jest na półce, i może wypożyczyć go wspólnie z podstawką lub osobno. |
| **Kluczowe mechanizmy** | Relacja `BaseGame` <-> `Expansion` w PostgreSQL, synchronizacja powiązań z BGG API. |
| **Wstępny MoSCoW** | **Should Have** – standard w świecie gier planszowych. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [GAME-13] Alert o nieoddanym pudełku po wyjściu gości |
|---|---|
| **Kto i gdzie** | System na terminalu POS barmana |
| **Co robi** | Jeśli sesja stolika zostanie zakończona lub upłynie czas rezerwacji, a gra nadal ma status `CheckedOut`, barman otrzymuje pilny alert: „Stolik 7 opuścił salę bez zwrotu gry Nemesis!”. |
| **Kluczowe mechanizmy** | Weryfikacja spójności stanu sesji przed rozliczeniem, blokada automatycznego rozliczenia bez potwierdzenia zwrotu gry. |
| **Wstępny MoSCoW** | **Must Have** – bezpośrednio likwiduje gubienie gier w lokalu. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [GAME-14] Rejestr znalezionych elementów na sali |
|---|---|
| **Kto i gdzie** | Barman / Personel sprzątający na terminalu POS |
| **Co robi** | Po znalezieniu pojedynczego pionka lub kostki na podłodze pracownik klika „Znaleziono element” i wybiera: „Żółty drewniany sześcian”. System przeszukuje bazę zawartości gier oraz historię stolików z danego rejonu sali i podpowiada: „Najbardziej prawdopodobna gra: Terraformacja Marsa, stolik nr 5 wczoraj o 21:00”. |
| **Kluczowe mechanizmy** | Tabela komponentów gier w PostgreSQL, silnik korelacji czasu i lokalizacji stolika z bazą inwentarza. |
| **Wstępny MoSCoW** | **Should Have** – innowacyjny ficzer rozwiązujący odwieczną zmorę każdego lokalu planszówkowego. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [GAME-15] Ocenianie gier przez użytkownika (Skala BGG 1-10) |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej w widoku gry lub po zakończonej partii |
| **Co robi** | Gracz może wystawić grze ocenę w skali od 1.0 do 10.0 (wzorowane na standardzie BoardGameGeek). Oceny zasilają profil gracza, historię jego preferencji dla algorytmu AI oraz budują lokalny ranking i średnią ocenę gry w kawiarni. |
| **Kluczowe mechanizmy** | Tabela `user_ratings` w PostgreSQL z ograniczeniem `CHECK (rating >= 1.0 AND rating <= 10.0)`, automatyczne przeliczanie zagregowanych kolumn `local_avg_rating` i `local_rating_count` w tabeli `games`. |
| **Wstępny MoSCoW** | **Should Have** - kluczowe dla personalizacji rekomendacji i zaangażowania społeczności graczy. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

## 5. Inteligentny doradca stolika i moduł AI (ISI & Systemy Rozmyte na zaliczenie przemiotów)

| ID & Nazwa | [AI-01] Konfigurator filtrów sesji stolika (Filtry ISI) |
|---|---|
| **Kto i gdzie** | Host w aplikacji mobilnej przy otwartej sesji |
| **Co robi** | Host klika przycisk "W co gramy?" i ustawia preferencje: ile czasu mają (np. do 60 min), jaki klimat (rywalizacja, kooperacja, imprezowa). Liczba graczy bierze się automatycznie z obecnych przy stole. |
| **Kluczowe mechanizmy** | Pobranie aktualnego składu stolika z bazy i przesłanie parametrów wejściowych do mikroserwisu rekomendacji w Pythonie. |
| **Wstępny MoSCoW** | **Must Have** - podstawa do wystartowania doradcy |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [AI-02] Rekomendacja grupowa - strategia kompromisu |
|---|---|
| **Kto i gdzie** | System w backendzie dla całej grupy |
| **Co robi** | Algorytm analizuje polubione kategorie i historię partii wszystkich graczy przy stole i wybiera gry które dają największą średnią satysfakcję dla całej grupy. |
| **Kluczowe mechanizmy** | Moduł ISI z algorytmem Collaborative Filtering / Content-Based, liczenie średniego wektora preferencji grupy z bazy BGG. |
| **Wstępny MoSCoW** | **Must Have** - główny silnik polecania gier pod zaliczenie ISI |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [AI-03] Ochrona początkujących graczy |
|---|---|
| **Kto i gdzie** | System w backendzie |
| **Co robi** | Jeśli przy stole siedzi chociaż jeden nowy gracz z małym doświadczeniem, system wycina zbyt trudne gry (np. złożoność BGG > 3.5), żeby nie zepsuć mu wieczoru paraliżem myślenia. |
| **Kluczowe mechanizmy** | Reguła Least Misery w module rekomendacji, odrzucanie gier gdzie min-satysfakcja któregoś gracza spada poniżej ustalonego progu. |
| **Wstępny MoSCoW** | **Must Have** - bardzo ważna funkcja żeby nowi gracze się nie odbili |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [AI-04] Filtr fizycznie wolnych gier na półce w czasie rzeczywistym |
|---|---|
| **Kto i gdzie** | System w backendzie |
| **Co robi** | System poleca WYŁĄCZNIE te gry, które w tej sekundzie leżą fizycznie wolne na regale w lokalu. Nigdy nie poleci gry która jest już wypożyczona przez inny stolik albo siedzi w kwarantannie. |
| **Kluczowe mechanizmy** | Inner join z tabelą GameCopies w PostgreSQL filtrujący tylko status AvailableOnShelf przed zwróceniem wyników z AI. |
| **Wstępny MoSCoW** | **Must Have** - bez tego algorytm polecałby gry których nie ma w lokalu |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [AI-05] Wyjaśnialność rekomendacji AI (Explainable AI - XAI / SHAP) |
|---|---|
| **Kto i gdzie** | Użytkownicy przy stoliku oraz obsługa lokalu w aplikacji |
| **Co robi** | Rekomendacja nie jest czarną skrzynką. Przy każdej zaproponowanej grze użytkownik może rozwinąć interaktywny wykres kaskadowy (Waterfall Plot) oparty na wartościach SHAP (Shapley Additive exPlanations), który dokładnie pokazuje, jaki wpływ na wybór miały poszczególne cechy (np. +40% za zgodność mechaniki Worker Placement, +25% za optymalny czas partii, -10% za wysoką losowość). |
| **Kluczowe mechanizmy** | Moduł XAI (biblioteka SHAP w mikroserwisie Python), obliczanie addytywnych wkładów cech do estymacji i generowanie wektora wag do wizualizacji na wykresie. |
| **Wstępny MoSCoW** | **Should Have** - kluczowy element badawczy eliminujący zjawisko „czarnej skrzynki” w AI |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [AI-06] Rozmyty estymator czasu partii i paraliżu decyzyjnego (ANFIS) |
|---|---|
| **Kto i gdzie** | System dla graczy w aplikacji i dla barmana na mapie sali |
| **Co robi** | Zamiast sztywnego czasu z pudełka system wylicza realny czas partii uwzględniając paraliż myślenia graczy. Wyświetla szacowany czas zakończenia, a u barmana stolik robi się żółty jeśli partia zaczyna się mocno przeciągać. |
| **Kluczowe mechanizmy** | Model neuro-rozmyty ANFIS (zaliczenie przedmiotu Systemy Rozmyte): zmienne lingwistyczne (waga gry, doświadczenie grupy, ilość osób) i reguły IF-THEN wyliczające doliczony czas. |
| **Wstępny MoSCoW** | **Must Have** - kluczowy model pod zaliczenie Systemów Rozmytych |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [AI-07] Pętla zwrotna rekomendacji - Ocena trafności AI |
|---|---|
| **Kto i gdzie** | Gracze w aplikacji mobilnej po zakończeniu rozgrywki |
| **Co robi** | Po zwrocie gry poleconej przez doradcę gracz otrzymuje krótkie pytanie: „Czy rekomendacja była trafiona? (1–5 gwiazdek)”. Wyniki zasilają algorytm uczenia maszynowego. |
| **Kluczowe mechanizmy** | Zapis oceny trafności rekomendacji `RecommendationFeedback` w bazie PostgreSQL, eksport danych do treningu modeli collaborative filtering w Pythonie. |
| **Wstępny MoSCoW** | **Should Have** - niezbędne do ewaluacji jakości algorytmów rekomendacji w rozdziale badawczym pracy. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [AI-08] Rekomendacja przekąsek pod typ gry |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej przy zamówieniu gastro |
| **Co robi** | Algorytm podpowiada przekąski w zależności od wypożyczonej gry: przy drogich, ciężkich grach promuje pozycje „bezpieczne dla kart” (niebrudzące rąk, np. orzechy, drinki ze słomką) i ostrzega przed tłustymi daniami (np. skrzydełka BBQ). |
| **Kluczowe mechanizmy** | Flaga `IsCardFriendly` w pozycjach menu gastro, reguły rekomendacji krzyżowej (cross-selling) w module analitycznym. |
| **Wstępny MoSCoW** | **Could Have** – genialny smaczek łączący gastronomię ze specyfiką lokalu z grami planszowymi. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [AI-09] Adaptacyjny estymator paraliżu myślenia na bazie składu stolika |
|---|---|
| **Kto i gdzie** | Mikroserwis Python w tle |
| **Co robi** | Model ANFIS dynamicznie koryguje szacowany czas gry o współczynnik "Analysis Paralysis Index" wyliczany na podstawie historii czasu ruchów poszczególnych graczy obecnych przy stole. |
| **Kluczowe mechanizmy** | Wektor cech graczy przekazywany do inferencji modelu neuro-rozmytego w FastAPI. |
| **Wstępny MoSCoW** | **Could Have** – Estymator paraliżu myślenia na bazie składu graczy; bazowy model ANFIS zrealizowany jest w AI-06. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [AI-10] Predykcja subiektywnej oceny gracza (Uczenie Maszynowe - Regresja) |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej w widoku szczegółów gry |
| **Co robi** | System szacuje przewidywaną ocenę w skali 1.0–10.0 („Prognozujemy, że ocenisz tę grę na 8.4/10”), jaką dany gracz wystawiłby nowemu, jeszcze niegranemu przez siebie tytułowi. Pozwala to na trafny dobór gier w ciemno. |
| **Kluczowe mechanizmy** | Model regresyjny (Random Forest Regressor / Ridge Regression w scikit-learn) trenowany na profilach wektorowych graczy i macierzy dotychczasowych ocen `user_ratings`. |
| **Wstępny MoSCoW** | **Should Have** - zaawansowany algorytm predykcyjny podnoszący wartość badawczą modułu AI |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

## 6. Paszport gracza, grywalizacja i Koło Mechanik BGG

| ID & Nazwa | [PASS-01] Interaktywne Koło Mechanik BGG w SVG/D3 |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej w zakładce Paszport |
| **Co robi** | Wykres kołowy hierarchii mechanik planszowych z BGG (np. Worker Placement, Deck Building). Użytkownik może klikać w wycinki koła i sprawdzać w jakie gry z tą mechaniką już grał. |
| **Kluczowe mechanizmy** | Biblioteka react-native-svg + D3-hierarchy, renderowanie drzewa mechanik pobranego z backendu. |
| **Wstępny MoSCoW** | **Should Have** - efektowny komponent wizualny; w wersji MVP dopuszcza się czytelną listę/siatkę odblokowanych mechanik jako fallback |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [PASS-02] Efekt mgły wojny i wskaźnik odkrycia mechanik |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej |
| **Co robi** | Na początku całe koło mechanik jest wyszarzone. Po zagraniu w grę z daną mechaniką ten kawałek koła trwale się podświetla i rośnie licznik: "Odkryłeś 34% mechanik planszowych". |
| **Kluczowe mechanizmy** | Zapisywanie unikalnych odkrytych mechanik w profilu użytkownika w PostgreSQL po zakończeniu sesji gry. |
| **Wstępny MoSCoW** | **Should Have** - motywator grywalizacji; licznik procentowy odblokowanych mechanik z BGG |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [PASS-03] Naliczanie punktów doświadczenia (XP) za gry i zamówienia |
|---|---|
| **Kto i gdzie** | System nalicza punkty zalogowanym graczom i kontom Shadow |
| **Co robi** | Po zakończeniu partii każdy gracz dostaje punkty XP (zależne od wagi gry i czasu) oraz dodatkowe punkty za każdą wydaną złotówkę na barze. |
| **Kluczowe mechanizmy** | Algorytm przeliczania XP w ASP.NET Core po zamknięciu sesji, aktualizacja stanu konta w bazie. |
| **Wstępny MoSCoW** | **Must Have** - podstawa systemu poziomów |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [PASS-04] Rangi gracza i stałe zniżki na barze |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji oraz Barman na terminalu POS |
| **Co robi** | Po uzbieraniu określonej liczby XP gracz wbija wyższą rangę (Nowicjusz -> Amator Kostek -> Mistrz Strategii -> Arcymistrz BGG). Wyższa ranga odblokowuje stały rabat np. 5% lub 10% na barze który sam nalicza się przy kasie. |
| **Kluczowe mechanizmy** | Tabela rang w bazie, automatyczne naliczanie rabatu po identyfikacji klienta na POS. |
| **Wstępny MoSCoW** | **Must Have** - łączy granie w planszówki ze sprzedażą na barze |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [PASS-05] System osiągnięć i odznak |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej |
| **Co robi** | Gracz odblokowuje wirtualne odznaki za specjalne osiągnięcia (np. "Pierwsza partia", "Mózgożerca - gra o trudności 4.0+", "Nocny Marek - partia po północy"). Zdobyte odznaki wpadają do gabloty w profilu i dają jednorazowy bonus punktów XP. |
| **Kluczowe mechanizmy** | Sprawdzanie warunków odznak w zdarzeniach domenowych po zakończeniu partii lub opłaceniu rachunku, przypisanie odznaki do konta i dopisanie punktów XP. |
| **Wstępny MoSCoW** | **Should Have** - fajny smaczek, bez tego apka też działa |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [PASS-06] Dziennik partii, arkusz punktacji i statystyki ze znajomymi |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej |
| **Co robi** | Gracz może przeglądać swoje archiwalne rozgrywki, wpisywać wyniki punktowe po partii, wyłaniać zwycięzcę i sprawdzać bilans wygranych ze znajomymi ze stolika. |
| **Kluczowe mechanizmy** | Relacja partii z arkuszem wyników w PostgreSQL, wyliczanie procentu wygranych (win-rate). |
| **Wstępny MoSCoW** | **Should Have** - super ficzer dla planszówkowiczów |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [PASS-07] Lokalna tablica liderów i Hall of Fame |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej |
| **Co robi** | Ranking miesięczny i wszech czasów bywalców lokalu: gracze z największą liczbą zdobytych XP, największą liczbą unikalnych tytułów oraz mistrzowie konkretnych gier. |
| **Kluczowe mechanizmy** | Zapytania widoków zmaterializowanych w PostgreSQL. |
| **Wstępny MoSCoW** | **Should Have** – napędza rywalizację i częstotliwość powrotów do lokalu. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [PASS-08] Cotygodniowe wyzwania i misje z nagrodami |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej w zakładce Paszport |
| **Co robi** | Zadania odnawiane co poniedziałek, np.: „Zagraj w grę z mechaniką Deck Building”, „Odwiedź lokal we wtorek przed 18:00”, „Wygraj partię 4-osobową”. Za ukończenie gracz dostaje duży bonus XP przyspieszający wbicie wyższej rangi. |
| **Kluczowe mechanizmy** | Moduł misji weryfikujący aktywność gracza z bieżącego tygodnia na podstawie rozegranych partii i automatyczne naliczanie punktów XP za zaliczone cele. |
| **Wstępny MoSCoW** | **Should Have** – motywuje do zapełniania lokalu w mniej popularne dni tygodnia. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [PASS-09] Interaktywny kalkulator punktacji partii na żywo |
|---|---|
| **Kto i gdzie** | Gracze przy stole w aplikacji mobilnej |
| **Co robi** | Zamiast papierowego notesu aplikacja udostępnia formularze liczenia punktów dopasowane do konkretnych gier (np. Scrabble, 7 Cudów Świata, Everdell) z podziałem na kategorie punktacji i liczeniem na bieżąco w trakcie gry. Aplikacja sama sumuje wyniki i wyłania zwycięzcę. |
| **Kluczowe mechanizmy** | Szablony JSON arkuszy kalkulacyjnych w React Native, automatyczny zapis do historii partii i bilansu graczy. |
| **Wstępny MoSCoW** | **Should Have** – wygoda eliminująca konieczność szukania ołówka i kalkulatora. Trzeba dla każdej gry zrobić osobny arkusz|

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [PASS-10] Tablica szukania graczy przy stoliku |
|---|---|
| **Kto i gdzie** | Host przy stoliku oraz Użytkownicy w aplikacji mobilnej |
| **Co robi** | Grupa 2 osób chcąca zagrać w grę na 4 osoby klika „Szukamy +2 graczy do gry Terraformacja Marsa”. Wszyscy goście w lokalu widzą ogłoszenie na tablicy i mogą podejść lub zgłosić się przez aplikację. |
| **Kluczowe mechanizmy** | Flaga `LookingForPlayers` przypisana do aktywnej sesji stolika, powiadomienia broadcast w obrębie lokalu. |
| **Wstępny MoSCoW** | **Could Have** – Tablica szukania graczy jest fajna społecznościowo, ale niepotrzebna do grania na sali. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [PASS-11] Bezpośrednie porównanie profili i bilans pojedynków H2H |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej |
| **Co robi** | Gracz klika profil znajomego i widzi bezpośredni bilans: „Zagraliście razem 14 partii: 8 wygranych, 6 przegranych”, wspólne ulubione gry oraz porównanie stopnia odkrycia Koła Mechanik BGG. |
| **Kluczowe mechanizmy** | Zapytanie agregujące w PostgreSQL filtrujące wspólne identyfikatory `GameSessionId` obu użytkowników. |
| **Wstępny MoSCoW** | **Could Have** – świetny smaczek społecznościowy |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [PASS-12] Weryfikacja wyniku partii przez współgraczy |
|---|---|
| **Kto i gdzie** | Wszyscy gracze przy stole w aplikacji |
| **Co robi** | Po wprowadzeniu punktów przez hosta pozostali uczestnicy otrzymują powiadomienie z prośbą o akceptację wyniku. Dopiero po zatwierdzeniu punkty XP i statystyki win-rate są trwale dopisywane do bazy. |
| **Kluczowe mechanizmy** | Maszyna stanów weryfikacji partii (`PendingApproval` -> `Verified`), zapobiega oszustwom i fałszowaniu rankingów. |
| **Wstępny MoSCoW** | **Should Have** – gwarantuje rzetelność danych turniejowych i ligowych. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [PASS-13] Generator grafiki podsumowania partii na Social Media |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej |
| **Co robi** | Przycisk „Udostępnij relację”: aplikacja generuje estetyczną pionową grafikę (format 9:16) z okładką gry, miejscem na opcjonalne selfie z partii, podsumowaniem punktów i logiem lokalu, gotową do wrzucenia na Instagram Stories / Facebooka. |
| **Kluczowe mechanizmy** | Renderowanie Canvas w React Native, natywny moduł udostępniania systemowego (Share Sheet). |
| **Wstępny MoSCoW** | **Could Have** – Generator grafiki na social media jest opcjonalnym dodatkiem marketingowym. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [PASS-14] Analiza prywatnej kolekcji BGG – Półka Wstydu i zmęczenie materiału |
|---|---|
| **Kto i gdzie** | Gracz w aplikacji mobilnej w profilu paszportu |
| **Co robi** | Gracz może zsynchronizować konto ze swoim profilem na BoardGameGeek. System analizuje jego domową kolekcję i oznacza gry posiadane, w które rozegrano 0 partii lub niebyły grane od >6 miesięcy („Półka Wstydu” / *Shelf of Shame*). Wykrywa także spadek częstotliwości grania w dawne ulubione tytuły (*Game Fatigue*) i sugeruje odświeżające alternatywy o pokrewnych mechanikach. |
| **Kluczowe mechanizmy** | Asynchroniczna integracja z BGG XML API2 (`/collection`), analiza dat ostatnich partii w relacji do średnich ocen i mechanik BGG. |
| **Wstępny MoSCoW** | **Should Have** - świetny psychologiczno-grywalizacyjny aspekt angażujący hobbystów planszówek |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

## 7. Gastronomia ze stolika i obsługa kuchni/baru (KDS)

| ID & Nazwa | [ORDER-01] Cyfrowe menu lokalu z piwami kraftowymi i jedzeniem |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej przy stoliku |
| **Co robi** | Gracz przegląda menu gastro podzielone na kategorie (krafty, alkohole, bezalko, przekąski, ciepłe dania). Przy piwach widzi parametry: styl, IBU, ekstrakt i browar. Pozycje wyprzedane są od razu wyszarzone. |
| **Kluczowe mechanizmy** | Pobieranie menu z bazy, SignalR wyłącza pozycje w telefonach w czasie rzeczywistym gdy skończy się keg. |
| **Wstępny MoSCoW** | **Must Have** - podstawa zamawiania ze smartfona |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [ORDER-02] Koszyk zamówienia z modyfikatorami |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej |
| **Co robi** | Gracz dodaje pozycje do koszyka, wybiera warianty (np. sos do nachosów, wielkość porcji) i może dopisać notatkę dla kuchni (np. "bez cebuli"). |
| **Kluczowe mechanizmy** | Lokalny stan koszyka w aplikacji mobilnej, przeliczanie kwoty z uwzględnieniem dodatków. |
| **Wstępny MoSCoW** | **Must Have** - niezbędne do złożenia zamówienia |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [ORDER-03] Idempotentne wysłanie zamówienia |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej |
| **Co robi** | Gracz klika "Zamów i dopisz do stolika". Jeśli w pubie zerwie WiFi i kliknie dwa razy, zamówienie nie zdubluje się na kuchni ani na rachunku. |
| **Kluczowe mechanizmy** | Generowanie unikalnego klucza `idempotency_key` (UUID) w telefonie, backend w .NET sprawdza unikalność klucza w PostgreSQL i ignoruje powtórzone żądanie. |
| **Wstępny MoSCoW** | **Must Have** - zabezpieczenie przed podwójnym skasowaniem klienta |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [ORDER-04] Kafelkowy ekran zamówień KDS dla personelu |
|---|---|
| **Kto i gdzie** | Barman / Kucharz na ekranie KDS w przeglądarce |
| **Co robi** | Zamówienia z telefonów wpadają na kafelkowy ekran barmana ułożone od najstarszego. Barman klika kafelek i zmienia status: Nowe -> W przygotowaniu -> Gotowe do odbioru. |
| **Kluczowe mechanizmy** | SignalR odbiera nowe zamówienie i natychmiast wrzuca kafelek na ekran KDS bez odświeżania strony. |
| **Wstępny MoSCoW** | **Must Have** - główny widok pracy personelu przy realizacji zamówień |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [ORDER-05] Ostrzeżenia czasowe na KDS |
|---|---|
| **Kto i gdzie** | Barman / Kucharz na ekranie KDS |
| **Co robi** | Każdy kafelek ma stoper od momentu zamówienia. Jeśli zamówienie czeka dłużej niż 15 minut, kafelek zaczyna pulsować na czerwono żeby obsługa wiedziała o opóźnieniu. |
| **Kluczowe mechanizmy** | Prosty interwał czasowy w React przeliczający minuty od utworzenia zamówienia i zmieniający klasę CSS na alert. |
| **Wstępny MoSCoW** | **Should Have** - bez tego da radę działać, ale bardzo pomaga w pilnowaniu kolejki |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [ORDER-06] Powiadomienia na żywo o gotowości zamówienia |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej przy stoliku |
| **Co robi** | Gdy barman kliknie "Gotowe" na KDS, telefon gracza wibruje i wyświetla powiadomienie: "Twoje zamówienie czeka do odbioru przy barze!". |
| **Kluczowe mechanizmy** | SignalR wysyła zdarzenie do aplikacji mobilnej konkretnego użytkownika po UserId. |
| **Wstępny MoSCoW** | **Must Have** - gracz wie kiedy podejść do baru bez stania w kolejce |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [ORDER-07] Sprzedaż bezpośrednia z lady na terminalu POS |
|---|---|
| **Kto i gdzie** | Barman na terminalu POS |
| **Co robi** | Obsługa gości podchodzących do lady bez otwartego stolika (np. ktoś wchodzi tylko kupić piwo na wynos lub kawę). Barman wybiera produkty, pobiera płatność przy ladzie i od razu zamyka rachunek. |
| **Kluczowe mechanizmy** | Transakcja bez powiązania z `TableSessionId` (tzw. `QuickSale`), natychmiastowe zdjęcie ze stanu magazynowego. |
| **Wstępny MoSCoW** | **Must Have** – podstawowa funkcjonalność każdego lokalu gastronomicznego. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [ORDER-08] Silnik promocji czasowych i Happy Hours |
|---|---|
| **Kto i gdzie** | Manager konfiguruje w panelu, System nalicza na POS |
| **Co robi** | System automatycznie kalkuluje rabaty na barze. Zniżki naliczają się na podstawie stałego rabatu z najwyższej rangi lojalnościowej gracza przy stole (np. Ranga Gold = stałe -10% na barze) oraz predefiniowanych zestawów promocyjnych w menu. |
| **Kluczowe mechanizmy** | Automatyczne przeliczanie kwoty zamówienia na kasie POS i w aplikacji mobilnej z uwzględnieniem stawek rabatowych graczy obecnych w sesji stolika. |
| **Wstępny MoSCoW** | **Should Have** – narzędzie marketingowe do stymulacji obrotów w martwych godzinach. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [ORDER-09] Wybór trybu serwisu: Dostawa do stolika vs Odbiór przy barze |
|---|---|
| **Kto i gdzie** | Użytkownik w koszyku zamówienia mobilnego |
| **Co robi** | Klient wybiera: „Przynieście do stolika (serwis kelnerski)” lub „Odbiorę sam przy barze po powiadomieniu”. Opcja wyświetla się na kafelku zamówienia na KDS. |
| **Kluczowe mechanizmy** | Flaga `DeliveryMode` na poziomie zamówienia, dostosowanie workflow na ekranie KDS. |
| **Wstępny MoSCoW** | **Should Have** – ułatwia organizację pracy w lokalach z obsługą mieszaną. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [ORDER-10] Odrzucenie / brak pozycji na kuchni z powiadomieniem gracza |
|---|---|
| **Kto i gdzie** | Kucharz / Barman na ekranie KDS |
| **Co robi** | Jeśli skończył się składnik dania, pracownik klika „Odrzuć pozycję: Brak na stanie”. Telefon gracza wibruje z komunikatem, pozycja jest usuwana z rachunku stolika, a produkt automatycznie wyszarza się w menu dla wszystkich gości. |
| **Kluczowe mechanizmy** | Komunikat SignalR `OrderItemRejected`, korekta salda w PostgreSQL, aktualizacja stanu dostępności produktu w czasie rzeczywistym. |
| **Wstępny MoSCoW** | **Must Have** – zapobiega czekaniu gościa na danie, którego kuchnia nie może wydać. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [ORDER-11] Kontrola serwowania alkoholu i weryfikacja pełnoletności (18+) |
|---|---|
| **Kto i gdzie** | System i Barman przy wydawaniu zamówienia z alkoholem |
| **Co robi** | Zamówienia zawierające alkohol są oznaczone na KDS czerwoną ikoną `18+`. Przy pierwszym zamówieniu alkoholu na dany stolik barman musi zweryfikować dowód tożsamości i zatwierdzić uprawnienie jednym kliknięciem na POS. |
| **Kluczowe mechanizmy** | Flaga `RequiresAgeCheck` w pozycji menu, blokada statusu „Wydane” na KDS bez potwierdzenia weryfikacji wieku. |
| **Wstępny MoSCoW** | **Must Have** – bezwzględny wymóg prawny ustawy o wychowaniu w trzeźwości. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [ORDER-12] Pakiety imprezowe i zestawy planszówkowe |
|---|---|
| **Kto i gdzie** | Gracz w aplikacji mobilnej w menu gastro |
| **Co robi** | Zamawianie gotowych zestawów dla ekip: np. „Zestaw Mózgożerca: 4 piwa kraftowe + duży półmisek nachosów + orzechy z rabatem 20%”. System automatycznie zdejmuje ze stanu odpowiednie składniki. |
| **Kluczowe mechanizmy** | Encja pakietu wielopozycyjnego w bazie, automatyczne rozbicie na komponenty magazynowe. |
| **Wstępny MoSCoW** | **Should Have** – podnosi średnią wartość koszyka w lokalu. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

## 8. Rozliczenie, płatności i rachunek stolika

| ID & Nazwa | [BILL-01] Podgląd wspólnego rachunku stolika na żywo |
|---|---|
| **Kto i gdzie** | Wszyscy gracze przy stole w aplikacji mobilnej |
| **Co robi** | Każdy gracz widzi na żywo cały rachunek stolika: kto co zamówił, jakie są kwoty cząstkowe i jaka jest łączna suma do zapłaty. |
| **Kluczowe mechanizmy** | Zapytanie do bazy grupujące pozycje po użytkownikach przypisanych do sesji stolika, aktualizowane przez SignalR. |
| **Wstępny MoSCoW** | **Must Have** - pełna przejrzystość rachunku dla grupy |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">


| ID & Nazwa | [BILL-02] Płatność tradycyjna przy ladzie |
|---|---|
| **Kto i gdzie** | Barman na terminalu POS |
| **Co robi** | Gracz podchodzi do baru i płaci gotówką lub kartą na terminalu fizycznym. Barman klika "Opłacono gotówką/kartą" i zamyka pozycje w systemie (cały stolik). |
| **Kluczowe mechanizmy** | Zmiana statusu pozycji rachunku w bazie z poziomu POS z walidacją roli Barmana. Całkowity brak bramek płatności online. |
| **Wstępny MoSCoW** | **Must Have** - jedyna forma płatności w lokalu |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [BILL-04] Naliczenie zniżek z rang i zamknięcie rachunku |
|---|---|
| **Kto i gdzie** | System przy podsumowaniu rachunku |
| **Co robi** | System automatycznie odejmuje rabat wynikający z rangi gracza (np. -10%), sprawdza czy cały rachunek został pokryty (suma wpłat = kwota zamówień) i zamyka rachunek sesji. |
| **Kluczowe mechanizmy** | Transakcja w PostgreSQL sprawdzająca bilans płatności, zmiana statusu sesji finansowej na Closed. |
| **Wstępny MoSCoW** | **Must Have** - zamyka obieg pieniędzy w lokalu |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [BILL-05] Procedura ochrony przed ucieczką bez płacenia |
|---|---|
| **Kto i gdzie** | Barman na terminalu POS / Administrator |
| **Co robi** | Jeśli goście opuszczą lokal bez podejścia do kasy, barman klika „Zgłoś ucieczkę (Walkout)”. System blokuje konta graczy powiązanych z sesją, zapisuje kwotę długu i generuje alert przy jakiejkolwiek przyszłej próbie wejścia lub rezerwacji. |
| **Kluczowe mechanizmy** | Zmiana statusu konta na `SuspendedUnpaidDebt`, rejestr długu w bazie, alert na POS w przypadku zeskanowania kodu QR zablokowanego użytkownika (`[AUTH-08]`). |
| **Wstępny MoSCoW** | **Must Have** – kluczowe zabezpieczenie przed nieuczciwymi klientami. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

## 9. Panel menadżera, magazyn barku i raporty

| ID & Nazwa | [ADMIN-01] Zarządzanie menu gastro i cennikami (CRUD) |
|---|---|
| **Kto i gdzie** | Menadżer / Admin w panelu webowym |
| **Co robi** | Menadżer może dodawać nowe piwa kraftowe, edytować ceny, dodawać kategorie, modyfikatory oraz wgrywać zdjęcia pozycji menu. |
| **Kluczowe mechanizmy** | CRUD w ASP.NET Core z autoryzacją ról (Admin ma pełnego CRUD-a), relacyjna baza w PostgreSQL. |
| **Wstępny MoSCoW** | **Must Have** - bez tego nie da się wprowadzić oferty lokalu |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [ADMIN-02] Prosty magazyn barku |
|---|---|
| **Kto i gdzie** | Menadżer / Barman w panelu webowym |
| **Co robi** | Ewidencja sztukowa butelek piwa kraftowego na stanie. Sprzedaż piwa w aplikacji automatycznie zdejmuje 1 sztukę z magazynu. Gdy stan osiąga 0 sztuk, system sam wyłącza pozycję w menu gości. |
| **Kluczowe mechanizmy** | Atomowe odejmowanie stanu w transakcji PostgreSQL, automatyczny broadcast SignalR o wyprzedaniu produktu. |
| **Wstępny MoSCoW** | **Should Have** - bardzo przydatne żeby barman nie musiał biegać do gości że piwo się skończyło |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [ADMIN-03] Raport popularności gier i czasów rozgrywki |
|---|---|
| **Kto i gdzie** | Menadżer / Admin w panelu webowym |
| **Co robi** | Wykresy i zestawienia: które gry są najczęściej wypożyczane, jaki jest średni realny czas partii oraz lista "martwych gier" które nie były grane od ponad 60 dni. |
| **Kluczowe mechanizmy** | Zapytania agregujące SQL (COUNT, AVG, GROUP BY) z możliwością eksportu do pliku CSV. |
| **Wstępny MoSCoW** | **Should Have** - świetne dane dla właściciela lokalu co warto dokupić a co sprzedać |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [ADMIN-04] Raport finansowy lokalu i obrotu stolików |
|---|---|
| **Kto i gdzie** | Menadżer / Admin w panelu webowym |
| **Co robi** | Raport sprzedaży gastro i wejściówek z podziałem na dni, godziny szczytu oraz zestawienie które stoliki generują największy utarg. |
| **Kluczowe mechanizmy** | Zapytania analityczne w PostgreSQL, wizualizacja danych na prostych wykresach w React. |
| **Wstępny MoSCoW** | **Should Have** - standardowy panel analityczny lokalu |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [ADMIN-05] Zarządzanie pracownikami lokalu i rolami |
|---|---|
| **Kto i gdzie** | Admin w panelu webowym |
| **Co robi** | Administrator lokalu może tworzyć konta pracownicze, resetować im hasła i przydzielać role systemowe: Barman, Menadżer lub drugi Administrator. |
| **Kluczowe mechanizmy** | Przypisywanie ról w ASP.NET Core Identity / PostgreSQL, blokada dostępu do panelu dla zwykłych graczy. |
| **Wstępny MoSCoW** | **Must Have** - zarządzanie uprawnieniami załogi lokalu |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [ADMIN-06] Podgląd logów audytowych i historii operacji |
|---|---|
| **Kto i gdzie** | Admin w panelu webowym |
| **Co robi** | Administrator widzi rejestr kluczowych akcji w lokalu: kto skasował stolik, kto przeniósł grę do kwarantanny, kto anulował zamówienie z baru i o której godzinie. |
| **Kluczowe mechanizmy** |Rejestrowanie wrażliwych operacji personelu w dzienniku audytowym backendu (strukturalne logi zdarzeń z identyfikatorem pracownika i datą akcji). |
| **Wstępny MoSCoW** | **Could Have** - fajny smaczek pod bezpieczeństwo i audyt |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [ADMIN-07] Raport dobowy kasy i rozliczenie zmianowe barmana (Shift Closeout / Z-Report) |
|---|---|
| **Kto i gdzie** | Barman / Menadżer na koniec dnia na terminalu POS |
| **Co robi** | Generowanie podsumowania dobowego kasy: łączny obrót brutto ze sprzedaży gastro i wejściówek, podział na gotówkę i kartę, stan kasetki pieniężnej, odnotowane różnice oraz statystyki obsłużonych stolików. |
| **Kluczowe mechanizmy** | Zamykanie sesji rozliczeniowej w tabeli `CashRegisterShifts`, archiwizacja raportu dobowego w PostgreSQL. |
| **Wstępny MoSCoW** | **Should Have** - kluczowe rozliczenie finansowe na koniec dnia pracy lokalu |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [ADMIN-08] Masowe powiadomienia marketingowe |
|---|---|
| **Kto i gdzie** | Manager w panelu webowym |
| **Co robi** | Wysyłanie powiadomień Push do graczy o nadchodzących turniejach planszowych, premierach nowych gier na półce czy zmianach godzin otwarcia lokalu z opcją filtrowania odbiorców według rang. |
| **Kluczowe mechanizmy** | Komunikaty na żywo na ekranach sali przez SignalR oraz wysyłka powiadomień systemowych push na telefony graczy (integracja z Firebase FCM). |
| **Wstępny MoSCoW** | **Could Have** – Masowe powiadomienia marketingowe są opcjonalnym modułem promocyjnym. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [ADMIN-09] Kalendarz dni roboczych, godzin otwarcia i wyjątków świątecznych |
|---|---|
| **Kto i gdzie** | Administrator w panelu webowym |
| **Co robi** | Konfiguracja standardowych godzin otwarcia lokalu w poszczególne dni tygodnia oraz definiowanie dni wolnych/świąt. Moduł rezerwacji automatycznie blokuje możliwość składania rezerwacji poza godzinami pracy lokalu. |
| **Kluczowe mechanizmy** | Tabela harmonogramu `OperatingHours` w PostgreSQL, weryfikacja poprawności żądań rezerwacji w warstwie reguł biznesowych API. |
| **Wstępny MoSCoW** | **Must Have** – uniemożliwia rezerwowanie stolików gdy lokal jest zamknięty. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

## 10. Rezerwacje stolików, sal i wizyt

| ID & Nazwa | [RES-01] Rezerwacja stolika z wyprzedzeniem z kalendarza |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej |
| **Co robi** | Gracz wybiera datę, slot godzinowy (np. 18:00–22:00), preferowaną strefę sali oraz liczbę osób. System weryfikuje dostępność mebli i tworzy rezerwację z przypisanym numerem stolika. |
| **Kluczowe mechanizmy** | Silnik alokacji zasobów w ASP.NET Core, blokada double-bookingu w PostgreSQL (typy zakresowe `tsrange`), widok kalendarza w React Native. |
| **Wstępny MoSCoW** | **Must Have** – kluczowa realizacja tematu pracy inżynierskiej. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [RES-02] Harmonogram i oś czasu rezerwacji |
|---|---|
| **Kto i gdzie** | Barman / Manager w panelu webowym POS |
| **Co robi** | Interaktywny wykres Gantta dla wszystkich stolików lokalu: wizualizacja trwających sesji, nadchodzących rezerwacji, luk czasowych oraz buforów na sprzątanie. |
| **Kluczowe mechanizmy** | Komponent timeline w React 19, pobieranie rezerwacji z indeksowanych zapytań SQL, push updates przez SignalR. |
| **Wstępny MoSCoW** | **Must Have** – podstawowe narzędzie pracy personelu przy planowaniu obsadzenia sali. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [RES-03] Okienko tolerancji i automatyczne zwalnianie No-Show |
|---|---|
| **Kto i gdzie** | System w tle |
| **Co robi** | Jeśli rezerwacja nie zostanie rozpoczęta (przez NFC/QR stolika lub potwierdzenie barmana) w ciągu 15 minut od wyznaczonej godziny, system oznacza ją jako No-Show, zwalnia stolik do puli wolnych i powiadamia POS. |
| **Kluczowe mechanizmy** | Zadanie cykliczne w Quartz.NET odpytujące bazę co 60 sekund, przejście stanu na `CancelledNoShow`, rozgłoszenie eventu SignalR. |
| **Wstępny MoSCoW** | **Must Have** – odblokowuje stoliki dla gości oczekujących przy barze. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

## 11. Odporność offline i integracja sprzętowa

| ID & Nazwa | [EDGE-01] Buforowanie transakcji POS w trybie awaryjnym |
|---|---|
| **Kto i gdzie** | Barman na terminalu POS przy zaniku internetu |
| **Co robi** | Przy zerwaniu łącza internetowego terminal POS przechodzi w tryb offline: pozwala nadal nabijać zamówienia i pobierać płatności gotówkowe, buforując transakcje w lokalnej pamięci przeglądarki (IndexedDB). |
| **Kluczowe mechanizmy** | Biblioteka IndexedDB w React POS, kolejka synchronizacyjna wysyłająca zgromadzone transakcje z idempotencyjnymi kluczami UUID po powrocie internetu. |
| **Wstępny MoSCoW** | **Should Have** – bar nie może przestać funkcjonować w piątkowy wieczór przez awarię łącza internetowego, natomiast sam projekt bez tego da rade funkcjonować. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [EDGE-02] Awaryjna synchronizacja stanu sali po restarcie serwera |
|---|---|
| **Kto i gdzie** | Backend po restarcie lub awarii zasilania |
| **Co robi** | Po restarcie serwera system odtwarza stan wszystkich otwartych sesji, przypisanych gier i statusów zamówień z bazy danych, wznawia timery i rozsyła aktualny stan do podłączonych ekranów POS/KDS. |
| **Kluczowe mechanizmy** | Inicjalizator stanu w ASP.NET Core (`IHostedService`), audyt spójności danych przy starcie aplikacji. |
| **Wstępny MoSCoW** | **Must Have** – chroni przed utratą danych po chwilowym braku prądu. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">


## 12. Moduł funkcji społecznościowych, eventów i czatu (Social & Event Hub)

| ID & Nazwa | [SOC-01] Tworzenie i publikacja wydarzeń społecznościowych / turniejów |
|---|---|
| **Kto i gdzie** | Manager / Organizator w panelu webowym LUB zaufany gracz w aplikacji mobilnej |
| **Co robi** | Tworzy wydarzenie (np. turniej ligowy, noc premierowa, meetup tematyczny), określa datę, godzinę, limit uczestników, wpisowe, powiązaną grę z bazy BGG oraz reguły rozgrywek. Wydarzenie pojawia się w kalendarzu lokalu. |
| **Kluczowe mechanizmy** | Encja `Event` w PostgreSQL, powiązanie z `bggId`, walidacja harmonogramu z wolnymi stolikami, automatyczne rozgłoszenie powiadomienia o nowym evencie przez SignalR. |
| **Wstępny MoSCoW** | **Must Have** – fundament modułu społecznościowego i realizacji rozszerzonego tematu pracy inżynierskiej. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [SOC-02] Zapisy na wydarzenia z obsługą limitu miejsc i listy rezerwowej |
|---|---|
| **Kto i gdzie** | Gracz w aplikacji mobilnej |
| **Co robi** | Gracz zapisuje się na turniej lub wydarzenie jednym kliknięciem. Jeśli limit miejsc został osiągnięty, trafia na listę rezerwową (Waitlist). W przypadku rezygnacji innego gracza, system automatycznie promuje pierwszą osobę z listy rezerwowej i wysyła powiadomienie push. |
| **Kluczowe mechanizmy** | Transakcje w PostgreSQL z blokadą wierszy (`SELECT ... FOR UPDATE`), ochrona przed zjawiskiem Overbookingu (wyścig współbieżności), maszyna stanów rejestracji (`Confirmed`, `Waitlist`, `Cancelled`). |
| **Wstępny MoSCoW** | **Must Have** – rygor inżynierski transakcyjności i zarządzania miejscami w czasie rzeczywistym. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [SOC-03] Rejestracja wyników partii i protokół meczowy (Match History) |
|---|---|
| **Kto i gdzie** | Host stolika / Sędzia turnieju w aplikacji mobilnej lub panelu POS |
| **Co robi** | Po zakończeniu partii stolikowej lub rundy turnieju host wprowadza oficjalne wyniki: liczbę punktów graczy, czas trwania partii oraz wskazuje zwycięzcę. Wynik zostaje zatwierdzony przez współgraczy i trwale zapisany w historii partii lokalu. |
| **Kluczowe mechanizmy** | Encje `MatchSession` oraz `MatchScore` w PostgreSQL, powiązanie z egzemplarzem gry, automatyczne naliczenie punktów doświadczenia XP do Paszportu Gracza oraz aktualizacja pozycji w rankingach lokalu (Hall of Fame). |
| **Wstępny MoSCoW** | **Must Have** – kluczowy komponent grywalizacji i archiwizacji historii rozgrywek. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [SOC-04] Tablica wyników i rankingi społecznościowe (Leaderboards & Hall of Fame) |
|---|---|
| **Kto i gdzie** | Gracz w aplikacji mobilnej oraz ekran w lokalu (POS / TV Display) |
| **Co robi** | Prezentacja rankingów lokalu: najlepsi gracze w danym miesiącu, liderzy w poszczególnych kategoriach gier BGG (np. Gry Strategiczne, Gry Imprezowe), gracze z najwyższą liczbą wygranych turniejów. |
| **Kluczowe mechanizmy** | Indeksowane zapytania agregujące w PostgreSQL (widoki zmaterializowane `MATERIALIZED VIEW` odświeżane cyklicznie), cache'owanie w pamięci RAM, dedykowany ekran w aplikacji mobilnej. |
| **Wstępny MoSCoW** | **Should Have** – buduje zaangażowanie społeczności i zdrową rywalizację bywalców lokalu. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [SOC-05] Czat czasu rzeczywistego w ramach pokoju wydarzenia / turnieju |
|---|---|
| **Kto i gdzie** | Uczestnicy wydarzenia i organizator w aplikacji mobilnej |
| **Co robi** | Zapisani gracze mają dostęp do dedykowanego czatu wydarzenia, w którym mogą zadawać pytania organizatorowi, ustalać szczegóły logistyczne oraz odbierać komunikaty sędziowskie o kolejnych rundach turniejowych. |
| **Kluczowe mechanizmy** | Lekki SignalR Hub z obsługą grup (`event-{eventId}`), streaming WebSockets, persystencja wiadomości w tabeli `chat_messages` w PostgreSQL, pobieranie historii ostatnich 50 wiadomości przez REST API. |
| **Wstępny MoSCoW** | **Must Have** – bezpośrednia realizacja funkcji czatu na żywo w oparciu o protokół WebSockets. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [SOC-06] Czat stolika i komunikacja z obsługą baru (Table & Service Chat) |
|---|---|
| **Kto i gdzie** | Gracze przypisani do stolika oraz barman/kelner na ekranie KDS |
| **Co robi** | Gracze przy danym stoliku mogą wymieniać się wiadomościami oraz wysyłać szybkie prośby do obsługi lokalu (np. „prosimy o serwetki do stolika 4”, „pytanie o zasady gry”). Wiadomość pojawia się z dyskretnym powiadomieniem na ekranie baru. |
| **Kluczowe mechanizmy** | Lekki SignalR Hub z grupami (`table-{sessionId}`), powiadomienie na ekran baru, zapis wiadomości w tabeli `chat_messages` powiązanych z sesją stolika. |
| **Wstępny MoSCoW** | **Should Have** – podnosi komfort obsługi bez konieczności podchodzenia do baru. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [SOC-07] Tablica ogłoszeń LFG (Looking For Group – szukam ekipy do gry) |
|---|---|
| **Kto i gdzie** | Gracz w aplikacji mobilnej w lokalu lub planujący wizytę |
| **Co robi** | Gracz lub niekompletna ekipa przy stoliku wystawia publiczne ogłoszenie LFG (np. „Stolik 6: gramy w Terraformację Marsa, szukamy 2 graczy o poziomie średnim, start za 20 min”). Inni gracze przeglądający aplikację mogą zgłosić chęć dołączenia jednym przyciskiem. |
| **Kluczowe mechanizmy** | Status stolika `LookingForPlayers`, rozgłaszanie zmian na żywo przez SignalR, integracja z profilem gry BGG i poziomem złożoności (Weight). |
| **Wstępny MoSCoW** | **Should Have** – likwiduje barierę wejścia dla pojedynczych graczy i integruje społeczność planszówkową. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [SOC-08] Lista znajomych i powiadomienia o obecności w lokalu |
|---|---|
| **Kto i gdzie** | Gracz w aplikacji mobilnej |
| **Co robi** | Gracz może dodać innych użytkowników do listy znajomych (np. po wspólnej partii przy stoliku). Opcjonalnie otrzymuje powiadomienie, gdy jego znajomy melduje się w lokalu lub dołącza do otwartego turnieju. |
| **Kluczowe mechanizmy** | Relacja `Friendship` w PostgreSQL, rygorystyczne ustawienia prywatności RODO (użytkownik decyduje w profilu, czy jest widoczny dla znajomych), notyfikacje push / in-app. |
| **Wstępny MoSCoW** | **Could Have** – dodatek społecznościowy zwiększający retencję graczy w lokalu. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">
