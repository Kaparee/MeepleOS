# Usunięte funkcjonalności z projektu MeepleOS

**Autor:** Jakub Płocica  
**Status:** Wycięte z zakresu inżynierskiego / Przeniesione do Backlogu  
**Łączna liczba wyciętych funkcji:** 69  

Dokument zawiera pełną specyfikację funkcjonalności, które zostały odrzucone lub przeniesione poza zakres pracy inżynierskiej na etapie budowania matrycy MoSCoW. Pozwala to zachować zwartą, realistyczną architekturę systemu (100 kluczowych funkcji w głównym dokumencie) bez utraty wypracowanych pomysłów operacyjnych.

---

## 1. Moduł Rezerwacji (RES) – wycięte skomplikowane warianty

| ID & Nazwa | [RES-02] Pre-rezerwacja gry planszowej do stolika |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej podczas bookowania stolika |
| **Co robi** | Gracz rezerwując stolik może od razu odłożyć z biblioteki 1 konkretną grę. Egzemplarz zyskuje status `ReservedForBooking` i czeka przygotowany na stoliku lub odłożony za barem. |
| **Kluczowe mechanizmy** | Powiązanie encji `Booking` z `GameCopyId`, automatyczna blokada wypożyczenia tego egzemplarza na sali na 1/2h przed planowaną rezerwacją. |
| **Wstępny MoSCoW** | **Should Have** – gwarancja dla graczy, że wybrana gra nie zostanie zajęta tuż przed ich przyjściem. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [RES-03] Weryfikacja rezerwacji SMS i ochrona No-Show (Bar Check-in Window) |
|---|---|
| **Kto i gdzie** | System oraz Użytkownik w aplikacji mobilnej (100% bez bramek online) |
| **Co robi** | Zamiast przedpłat internetowych rezerwacja wymaga potwierdzenia numeru telefonu kodem SMS. Obowiązuje twarda zasada: stolik musi zostać odebrany w lokalu (skan NFC lub podejście do baru) w ciągu 15 minut od wyznaczonej godziny, w przeciwnym razie rezerwacja automatycznie wygasa. |
| **Kluczowe mechanizmy** | Integracja z bramką SMS (SMSAPI / Twilio) do wysyłki jednorazowego kodu weryfikacyjnego, cykliczne zadanie Quartz.NET anulujące niepotwierdzone rezerwacje. |
| **Wstępny MoSCoW** | **Must Have** – skuteczna ochrona przed pustymi rezerwacjami bez angażowania bramek płatniczych. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [RES-06] Wprowadzanie rezerwacji telefonicznej / Walk-in przez barmana |
|---|---|
| **Kto i gdzie** | Barman na terminalu POS |
| **Co robi** | Szybkie dodanie rezerwacji od gościa dzwoniącego lub wchodzącego z ulicy: podanie telefonu, nazwiska, liczby osób i wybór stolika z natychmiastowym sprawdzeniem kolizji. |
| **Kluczowe mechanizmy** | Formularz modalny w React POS z natychmiastową walidacją kolizji terminów w ASP.NET Core API. |
| **Wstępny MoSCoW** | **Must Have** – obsługa tradycyjnych kanałów kontaktu z lokalem. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [RES-07] Automatyczne przypomnienia Push/SMS o rezerwacji |
|---|---|
| **Kto i gdzie** | System wysyła do Użytkownika |
| **Co robi** | Na 3 godziny przed rezerwacją użytkownik otrzymuje powiadomienie Push i SMS z przypomnieniem o wizycie oraz przyciskiem szybkiego odwołania stolika, jeśli plany grupy uległy zmianie. |
| **Kluczowe mechanizmy** | Usługa w tle, integracja Firebase Cloud Messaging (FCM) oraz SMSAPI, jednorazowy token odwołania wizyty. |
| **Wstępny MoSCoW** | **Should Have** – drastycznie ogranicza odsetek zapomnianych rezerwacji. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [RES-08] Rezerwacja Pokoju RPG / Sali VIP na wyłączność |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej lub Barman na POS |
| **Co robi** | Rezerwacja wyciszonej sali tematycznej (np. Pokój RPG z klimatycznym oświetleniem) z minimalnym limitem rachunku gastronomicznego (Minimum Spend) rozliczanym fizycznie przy barze pod koniec wizyty. |
| **Kluczowe mechanizmy** | Oznaczenie strefy `ZoneType = PrivateVIPRoom`, reguła minimalnej kwoty rozliczeniowej sprawdzana na POS przy zamykaniu rachunku. |
| **Wstępny MoSCoW** | **Should Have** – kluczowa usługa w lokalach ze strefami gier fabularnych. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [RES-09] Link grupowy do rezerwacji (Social Booking Invite) |
|---|---|
| **Kto i gdzie** | Organizator rezerwacji w aplikacji mobilnej |
| **Co robi** | Po utworzeniu rezerwacji organizator klika „Zaproś znajomych” i generuje link do wysłania na Messengerze/WhatsAppie. Znajomi jednym kliknięciem potwierdzają obecność i widzą szczegóły spotkania. |
| **Kluczowe mechanizmy** | Unikalny token zaproszenia `InviteCode`, dynamiczny deep-link w React Native, aktualizacja listy uczestników w czasie rzeczywistym. |
| **Wstępny MoSCoW** | **Should Have** – ułatwia organizację wyjść grupowych. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [RES-10] Bufor techniczny na sprzątanie stolika (Turnaround Buffer) |
|---|---|
| **Kto i gdzie** | System automatycznie przy planowaniu slotów |
| **Co robi** | System automatycznie dolicza konfigurowalny bufor (np. 15 minut) po zakończeniu każdej rezerwacji, blokując nakładanie się rezerwacji i dając obsłudze czas na odkażenie blatu i ułożenie gier. |
| **Kluczowe mechanizmy** | Reguła biznesowa w algorytmie rezerwacyjnym dodająca interwał `CleaningBufferMinutes` do czasu zwolnienia stołu. |
| **Wstępny MoSCoW** | **Must Have** – eliminuje chaos i sytuacje, w których nowi goście czekają nad brudnym stolikiem. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

## 2. Moduł Animatorów i Mistrzów Gry (GM) – wycięty cały moduł

| ID & Nazwa | [GM-01] Cyfrowe wezwanie tłumacza reguł gry (Call Gamemaster) |
|---|---|
| **Kto i gdzie** | Gracze w aplikacji mobilnej przy stoliku |
| **Co robi** | Gdy ekipa utknie nad instrukcją, gracz klika „Poproś o wytłumaczenie zasad”. Wybiera grę, podaje problem (np. „Przygotowanie do gry”, „Wątpliwość w fazie walki”) i wysyła zgłoszenie do kolejki animatorów. |
| **Kluczowe mechanizmy** | Zdarzenie SignalR kierowane do grupy personelu `Group("Gamemasters")`, rejestracja zgłoszenia w bazie z czasem oczekiwania. |
| **Wstępny MoSCoW** | **Must Have** – fundamentalna wartość dodana pubu planszówkowego. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [GM-02] Panel kolejki wezwań animatora na tablecie sali |
|---|---|
| **Kto i gdzie** | Animator / Tłumacz gier na tablecie mobilnym |
| **Co robi** | Animator widzi listę stolików oczekujących na pomoc posortowaną według czasu zgłoszenia. Klika „Idę do stolika 4”, co zmienia kolor stolika na mapie i powiadamia graczy: „Animator Jakub idzie do Was”. |
| **Kluczowe mechanizmy** | Widok SPA React na tablecie, blokada przejęcia zgłoszenia przez innego animatora, powiadomienie push/SignalR do stolika. |
| **Wstępny MoSCoW** | **Must Have** – organizuje pracę personelu animacyjnego. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [GM-03] Pigułki wiedzy i mini-ściągi dla personelu (Staff Rules Cheatsheet) |
|---|---|
| **Kto i gdzie** | Animator / Barman w panelu POS / tabletu |
| **Co robi** | Szybki podgląd skrótu zasad dla danej gry: liczba kart startowych, warunki końca gry, najczęstsze błędy początkujących oraz schemat rozłożenia planszy, bez konieczności czytania 30-stronicowej instrukcji. |
| **Kluczowe mechanizmy** | Moduł bazy wiedzy w PostgreSQL powiązany z kartotekami gier, szybka wyszukiwarka w React. |
| **Wstępny MoSCoW** | **Should Have** – podnosi kompetencje personelu i skraca czas tłumaczenia reguł. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [GM-04] Ocena pomocy animatora (Feedback dla personelu) |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej po zakończonej asyście |
| **Co robi** | Po odejściu animatora gracze mogą ocenić jakość wytłumaczenia gry (1–5 gwiazdek). Napiwek dla animatora gracz może przekazać tradycyjnie na barze przy rozliczaniu całego rachunku. |
| **Kluczowe mechanizmy** | Tabela ocen `GamemasterRatings` w bazie, powiązanie z profilem pracownika. |
| **Wstępny MoSCoW** | **Could Have** – narzędzie weryfikacji jakości pracy animatorów. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [GM-05] Cyfrowe wezwanie obsługi do rozlanego napoju (Spill Alert) |
|---|---|
| **Kto i gdzie** | Gracz przy stoliku w aplikacji mobilnej |
| **Co robi** | Przycisk alarmowy: „Rozlany napój / wypadek przy stole”. Stolik natychmiast zaczyna pulsować na czerwono na ekranie POS z głośnym sygnałem audio, umożliwiając barmanowi podbiegnięcie z ręcznikami zanim gra ulegnie zniszczeniu. |
| **Kluczowe mechanizmy** | Priorytetowy komunikat WebSockets SignalR z flagą `HighUrgency`, wywołanie Web Audio API na wszystkich terminalach personelu. |
| **Wstępny MoSCoW** | **Must Have** – ratuje drogie gry planszowe przed zalaniem piwem. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [GM-06] Rejestr wypożyczonych rekwizytów sesji RPG (RPG Kit Inventory) |
|---|---|
| **Kto i gdzie** | Mistrz Gry / Barman na POS |
| **Co robi** | Przypisanie do stolika zestawu RPG: suchościeralnej battlematy, pisaków, zestawu kości wielościennych K20 i wieży do kości. Ewidencja wydania i zwrotu akcesoriów. |
| **Kluczowe mechanizmy** | Kartoteki zasobów nieseryjnych `SpecialtyInventory` powiązane z sesją stolika. |
| **Wstępny MoSCoW** | **Could Have** – wspiera społeczność fanów gier fabularnych. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

## 3. Moduł Wypożyczalni zewnętrznej do domu (RENT) – wycięty cały moduł

| ID & Nazwa | [RENT-01] Wypożyczenie gry na wynos do domu (Take-Home Rental) |
|---|---|
| **Kto i gdzie** | Barman na POS z udziałem Klienta |
| **Co robi** | Klient wypożycza fizyczną grę do domu (np. na weekend). System rejestruje termin zwrotu, dane najemcy, generuje umowę najmu i nalicza opłatę za dobę, opłacaną na barze przy wydaniu gry. |
| **Kluczowe mechanizmy** | Tabela `ExternalRentals` w PostgreSQL, wyliczanie opłat na podstawie taryfikatora doby, status egzemplarza `RentedOutside`. |
| **Wstępny MoSCoW** | **Should Have** – istotne źródło przychodów pubów planszówkowych. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [RENT-02] Pobranie i ewidencja kaucji zwrotnej na kasie POS |
|---|---|
| **Kto i gdzie** | Barman na terminalu POS przy ladzie |
| **Co robi** | Kaucja zwrotna za grę do domu jest pobierana fizycznie na kasie baru: w gotówce do kasetki lub kartą/BLIKiem na fizycznym terminalu EFT-POS. System rejestruje kwotę kaucji. Przy bezszkodowym zwrocie barman wypłaca gotówkę lub dokonuje zwrotu na terminalu płatniczym. |
| **Kluczowe mechanizmy** | Tabela `SecurityDeposits` z powiązaniem z transakcją kasy POS, audyt wydania i zwrotu kaucji przez pracownika. |
| **Wstępny MoSCoW** | **Must Have** – bezwzględne zabezpieczenie majątku lokalu bez konieczności integracji bramek online. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [RENT-03] Naliczanie kar za przetrzymanie gry po terminie zwrotu |
|---|---|
| **Kto i gdzie** | System automatycznie w tle |
| **Co robi** | Po przekroczeniu terminu zwrotu (np. poniedziałek 18:00) system nalicza opłatę karną za każdy rozpoczęty dzień zwłoki (np. 15 zł/dzień). Przy zwrocie kwota ta jest automatycznie potrącana z wpłaconej kaucji na barze. |
| **Kluczowe mechanizmy** | Harmonogram Quartz.NET kalkulujący spóźnienia, rozliczenie potrącenia z kaucji na ekranie zwrotu POS. |
| **Wstępny MoSCoW** | **Must Have** – dyscyplinuje pożyczających do terminowego oddawania pudełek. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [RENT-04] Inspekcja kompletności przy zwrocie z wynajmu zewnętrznego |
|---|---|
| **Kto i gdzie** | Barman / Serwisant na POS przy odbiorze |
| **Co robi** | Procedura kontrolna: pracownik sprawdza grę według cyfrowej checklisty komponentów (liczba kart, kafli, pionków). Po zatwierdzeniu kaucja zostaje zwrócona, a gra wraca na półkę. |
| **Kluczowe mechanizmy** | Formularz weryfikacji stanu fizycznego w React POS, log audytowy osoby przyjmującej zwrot. |
| **Wstępny MoSCoW** | **Must Have** – gwarantuje, że kolejny klient otrzyma kompletną grę. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [RENT-05] Karnet abonamentowy wypożyczalni opłacany na kasie POS |
|---|---|
| **Kto i gdzie** | Klient u Barmana na terminalu POS |
| **Co robi** | Klient kupuje 30-dniowy karnet wypożyczalni domowej bezpośrednio przy ladzie. Barman inkasuje opłatę (gotówka/terminal) i aktywuje na profilu gracza status abonamentowy (np. max 2 gry do domu jednocześnie bez opłat dobowych). |
| **Kluczowe mechanizmy** | Tabela uprawnień `UserSubscriptions` z datą ważności, weryfikacja uprawnień na POS przy rejestracji wypożyczenia. |
| **Wstępny MoSCoW** | **Could Have** – model lojalnościowy budujący stały recurring revenue w tradycyjny sposób. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [RENT-06] Rezerwacja gry na wynos z wyprzedzeniem |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej |
| **Co robi** | Gracz może zarezerwować konkretną grę na odbiór w piątek po południu, aby mieć pewność, że zabierze ją na weekendowy wyjazd za miasto. Opłatę i kaucję uiszcza fizycznie przy odbiorze w lokalu. |
| **Kluczowe mechanizmy** | Rezerwacja slotu wypożyczenia zewnętrznego w kalendarzu dostępności egzemplarza. |
| **Wstępny MoSCoW** | **Should Have** – popularna funkcjonalność przed weekendami i świętami. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

## 4. Moduł Tablicy kranów i multimediów TV (SIGN) – wycięty cały moduł

| ID & Nazwa | [SIGN-01] Cyfrowa Tablica Kranowa na TV (Digital Taplist Web View) |
|---|---|
| **Kto i gdzie** | Ekran TV powieszony nad barem (dedykowany widok Web) |
| **Co robi** | Wyświetlanie aktualnego menu piw z kranu: numer kranu (Tap 1..12), nazwa browaru, styl piwa, alk %, BLG, IBU, cena za 0.3L/0.5L oraz wizualny pasek pozostałej ilości w kegu. |
| **Kluczowe mechanizmy** | Dedykowany widok fullscreen w React 19 z auto-refresh i websocketami SignalR, reagujący natychmiast na zmianę podpiętego piwa. |
| **Wstępny MoSCoW** | **Must Have** – wizytówka i standard każdego lokalu kraftowego/barcade. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [SIGN-02] Podpinanie kega pod kran i monitoring litrażu |
|---|---|
| **Kto i gdzie** | Barman na terminalu POS |
| **Co robi** | Barman wybiera kran i przypisuje nowy keg z magazynu (np. Pinta - Atak Chmielu, 30L). Każde nalane piwo automatycznie odejmuje mililitry. Przy poziomie <5L barman dostaje alert: „Keg na kranie 3 bliski wyczerpania”. |
| **Kluczowe mechanizmy** | Tabela `ActiveTaps` powiązana z partią magazynową kegów, odejmowanie objętości porcji w transakcji PostgreSQL. |
| **Wstępny MoSCoW** | **Must Have** – precyzyjna kontrola sprzedaży alkoholu lanego. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [SIGN-03] Rejestr odpisów zlewkowych i czyszczenia instalacji piwnej |
|---|---|
| **Kto i gdzie** | Barman / Manager w panelu webowym |
| **Co robi** | Ewidencja strat technologicznych: zlewki piany przy zmianie kega, ubytki przy płukaniu linii oraz rejestracja okresowej sanityzacji instalacji (wymóg sanitarny). |
| **Kluczowe mechanizmy** | Tabela `BeerLineSanitizationLog`, odpisanie ubytków surowca bez generowania przychodu ze sprzedaży. |
| **Wstępny MoSCoW** | **Should Have** – gwarantuje czystość piwa i zgodność z bilansami magazynowymi. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [SIGN-04] Ekran przywoławczy gotowych zamówień gastro (Pickup Screen) |
|---|---|
| **Kto i gdzie** | Ekran TV w strefie odbioru przy barze |
| **Co robi** | Wyświetlanie dużych numerów zamówień: lewa kolumna „W przygotowaniu”, prawa kolumna „Gotowe do odbioru” z gongiem dźwiękowym przy pojawieniu się nowego numeru. |
| **Kluczowe mechanizmy** | Komponent Digital Signage zasilany kolejką zamówień z SignalR Hub, odtwarzanie dźwięku Web Audio API. |
| **Wstępny MoSCoW** | **Should Have** – zapobiega tłoczeniu się gości przy ladzie barowej. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [SIGN-05] Tablica wyników i ogłoszeń lokalu (Community TV Slideshow) |
|---|---|
| **Kto i gdzie** | Telewizor w sali głównej lokalu |
| **Co robi** | Rotacyjny pokaz slajdów: liderzy rankingu miesiąca, zapowiedzi czwartkowych turniejów, Gra Tygodnia oraz zdjęcia z ostatnich imprez. |
| **Kluczowe mechanizmy** | Karuzela slajdów w React zasilana danymi z CMS lokalu, automatyczne przełączanie slajdów co 15 sekund. |
| **Wstępny MoSCoW** | **Could Have** – buduje atmosferę lokalu i promuje bieżące wydarzenia. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [SIGN-06] Sterowanie klimatem i nagłośnieniem strefowym (Ambient Sound) |
|---|---|
| **Kto i gdzie** | Barman / Manager z panelu POS |
| **Co robi** | Szybkie przełączanie playlist audio (strefa głośna vs sala cicha) oraz regulacja poziomu głośności w poszczególnych strefach lokalu. |
| **Kluczowe mechanizmy** | Integracja z zewnętrznym API nagłośnienia przez webhooki w ASP.NET Core. |
| **Wstępny MoSCoW** | **Could Have** – smaczek podnoszący immersję w lokalu tematycznym. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

## 5. Moduł Sprzętu lokalu i integracji peryferyjnych (EDGE)

| ID & Nazwa | [EDGE-02] Obsługa czytników kodów kreskowych 1D/2D w trybie klawiaturowym (HID Wedge) |
|---|---|
| **Kto i gdzie** | Barman na POS / Magazynier |
| **Co robi** | Błyskawiczne skanowanie kodów kreskowych z butelek piwa lub etykiet QR z pudełek gier ręcznym czytnikiem USB działającym jako emulacja klawiatury (Keyboard Wedge), z automatycznym przechwytywaniem prefiksów. |
| **Kluczowe mechanizmy** | Globalny listener zdarzeń `keydown` w React z buforem czasowym (<50ms między znakami), rozpoznający wejście ze skanera bez konieczności klikania w pole tekstowe. |
| **Wstępny MoSCoW** | **Must Have** – przyspiesza pracę barmana kilkukrotnie. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [EDGE-03] Wskaźnik jakości sieci i statusu połączenia w aplikacji mobilnej |
|---|---|
| **Kto i gdzie** | Gracz w aplikacji mobilnej |
| **Co robi** | Gdy gracz schodzi do piwnicy lokalu ze słabym zasięgiem GSM, u góry ekranu pojawia się dyskretny pasek: „Brak połączenia z siecią lokalu – połącz się z darmowym Wi-Fi MeepleGuest”. |
| **Kluczowe mechanizmy** | Nasłuchiwanie stanu sieci `NetInfo` w React Native, automatyczne ponawianie zapytań HTTP (Exponential Backoff). |
| **Wstępny MoSCoW** | **Should Have** – zapobiega frustracji użytkowników w zabytkowych piwnicach. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [EDGE-04] Druk zamówień na boniarce kuchennej przez sieć LAN (ESC/POS Network Printing) |
|---|---|
| **Kto i gdzie** | System wysyła do drukarki w kuchni/barze |
| **Co robi** | Wysłanie sformatowanego bloczka zamówienia (numer stolika, godzina, pozycje, modyfikatory) bezpośrednio do drukarki termicznej w kuchni po lokalnym protokole sieciowym TCP (port 9100). |
| **Kluczowe mechanizmy** | Surowy strumień bajtów ESC/POS generowany w backendzie ASP.NET Core i wysyłany przez `TcpClient` na lokalny adres IP drukarki. |
| **Wstępny MoSCoW** | **Must Have** – kucharz w hałasie kuchni potrzebuje papierowego bonu. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [EDGE-05] Automatyczne wykrywanie serwera lokalnego w sieci LAN (Local mDNS) |
|---|---|
| **Kto i gdzie** | Aplikacja mobilna po podłączeniu do Wi-Fi lokalu |
| **Co robi** | Aplikacja automatycznie wykrywa lokalny serwer pubu za pomocą protokołu Zeroconf/mDNS, co drastycznie obniża opóźnienia i pozwala na funkcjonowanie systemu w lokalu nawet przy całkowitej awarii światłowodu. |
| **Kluczowe mechanizmy** | Usługa Zeroconf w React Native odpytująca domenę lokalną `meepleos.local`. |
| **Wstępny MoSCoW** | **Could Have** – najwyższa odporność infrastruktury sieciowej lokalu. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

## 6. Moduł Autoryzacji i personelu (AUTH)

| ID & Nazwa | [AUTH-12] Szybkie logowanie personelu kodem PIN / kartą RFID na POS |
|---|---|
| **Kto i gdzie** | Barman / Kelner przy terminalu POS |
| **Co robi** | Przy intensywnej pracy na barze pracownicy nie wpisują maila i hasła: zbliżają swoją opaskę/kartę RFID do czytnika USB lub wpisują 4-cyfrowy PIN, aby natychmiast odblokować kasę i nabić pozycję. |
| **Kluczowe mechanizmy** | Błyskawiczna zmiana kontekstu użytkownika przez WebHID API, weryfikacja hashowanego PINu w bazie bez przeładowania aplikacji React. |
| **Wstępny MoSCoW** | **Must Have** – bez tego obsługa baru w piątkowy wieczór ugrzęźnie w logowaniu. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [AUTH-13] Dwuetapowa weryfikacja (2FA / TOTP) dla panelu zarządczego |
|---|---|
| **Kto i gdzie** | Manager / Administrator w panelu webowym |
| **Co robi** | Logowanie do panelu administracyjnego wymaga podania 6-cyfrowego kodu z aplikacji uwierzytelniającej (Google Authenticator), zabezpieczając wrażliwe dane finansowe lokalu. |
| **Kluczowe mechanizmy** | Standard RFC 6238 TOTP w ASP.NET Core Identity. |
| **Wstępny MoSCoW** | **Should Have** – standard bezpieczeństwa aplikacji webowych. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [AUTH-14] Aktywacja konta cieniowego przez Magic Link (Claim Shadow Profile) |
|---|---|
| **Kto i gdzie** | Użytkownik posiadający profil Shadow po powrocie do domu |
| **Co robi** | Gracz, który podał przy stoliku tylko maila, otrzymuje wiadomość z linkiem Magic Link. Po kliknięciu zakłada hasło, a system automatycznie przenosi wszystkie punkty XP, odznaki i historię partii z tymczasowego konta na pełne konto. |
| **Kluczowe mechanizmy** | Kryptograficzny token z czasem ważności 72h, atomowa migracja relacji `ShadowUserId` -> `RegisteredUserId` w PostgreSQL. |
| **Wstępny MoSCoW** | **Must Have** – domyka koncepcję *Zero-Friction Shadow Profiles* opisaną w pracy dyplomowej. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [AUTH-16] Rejestracja czasu pracy personelu (RCP Clock-in / Clock-out) |
|---|---|
| **Kto i gdzie** | Pracownik lokalu przy terminalu POS |
| **Co robi** | Przyjście i wyjście z pracy rejestrowane zbliżeniem karty RFID do czytnika USB. System zlicza przepracowane godziny na zmianie i generuje miesięczny raport ewidencji czasu pracy. |
| **Kluczowe mechanizmy** | Tabela `StaffWorkTimeLogs` z dokładnymi timestampami wejścia/wyjścia. |
| **Wstępny MoSCoW** | **Should Have** – niezbędne narzędzie kadrowo-płacowe dla managera. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

## 7. Moduł Profilu i dietetyki (PROF)

| ID & Nazwa | [PROF-07] Preferencje dietetyczne i filtry alergenów w profilu |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej w profilu |
| **Co robi** | Gracz zaznacza preferencje żywieniowe (wegetarianizm, bez glutenu, uczulenie na orzechy). W cyfrowym menu pozycje z niedozwolonymi składnikami są automatycznie oznaczane wyraźnym ostrzeżeniem. |
| **Kluczowe mechanizmy** | Tabela preferencji w profilu, dynamiczne filtry w menu mobilnym. |
| **Wstępny MoSCoW** | **Should Have** – wygoda i bezpieczeństwo zdrowotne gości. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [PROF-08] Przedpłata / doładowanie salda gracza przy ladzie na barze |
|---|---|
| **Kto i gdzie** | Gracz u Barmana na terminalu POS |
| **Co robi** | Gracz może wpłacić gotówkę lub zapłacić kartą przy ladzie baru, aby doładować swoje saldo stałego bywalca. Przy kolejnych zamówieniach barman może jednym kliknięciem pobrać środki z przedpłaconego konta gracza. |
| **Kluczowe mechanizmy** | Tabela `UserAccountBalance` w PostgreSQL, księgowanie wpłat dokonywanych fizycznie na kasie POS. |
| **Wstępny MoSCoW** | **Should Have** – przyspiesza rozliczenia bez użycia jakichkolwiek bramek online. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [PROF-09] Centrum zgód marketingowych i retencji danych (RODO Dashboard) |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej |
| **Co robi** | Przejrzysty panel zarządzania zgodami: powiadomienia push o turniejach, profilowanie rekomendacji AI. Opcja pobrania wszystkich zebranych danych jednym kliknięciem. |
| **Kluczowe mechanizmy** | Rejestr zgód z wersjonowaniem, endpoint eksportu danych osobowych. |
| **Wstępny MoSCoW** | **Must Have** – bezwzględna zgodność z prawem unijnym (RODO). |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

## 8. Moduł Stolików (TAB)

| ID & Nazwa | [TAB-14] Potwierdzenie opuszczenia stolika i odznaczenie sprzątania |
|---|---|
| **Kto i gdzie** | Personel sprzątający / Kelner na POS lub smartfonie |
| **Co robi** | Po odejściu gości stolik świeci na czerwono (`NeedsCleaning`). Po przetarciu blatu i odłożeniu szklanek pracownik klika „Posprzątane”, co zmienia kolor stolika na zielony (`Available`). |
| **Kluczowe mechanizmy** | Zmiana stanu w maszynie stanów stolika, natychmiastowa aktualizacja rzutu sali przez SignalR. |
| **Wstępny MoSCoW** | **Must Have** – zapewnia higienę i porządek na sali. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

## 9. Moduł Gier planszowych, serwisu i akcesoriów (GAME)

| ID & Nazwa | [GAME-12] Kolejka oczekujących na zajętą grę (Waitlist & Push Alert) |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej |
| **Co robi** | Gdy wszystkie egzemplarze danej gry są wypożyczone, gracz klika „Powiadom mnie, gdy będzie wolna”. Gdy gra wróci do baru i przejdzie inspekcję, gracz dostaje powiadomienie Push z 10-minutową rezerwacją na odbiór. |
| **Kluczowe mechanizmy** | Kolejka FIFO w Redis / PostgreSQL dla danej gry, zdarzenie po zmianie statusu gry na `AvailableOnShelf`. |
| **Wstępny MoSCoW** | **Should Have** – wygoda dla graczy polujących na hitowe tytuły. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [GAME-13] Magazyn części zamiennych i kanibalizacja egzemplarzy |
|---|---|
| **Kto i gdzie** | Administrator / Serwisant w panelu webowym |
| **Co robi** | Ewidencja zapasowych klocków, kości i kart. Gdy gra z kwarantanny ma brakujący pionek, pracownik może odnotować pobranie części z magazynu części zamiennych lub ze „spisanego dawcy organów” (innego uszkodzonego pudełka). |
| **Kluczowe mechanizmy** | Tabela `GameSpareParts`, rejestracja przesunięć elementów między pudełkami w PostgreSQL. |
| **Wstępny MoSCoW** | **Should Have** – ratuje dziesiątki gier przed wyrzuceniem do kosza. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [GAME-14] Monitoring zużycia koszulek i komponentów (Sleeve & Wear Alert) |
|---|---|
| **Kto i gdzie** | System w panelu Managera |
| **Co robi** | Na podstawie licznika partii system automatycznie podświetla egzemplarze wymagające przeglądu: np. alert po 40 partiach „Wymień koszulki na karty” lub po 100 partiach „Sprawdź stan planszy”. |
| **Kluczowe mechanizmy** | Liczniki `PlayCount` w encji `GameCopy`, reguły alertów w ASP.NET Core z powiadomieniem w dashboardzie. |
| **Wstępny MoSCoW** | **Could Have** – prewencyjne utrzymanie wysokiej jakości gier. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [GAME-15] Naliczanie opłat karnych za zniszczenie lub zgubienie gry |
|---|---|
| **Kto i gdzie** | Barman na terminalu POS przy zwrocie gry |
| **Co robi** | Jeśli gra wraca zalana piwem lub z brakami bez wcześniejszego zgłoszenia Photo Evidence, barman wybiera z listy pozycję kary (np. „Zniszczenie kart – 30 zł”, „Odkupienie gry – 150 zł”). Kwota dolicza się do rachunku stolika rozliczanego przy kasie. |
| **Kluczowe mechanizmy** | Cennik szkód `DamageFeeCatalog`, dodanie pozycji do aktywnego rachunku sesji, powiązanie ze zdjęciem szkody w bazie. |
| **Wstępny MoSCoW** | **Must Have** – ochrona majątku lokalu przed niszczeniem gier. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [GAME-16] Limit jednoczesnych wypożyczeń na stolik |
|---|---|
| **Kto i gdzie** | System przy próbie wypożyczenia przez NFC/QR |
| **Co robi** | Konfiguracja lokalu narzuca limit aktywnych gier na stolik (np. max 1 duża gra lub 2 małe). Jeśli gracz spróbuje pobrać kolejne pudełko, system blokuje wypożyczenie: „Oddaj poprzednią grę do baru, aby wypożyczyć kolejną”. |
| **Kluczowe mechanizmy** | Walidator w ASP.NET Core sprawdzający liczbę aktywnych wypożyczeń dla danej sesji stolika przed akceptacją komendy `BorrowGameCommand`. |
| **Wstępny MoSCoW** | **Must Have** – zapobiega „chomikowaniu” 5 gier na jednym stole. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [GAME-18] Lokalizator półkowy i mapa regałów (Shelf Locator) |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej przy karcie gry |
| **Co robi** | Karta gry wskazuje dokładne położenie: np. „Regał B, Półka 3” oraz schemat regałów sali, dzięki czemu gość od razu wie, w które miejsce lokalu podejść po pudełko. |
| **Kluczowe mechanizmy** | Atrybuty `RackId`, `ShelfNumber` w encji egzemplarza, interaktywny schemat w aplikacji mobilnej. |
| **Wstępny MoSCoW** | **Should Have** – eliminuje błądzenie między regałami. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [GAME-19] Generator i masowy druk etykiet QR na pudełka |
|---|---|
| **Kto i gdzie** | Administrator w panelu webowym |
| **Co robi** | Manager wybiera gry z listy i klika „Drukuj etykiety”. System generuje plik PDF w standardzie etykiet samoprzylepnych z kodem QR, tytułem, ID egzemplarza i logiem lokalu. |
| **Kluczowe mechanizmy** | Generowanie PDF w ASP.NET Core (QuestPDF), wektorowe kody QR z UID egzemplarza. |
| **Wstępny MoSCoW** | **Must Have** – niezbędne narzędzie wdrożeniowe do oklejenia biblioteki gier. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [GAME-21] Cyfrowy regulamin i akceptacja odpowiedzialności materialnej |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej przed pierwszym wypożyczeniem |
| **Co robi** | Przy pierwszym wypożyczeniu gracz akceptuje skrócony regulamin wypożyczalni (odpowiedzialność za zalania, zakaz wynoszenia gier poza lokal, obowiązek zgłaszania braków). |
| **Kluczowe mechanizmy** | Zapis timestampu i wersji regulaminu `TermsAcceptedAt` w profilu użytkownika. |
| **Wstępny MoSCoW** | **Must Have** – podstawa prawna do ewentualnego obciążenia klienta za zniszczenia przy kasie. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [GAME-22] Wypożyczenie akcesoriów planszówkowych (Dice Trays, Wieże, Maty) |
|---|---|
| **Kto i gdzie** | Gracz w aplikacji mobilnej lub Barman na POS |
| **Co robi** | Możliwość dopisania do stolika akcesoriów: skórzanych tacek na kości, neoprenowych mat do kart czy wież do kości, również ewidencjonowanych tagami NFC/kodami. |
| **Kluczowe mechanizmy** | Kategoria zasobów `Accessories` w inwentarzu, przypisywanie do `TableSession`. |
| **Wstępny MoSCoW** | **Could Have** – podnosi kulturę i komfort gry. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [GAME-23] Pauza w partii / Przerwa na posiłek |
|---|---|
| **Kto i gdzie** | Gracze przy stoliku w aplikacji mobilnej |
| **Co robi** | Gracze mogą kliknąć „Pauza (idziemy zjeść / przerwa 15 min)”. Czas ten nie jest doliczany do czystego czasu partii, zapobiegając zafałszowaniu danych w modelu neuro-rozmytym ANFIS. |
| **Kluczowe mechanizmy** | Rejestracja okresów `SessionPauseInterval`, korekta czasu netto partii przesyłanego do mikroserwisu analitycznego w Pythonie. |
| **Wstępny MoSCoW** | **Should Have** – gwarantuje czystość danych badawczych dla modelu ANFIS. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [GAME-25] Waga kontrolna pudełka przy zwrocie (Weight-Check PoC) |
|---|---|
| **Kto i gdzie** | Barman na stanowisku inspekcji ze zintegrowaną wagą USB |
| **Co robi** | Przy zwrocie ciężkiej gry barman kładzie pudełko na wadze USB. System odczytuje masę z tolerancją +/- 5g i porównuje ze wzorcem w bazie: jeśli brakuje 50g żetonów, natychmiast zapala się ostrzeżenie. |
| **Kluczowe mechanizmy** | Odczyt wagi laboratoryjnej przez Web Serial API w Chrome POS, atrybut `StandardWeightGrams` w rekordzie gry. |
| **Wstępny MoSCoW** | **Could Have** – laboratoryjna innowacja inżynierska na najwyższym poziomie pracy dyplomowej. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [GAME-26] Blokada gier unikatowych i kaucja fizyczna (High-Value Games) |
|---|---|
| **Kto i gdzie** | Barman na terminalu POS przy wydawaniu gry |
| **Co robi** | Gry o wartości rynkowej >400 zł (unikaty z Kickstartera) są oznaczone statusem `HighValue`. Wypożyczenie wymaga fizycznego podejścia do lady, gdzie barman zatwierdza wydanie i pobiera kaucję zwrotną w gotówce lub na terminalu płatniczym. |
| **Kluczowe mechanizmy** | Flaga `RequiresDeposit` w kartotece gry, blokada self-checkoutu przez telefon dla gier z tej kategorii. |
| **Wstępny MoSCoW** | **Must Have** – ochrona przed zniszczeniem lub kradzieżą unikatów. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

## 10. Moduł Paszportu gracza i społeczności (PASS)

| ID & Nazwa | [PASS-12] Eksport partii do konta gracza na BoardGameGeek (BGG Play Logging Sync) |
|---|---|
| **Kto i gdzie** | Użytkownik w aplikacji mobilnej po partii |
| **Co robi** | Gracz klika „Zapisz na moim koncie BGG”. Aplikacja wysyła parametry partii (data, gra, gracze, wynik, czas trwania) bezpośrednio do oficjalnego profilu gracza na BGG przez BGG XML API2. |
| **Kluczowe mechanizmy** | Klient HTTP w ASP.NET Core integrujący się z API BGG przy użyciu zapisanego tokena/danych BGG użytkownika. |
| **Wstępny MoSCoW** | **Should Have** – marzenie każdego geeka planszówkowego. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

## 11. Moduł Gastronomii i Baru (ORDER)

| ID & Nazwa | [ORDER-07] Wielostanowiskowy routing zamówień (Bar KDS vs Kuchnia KDS) |
|---|---|
| **Kto i gdzie** | System w backendzie przy składaniu zamówienia ze stolika |
| **Co robi** | Jeśli zamówienie zawiera piwa kraftowe i zapiekanki, system automatycznie rozbija je na dwa niezależne bilety: napoje wpadają na ekran KDS barmana, a jedzenie na KDS kucharza (lub boniarkę termiczną w kuchni). |
| **Kluczowe mechanizmy** | Routing kategorii produktów w MediatR, selektywne grupy odbiorców SignalR (`Group("KDS_Bar")`, `Group("KDS_Kitchen")`). |
| **Wstępny MoSCoW** | **Must Have** – bez tego barman ma bałagan na ekranie, a kucharz nie wie, co ma smażyć. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [ORDER-09] Moduł napiwków na terminalu POS (Tipping Engine) |
|---|---|
| **Kto i gdzie** | Barman na terminalu POS przy rozliczaniu rachunku z Klientem |
| **Co robi** | Podczas zamykania rachunku przy ladzie barman pyta klienta o napiwek: na ekranie POS klika przycisk (+5 zł, +10 zł, 10% lub kwotę własną), co powiększa kwotę do zapłaty na terminalu bankowym / gotówką. |
| **Kluczowe mechanizmy** | Rozbicie kwoty transakcji na `Subtotal` i `TipAmount`, raportowanie napiwków per zmiana pracownicza. |
| **Wstępny MoSCoW** | **Should Have** – standard w gastronomii podnoszący motywację personelu. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

## 12. Moduł Rozliczeń, fiskalizacji i zaawansowanych płatności (BILL)

| ID & Nazwa | [BILL-06] Integracja z drukarką fiskalną i e-paragony |
|---|---|
| **Kto i gdzie** | Barman przy kasie POS / System w backendzie |
| **Co robi** | Po fizycznym opłaceniu rachunku przy ladzie system automatycznie wysyła komendę fiskalizacji do drukarki fiskalnej (protokół Posnet Thermal / Novitus) drukując papierowy paragon LUB generuje cyfrowy e-paragon wysyłany na e-mail klienta. |
| **Kluczowe mechanizmy** | Sterownik komunikacji sieciowej TCP/IP / COM z drukarką fiskalną w ASP.NET Core, generowanie rejestru fiskalnego w PostgreSQL. |
| **Wstępny MoSCoW** | **Must Have** – bez kasy fiskalnej żaden lokal w Polsce nie może legalnie działać. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [BILL-07] Wystawianie faktur VAT z automatycznym pobieraniem danych z GUS |
|---|---|
| **Kto i gdzie** | Barman na POS przy rozliczeniu z klientem |
| **Co robi** | Klient biznesowy podaje NIP przy ladzie. System w 1 sekundę pobiera nazwę i adres firmy z publicznego API GUS (Baza Internetowa REGON) i drukuje/wysyła fakturę VAT w PDF. |
| **Kluczowe mechanizmy** | Klient HTTP odpytujący API GUS w ASP.NET Core, generowanie szablonu faktury PDF (QuestPDF), wysyłka na e-mail. |
| **Wstępny MoSCoW** | **Should Have** – oszczędza czas barmana na ręczne wklepywanie danych firmowych. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [BILL-08] Płatności mieszane przy kasie (Split Payment Methods) |
|---|---|
| **Kto i gdzie** | Barman na terminalu POS |
| **Co robi** | Rozliczenie pojedynczego rachunku kilkoma metodami fizycznymi: np. rachunek na 120 zł płacony: 50 zł gotówką, 50 zł kartą na terminalu i 20 zł papierowym voucherem podarunkowym. System czuwa nad zbilansowaniem kwoty do 0 zł. |
| **Kluczowe mechanizmy** | Tabela transakcji cząstkowych `PaymentTransactions` powiązana z rachunkiem sesji, walidacja sumy wpłat w bazie przed zamknięciem rachunku. |
| **Wstępny MoSCoW** | **Must Have** – standardowa praktyka rozliczeń w gastronomii. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [BILL-09] Realizacja fizycznych voucherów i kodów rabatowych |
|---|---|
| **Kto i gdzie** | Barman na POS podczas zamykania rachunku |
| **Co robi** | Klient przekazuje barmanowi voucher podarunkowy lub kod zniżkowy. Barman skanuje czytnikiem kod kreskowy z bonu, a system pomniejsza rachunek stolika o wartość bonu. |
| **Kluczowe mechanizmy** | Tabela `Vouchers` z unikalnym kodem, datą ważności i blokadą wielokrotnego użycia w transakcji PostgreSQL. |
| **Wstępny MoSCoW** | **Should Have** – popularny produkt sprzedażowy pubów planszówkowych. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [BILL-10] Naliczanie opłat za wstęp i czas grania (Cover Charge / Time Fee) |
|---|---|
| **Kto i gdzie** | System automatycznie na rachunku sesji stolika |
| **Co robi** | Automatyczne naliczenie opłaty za strefę gier: stała wejściówka (np. 15 zł/osobę) LUB opłata za czas stolika (np. 10 zł/godz.), ewentualnie zasada „Wstęp darmowy przy zamówieniu gastro za min. 30 zł/os.”. Kwota trafia na końcowy rachunek rozliczany przy barze. |
| **Kluczowe mechanizmy** | Konfigurator reguł rozliczeniowych `BillingModelConfig` w ASP.NET Core, automatyczne kalkulowanie pozycji na rachunku w oparciu o czas trwania sesji i liczbę osób. |
| **Wstępny MoSCoW** | **Must Have** – fundament monetyzacji board game cafe. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [BILL-12] Sprzedaż gier planszowych i akcesoriów na wynos (Retail Shelf) |
|---|---|
| **Kto i gdzie** | Barman na terminalu POS |
| **Co robi** | Sprzedaż fabrycznie nowych gier w folii, koszulek na karty i gadżetów ze sklepowej półki lokalu. Barman skanuje kod EAN czytnikiem, a produkt dodaje się do paragonu ze stawką VAT 23%. |
| **Kluczowe mechanizmy** | Kartoteki artykułów sklepowych `RetailProducts`, integracja z magazynem i paragonem fiskalnym. |
| **Wstępny MoSCoW** | **Should Have** – istotne źródło przychodu w barcade. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [BILL-13] Integracja z Krajowym Systemem e-Faktur (KSeF 2.0) |
|---|---|
| **Kto i gdzie** | System w tle przy zatwierdzaniu faktur B2B przez barmana |
| **Co robi** | Automatyczne wysyłanie ustrukturyzowanych faktur VAT w formacie XML FA(2) do rządowej bramki KSeF z odbiorem unikalnego numeru KSeF i Urzędowego Poświadczenia Odbioru (UPO). |
| **Kluczowe mechanizmy** | Klient REST API KSeF w ASP.NET Core z uwierzytelnianiem tokenem autoryzacyjnym NIP / pieczęcią. |
| **Wstępny MoSCoW** | **Must Have** – bezwzględny wymóg prawny w polskim systemie podatkowym dla transakcji B2B. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [BILL-14] Integracja z terminalem płatniczym EFT-POS (Protokół ECR-EFT) |
|---|---|
| **Kto i gdzie** | Barman na terminalu POS przy płatności kartą / fizycznym BLIKiem |
| **Co robi** | Barman klika na ekranie „Karta / BLIK: 45,50 zł”. Terminal bankowy (np. Ingenico/Polcard) natychmiast wybudza się z właściwą kwotą bez ręcznego wpisywania groszy przez pracownika. Po zbliżeniu karty lub wpisaniu 6-cyfrowego kodu BLIK na terminalu kasa automatycznie rejestruje wpłatę. |
| **Kluczowe mechanizmy** | Komunikacja po protokole ECR (Ethernet/RS232) z terminalem bankowym w warstwie backendu. |
| **Wstępny MoSCoW** | **Must Have** – eliminuje pomyłki personelu w klepaniu kwot na terminalu. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [BILL-15] Kaucje zwrotne za szkło degustacyjne i dzbany (Glassware Deposit) |
|---|---|
| **Kto i gdzie** | Barman na POS przy kasowaniu piwa kraftowego |
| **Co robi** | Przy zamawianiu drogiego szkła degustacyjnego (pokale Teku) lub dzbanów z kranu system dolicza kaucję (np. 10 zł). Zwrot szkła na barze natychmiast odejmuje kaucję z rachunku lub barman wypłaca gotówkę. |
| **Kluczowe mechanizmy** | Pozycja kaucyjna `DepositItem` na rachunku stolika z osobną stawką rozliczeniową. |
| **Wstępny MoSCoW** | **Should Have** – chroni lokal przed plagą kradzieży markowego szkła kraftowego. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

## 13. Moduł Panelu menadżera, receptur BOM i zaawansowanych raportów (ADMIN)

| ID & Nazwa | [ADMIN-07] Magazyn surowców gastro z recepturami (BOM - Bill of Materials) |
|---|---|
| **Kto i gdzie** | Manager w panelu webowym |
| **Co robi** | Ewidencja surowców na gramy i mililitry (kawa ziarnista, mleko, syropy, kegi piwa 30L). Każda pozycja menu ma zdefiniowaną recepturę (np. Zapiekanka = 1 bagietka + 60g sera + 40g pieczarek). Sprzedaż dania automatycznie odpisuje surowce w ułamkach jednostek. |
| **Kluczowe mechanizmy** | Model receptur BOM w PostgreSQL, automatyczne odejmowanie stanów surowców w transakcji zamówienia. |
| **Wstępny MoSCoW** | **Must Have** – fundament kontroli kosztów i strat (Food Cost) w gastronomii. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [ADMIN-08] Dokumenty przyjęcia towaru PZ i kontrola dostawców |
|---|---|
| **Kto i gdzie** | Manager / Barman w panelu webowym |
| **Co robi** | Wprowadzanie dostaw towarów do lokalu (dokument PZ): wybór dostawcy, numer faktury, wpisanie ilości i cen hurtowych. System aktualizuje stany magazynowe i przelicza średnią cenę zakupu. |
| **Kluczowe mechanizmy** | Tabela dokumentów magazynowych `WarehouseReceiptPZ` powiązana z kartotekami towarów w PostgreSQL. |
| **Wstępny MoSCoW** | **Must Have** – ewidencja skąd biorą się towary na stanie baru. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [ADMIN-09] Szybka inwentaryzacja RFID/kreskowa gier i magazynu gastro |
|---|---|
| **Kto i gdzie** | Pracownik z czytnikiem USB lub telefonem w trybie inwentaryzacji |
| **Co robi** | Tryb masowego skanowania: pracownik chodzi wzdłuż regałów i przykłada czytnik do pudełek gier. System w czasie rzeczywistym odznacza obecne gry i wyświetla listę brakujących pudełek („Rozbieżności inwentaryzacyjne”). |
| **Kluczowe mechanizmy** | Zestawienie skanowanych tagów UID w pamięci podręcznej, różnicowe porównanie ze stanem ewidencyjnym w bazie, raport nadwyżek i niedoborów. |
| **Wstępny MoSCoW** | **Must Have** – skraca czas comiesięcznego liczenia 500 gier z 8 godzin do 30 minut. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [ADMIN-10] Raport dobowy kasy i rozliczenie zmianowe personelu (Shift Closeout) |
|---|---|
| **Kto i gdzie** | Barman / Manager na zakończenie zmiany |
| **Co robi** | Procedura zamknięcia zmiany: barman przelicza fizyczny stan gotówki w kasetce i drukuje podsumowanie z terminala płatniczego EFT-POS. System porównuje to ze sprzedażą systemową, generuje raport różnic (manko/superata) i drukuje dobowy raport fiskalny (Raport Z). |
| **Kluczowe mechanizmy** | Tabela `WorkShifts` z polami `CashStart`, `CashEnd`, `CashSystem`, `CardSystem`, generowanie protokołu zamknięcia zmiany w PDF. |
| **Wstępny MoSCoW** | **Must Have** – bez rozliczenia kasy żaden lokal nie utrzyma dyscypliny finansowej. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [ADMIN-14] Eksport księgowo-podatkowy (JPK / CSV Accounting Export) |
|---|---|
| **Kto i gdzie** | Manager / Księgowość w panelu webowym |
| **Co robi** | Generowanie zestawień sprzedaży, stawek VAT, raportu zamknięć fiskalnych i faktur do formatu CSV/Excel zgodnego z programami księgowymi (np. Comarch Optima, Symfonia) lub pliku JPK_FA. |
| **Kluczowe mechanizmy** | Generator raportów w ASP.NET Core z podziałem na stawki VAT (0%, 5%, 8%, 23%). |
| **Wstępny MoSCoW** | **Should Have** – oszczędza godziny ręcznej pracy przy rozliczeniach z biurem rachunkowym. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [ADMIN-15] Rejestr ubytków i strat (Waste & Spoilage Log) |
|---|---|
| **Kto i gdzie** | Barman / Kucharz / Manager w panelu |
| **Co robi** | Odpisanie surowców i produktów, które uległy zepsuciu, stłuczeniu lub wylaniu (np. rozbita butelka rzemieślniczego piwa, przeterminowane mleko, ubytki przy czyszczeniu linii piwnej). |
| **Kluczowe mechanizmy** | Dokument magazynowy RW (Rozchód Wewnętrzny) ze wskazaniem przyczyny straty, aktualizacja wskaźnika Strat Magazynowych w raporcie finansowym. |
| **Wstępny MoSCoW** | **Should Have** – gwarantuje zgodność stanu ewidencyjnego z fizycznym. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [ADMIN-16] Grafik pracy i planowanie obsady zmian (Staff Scheduler) |
|---|---|
| **Kto i gdzie** | Manager w panelu webowym |
| **Co robi** | Tworzenie tygodniowego grafiku pracy dla barmanów, kucharzy i animatorów. Pracownicy widzą swój grafik w aplikacji, mogą zgłaszać dyspozycyjność lub prośby o zamianę zmian. |
| **Kluczowe mechanizmy** | Moduł kalendarza zmian w React 19 z walidacją norm dobowych odpoczynku Kodeksu Pracy. |
| **Wstępny MoSCoW** | **Should Have** – ułatwia zarządzanie kilkunastoosobowym zespołem lokalu. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

| ID & Nazwa | [ADMIN-17] Kalkulator Food Cost i rentowności pozycji menu |
|---|---|
| **Kto i gdzie** | Manager w panelu webowym |
| **Co robi** | System zestawia koszt zakupu składników z receptury BOM z ceną sprzedaży brutto i automatycznie wylicza marżę procentową oraz wskaźnik Food Cost % dla każdej pozycji w karcie, sugerując korektę cen przy podwyżkach u dostawców. |
| **Kluczowe mechanizmy** | Algorytm analityczny w ASP.NET Core z uwzględnieniem podatku VAT i średniej ważonej ceny zakupu surowców. |
| **Wstępny MoSCoW** | **Should Have** – chroni lokal przed nieopłacalną sprzedażą. |

<hr style="height: 3px; background-color: #555555; border: none; margin: 40px 0;">

