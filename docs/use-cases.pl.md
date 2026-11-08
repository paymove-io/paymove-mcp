# Oferty partnera na MCP Paymove — przewodnik po przypadkach

> **Narzędzia na żywo: 20. Narzędzia planowane: 11, status Planned / Planowane.** Sekwencje poniżej mieszają jedne i drugie. Krok oznaczony **Na żywo** jest dziś w `tools/list`. Krok oznaczony **Planowane** jest opisany w [tools.md](./tools.md#planned-tools) i nie wolno go wywołać, dopóki ta nazwa nie pojawi się w `tools/list`. Wersja angielska: [use-cases.md](./use-cases.md).

Nowy produkt partnera jest zawsze typu `PAY`, `GO` albo `PARKING`. KYC kończy człowiek w [panel.paymove.io](https://panel.paymove.io). Żadne narzędzie z tego przewodnika nie wysyła KYC. Żadna nazwa poniżej nie jest prawdziwą firmą.

Kwoty są liczbami całkowitymi w groszach. `8000` oznacza 80,00 PLN. Autoryzacja to nagłówek `X-API-KEY`. Wywołania sandbox dokładają `X-SANDBOX-API-KEY` (`sk_test_...`).

## Wybór typu produktu

| Partner chce | Typ | Tworzenie (na żywo) | Dalej |
| :--- | :--- | :--- | :--- |
| Bilety na wydarzenie, warsztat, wejście o określonej godzinie z limitem miejsc | `GO` | `go-create-product`, `go-add-ticket-option` | **Planowane** `set-availability` na `entryId` biletu, gdy sesja ma liczbę miejsc. Webhook i widoczność. |
| Strefę parkowania i jej taryfę | `PARKING` | `parking-create-product` | **Planowane** `parking-update-pricing` do późniejszej edycji taryfy bazowej. `parking-create-event` (na żywo) dla czasowego nadpisania. Bez slotów. |
| Usługę bez daty (opłata, pakiet, jednorazowe zlecenie) | `PAY` | `create-pay-product`, `add-pay-pricing-entry` | Bez dostępności. Checkout ze śledzeniem zamówienia: na żywo `create-subproduct`. |
| Terminarz (fryzjer, wizyta, usługa zajmująca osobę i godzinę) | `PAY` | `create-pay-product` z `price: 0`, potem jeden `add-pay-pricing-entry` na usługę | **Planowane** `set-availability` na tej pozycji. **Planowane** `create-reservation` trzyma miejsce i zwraca adres checkoutu. |

Nie dodawaj typu produktu. Nie wołaj drugiego narzędzia tworzącego produkt dla wizyt ani dla usług. `create-pay-product` jest narzędziem tworzącym dla obu.

## Co zebrać na początku

Zapytaj raz i zatrzymaj się do odpowiedzi partnera:

1. Środowisko: sandbox (`sk_test_...`) albo produkcja (`sk_live_...`).
2. `X-API-KEY` z panelu. Nie wymyślaj klucza.
3. `partnerId`, gdy trzeba utworzyć produkt albo webhook. Nadaje go Paymove. Żadne API go nie zwraca.
4. Nazwa sklepu albo miejsca, miasto i strefa czasowa. Proponuj `Europe/Warsaw`.
5. Który wiersz tabeli powyżej pasuje do oferty.
6. Dla każdej pozycji sprzedaży: nazwa i cena w groszach.
7. Dla biletów i wizyt: sesje (`start`, `end`, `capacity`, opcjonalny `resource`).
8. Publiczny adres `https` webhooka, jeśli partner chce powiadomienia o płatności. Proponuj `retries: 3` i `expectedCode: 200`.

`signingSecret` wraca z rejestracji webhooka. Zapisz go. Zweryfikuj `X-Paymove-Signature` przed realizacją. Realizuj wyłącznie przy `COMPLETED`. Wejście na `returnUrl` nie jest płatnością.

## 1. Bilety — `GO`

**Wymyślone miejsce:** Festiwal Światła nad Odrą, Wrocław. Dwa warianty. Seans wieczorny 20 listopada 2026 ma 120 miejsc w wariancie pełnopłatnym.

| Krok | Narzędzie | Status | Co się dzieje |
| :--- | :--- | :--- | :--- |
| 1 | `go-create-product` | Na żywo | `name` / `fullName`: `Festiwal Światła nad Odrą`. `location`: `Wrocław`. `shortName`: `festiwal-swiatla-nad-odra`. Zapisz `productId`. |
| 2 | `go-add-ticket-option` | Na żywo | `title`: `Bilet normalny`, `price`: `4500` (45,00 PLN). Zapisz `entryId`. Powtórz dla `Bilet ulgowy` z ceną `3000`. |
| 3 | `set-availability` | Planowane | `targetType`: `GO_TICKET`, ten `entryId`, jeden slot `2026-11-20T18:00:00`–`2026-11-20T21:00:00`, `capacity`: `120`, `timezone`: `Europe/Warsaw`. |
| 4 | `register-webhook`, potem `assign-webhook-to-product` | Planowane (REST działa dziś) | Zarejestruj, zapisz `signingSecret`, przypisz do tego `productId`. |
| 5 | `set-product-visibility` | Planowane | `visibility`: `public`, gdy cennik jest gotowy. Wpis w wyszukiwarce i tak wymaga `ACTIVE` i KYC. |
| 6 | `search-public-products` | Na żywo | Agent kupującego znajduje festiwal po nazwie albo `location`. |
| 7 | `list-availability` | Planowane, odczyt publiczny | Zwraca `remaining` na wieczór. Bez klucza API, gdy produkt jest wyszukiwalny. |
| 8 | `create-reservation` | Planowane | `quantity`: `2`, `externalId`: `FEST-2001`, `returnUrl`: adres https partnera. Bez `price`. Odpowiedź: `status` `HELD`, `price` `9000`, `redirectUrl`. |
| 9 | Klient płaci na `redirectUrl` | Checkout na żywo | Partner nie oznacza zamówienia jako opłaconego na `returnUrl`. |
| 10 | Webhook `COMPLETED` | Dostawa na żywo, gdy webhook już istnieje | Zweryfikuj podpis. `get-reservation` pokazuje wtedy `confirmed: true`. Bilety wydaj w tej obsłudze, idempotentnie. |

Ładunki: [examples/planned/event-tickets.json](../examples/planned/event-tickets.json).

Dwóch kupujących na ostatnie miejsca: jedno `create-reservation` zwraca `HELD`, drugie `409` `SLOT_FULL`. Ten sam `externalId` wysłany ponownie zwraca pierwotne `reservationId` i nie zabiera kolejnych miejsc.

## 2. Parking — `PARKING`

**Wymyślona strefa:** Parking Bulwar Przykładowy, Toruń. Taryfa za czas postoju, nie kalendarz slotów.

| Krok | Narzędzie | Status | Co się dzieje |
| :--- | :--- | :--- | :--- |
| 1 | `parking-create-product` | Na żywo | `name`: `Parking Bulwar Przykładowy`. `shortName`: `parking-bulwar-przykladowy`. `location`: `Toruń, bulwar Przykładowy 1`. `timezone`: `Europe/Warsaw`. `entriesJson` w mapie kanonicznej: 30 minut za `200` groszy, potem `500` groszy za godzinę, ostatni próg `repeatable: true`. |
| 2 | `parking-get-pricing` | Na żywo | Odczytaj zapisaną taryfę przed edycją. |
| 3 | `parking-update-pricing` | Planowane | Wyślij całą mapę kanoniczną jeszcze raz, z nowymi `cost`. Skrócona tablica jest odrzucana. Nadpisania wydarzeń zostają. |
| 4 | `parking-create-event` | Na żywo | Sobotnia stawka ryczałtowa, `fixedCost` w groszach, `type`: `EVENT`. To czasowe nadpisanie, nie edycja taryfy bazowej. |
| 5 | `set-product-visibility` | Planowane | `public`, gdy strefa ma się pojawić w wyszukiwarce. |

Nie podpinaj `set-availability` pod parking. Postój jest czasem, a cenę liczy taryfa.

Ładunki: [examples/planned/parking-tariff.json](../examples/planned/parking-tariff.json).

## 3. Usługa bez daty — `PAY`

**Wymyślony punkt:** Biuro Przekładu Lipowa, Poznań. Klient płaci za stronę tłumaczenia. Nie ma slotu ani osoby do rezerwacji.

| Krok | Narzędzie | Status | Co się dzieje |
| :--- | :--- | :--- | :--- |
| 1 | `create-pay-product` | Na żywo | `name`: `Biuro Przekładu Lipowa`. `price`: `0`, więc kontener nie ma jednej ceny. `location`: `Poznań`. |
| 2 | `add-pay-pricing-entry` | Na żywo | `price`: `6000` (60,00 PLN), `description`: `Tłumaczenie — jedna strona`. Zapisz `entryId`. Kolejne pozycje dodaj, gdy jest usługa ekspresowa. |
| 3 | `create-subproduct` | Na żywo | Gdy zamówienie potrzebuje `externalId`: `amount` to cena pozycji razy liczba stron, policzona na serwerze partnera, z ustawionym `returnUrl`. Klient płaci na `redirectUrl`. |
| 4 | Webhook | MCP planowane, REST na żywo | Przypisz webhook. Zlecenie tłumaczenia realizuj dopiero po zweryfikowanym `COMPLETED`. |
| 5 | `set-product-visibility` | Planowane | `public`, jeśli link płatniczy ma być w katalogu. `hidden`, jeśli mają istnieć tylko zamówienia bezpośrednie. |

Pomiń `set-availability` i `create-reservation`. Przy usłudze bez godziny nie ma czego sprzedać drugi raz na zegarze.

Ładunki: [examples/planned/undated-service.json](../examples/planned/undated-service.json).

## 4. Fryzjer — `PAY` i sloty

**Wymyślony salon:** Atelier Nici, Sopot. Usługa: strzyżenie damskie, 30 minut, `8000` groszy. Etykieta stanowiska: `stylist-a`. To napis wybrany przez partnera, nie zweryfikowana tożsamość.

| Krok | Narzędzie | Status | Co się dzieje |
| :--- | :--- | :--- | :--- |
| 1 | `list-partner-products` | Na żywo | `productType`: `PAY`. Użyj istniejącego produktu, gdy już pasuje. |
| 2 | `create-pay-product` | Na żywo | Tylko gdy żadnego nie ma. `name`: `Atelier Nici`. `price`: `0`. `location`: `Sopot`. |
| 3 | `add-pay-pricing-entry` | Na żywo | `description`: `Strzyżenie damskie 30 min`, `price`: `8000`. Zapisz `entryId`. |
| 4 | `set-availability` | Planowane | `targetType`: `PAY_ENTRY`. Sloty `10:00–10:30` i `10:30–11:00` dnia `2026-11-20`, `capacity`: `1`, `resource`: `stylist-a`, `timezone`: `Europe/Warsaw`. |
| 5 | `register-webhook` + `assign-webhook-to-product` | Planowane (REST na żywo) | Salon potrzebuje tego przed otwarciem terminarza. Potwierdzeniem jest webhook. |
| 6 | `set-product-visibility` | Planowane | `public`, żeby `search-public-products` mogło zwrócić salon po KYC. |
| 7 | `list-availability` | Planowane | Kupujący widzi `remaining: 1` o `10:00`. |
| 8 | `create-reservation` | Planowane | `externalId`: `APT-1001`, `quantity`: `1`, ustawiony `returnUrl`, bez pola ceny. Odpowiedź: `price` `8000`, `status` `HELD`, `ttlSeconds` `600`, `redirectUrl`. |
| 9 | Płatność | Checkout na żywo | Klient płaci przed `expiresAt`. |
| 10 | Webhook `COMPLETED` | Dostawa na żywo | Salon zapisuje wizytę we własnym kalendarzu w obsłudze ze sprawdzonym podpisem. `get-reservation` pokazuje `confirmed: true`. |

`cancel-reservation` przy statusie `HELD` oddaje miejsce. Nie zwraca pieniędzy za wizytę `COMPLETED`. Drugi klient proszący o `stylist-a` o `10:00` po założeniu holdu dostaje `409` `SLOT_FULL`. Nachodzący slot `stylist-a` na innej usłudze tego samego produktu to `409` `SLOT_OVERLAP` już przy `set-availability`.

Ładunki: [examples/planned/hairdresser.json](../examples/planned/hairdresser.json).

## 5. Wizyta — `PAY` i sloty

**Wymyślona praktyka:** Przychodnia na Lipowej, Lublin. Wizyta 20 minut za `12000` groszy (120,00 PLN). Etykieta zasobu: `room-1`. To przykład rezerwacji. To nie jest porada medyczna i nie zakłada karty pacjenta.

Sekwencja narzędzi jest taka jak u fryzjera, ze zmienionym opisem:

- Nazwa produktu `Przychodnia na Lipowej`, `location` `Lublin`, `price` `0` na kontenerze.
- Pozycja cennika `Wizyta 20 min`, `price` `12000`.
- Sloty po 20 minut, `capacity` `1`, `resource` `room-1`.
- `externalId` `VIS-3001`.
- Ten sam hold, ta sama cena liczona po stronie serwera, ta sama zasada: wizyta jest potwierdzona dopiero po webhooku płatności `COMPLETED`.

Ładunki: [examples/planned/visit.json](../examples/planned/visit.json).

## Zasady wspólne dla każdej rezerwowanej oferty

- Wywołujący nie wysyła ceny rezerwacji. Serwer kopiuje ją z pozycji cennika albo biletu.
- `externalId` jest kluczem idempotencji. Jeden identyfikator, jeden hold.
- Domyślna długość holdu w tym szkicu to 600 sekund. Miejsca nie da się sprzedać drugi raz, gdy hold jest `HELD` albo rezerwacja jest `COMPLETED`.
- `HELD` nie jest potwierdzeniem. `returnUrl` nie jest potwierdzeniem. Potwierdzeniem jest `COMPLETED` na webhooku płatności po weryfikacji podpisu.
- Zarejestruj webhook i przypisz go do produktu, inaczej system partnera nie dowie się o tym potwierdzeniu. REST potrafi to dziś. Narzędzia MCP `register-webhook` i `assign-webhook-to-product` nie, dopóki nie ma ich na liście.
- `search-public-products`, gdy widoczność wejdzie na serwer, ma zwracać wyłącznie produkty `ACTIVE` z widocznością `public`, których partner skończył KYC. Ukryte produkty zostają w narzędziach partnera.

## Pytania otwarte do właściciela produktu

Są celowo nierozstrzygnięte. Szkic podaje wartość proponowaną, żeby było co recenzować.

| Temat | Propozycja w tym szkicu | Pytanie |
| :--- | :--- | :--- |
| Domyślne TTL | `600` sekund. Wywołujący może podać `60`–`900`. | Jakie jest domyślne TTL i czy partner może je zmienić? |
| Spóźniona płatność | Płatność `COMPLETED` po `EXPIRED` nie potwierdza miejsca. | Kto zwraca tę płatność i jaki jest okres karencji? |
| Anulowanie | `cancel-reservation` zwalnia tylko miejsce `HELD`. `COMPLETED` zwraca `409` i nie uruchamia zwrotu. | Jakie jest okno anulowania i czy zwrot oddaje miejsce? |
| Kto potwierdza | Serwer ustawia `COMPLETED` z płatności. Partner realizuje zamówienie w obsłudze webhooka. Nie ma narzędzia ręcznego potwierdzenia. | Czy partner albo osoba z personelu ma potwierdzać dodatkowo? |
| Limity | Nieustalone. | Maks. slotów na wywołanie, maks. dni do przodu, maks. `capacity`, limity holdów, limity częstości. |
| `type` webhooka | Przykład używa `PAYMENT`. Aktualny REST oznacza ten typ jako wycofywany na rzecz `TRANSACTION`. | Który typ ma wysyłać MCP? |
| Cena zero | `PRICE_NOT_FIXED`, bez holdu. | Jak działa bilet bezpłatny z limitem miejsc? |
| Kto rezerwuje | `create-reservation` wymaga klucza partnera. | Czy publiczny agent ma móc założyć hold na wyszukiwalnym slocie? |
| Widoczność nowego produktu | Narzędzia tworzące na żywo jej nie zmieniają. | Gdy flaga powstanie, czy nowe produkty startują jako `hidden`? |
| Zakres zasobu | Etykieta zasobu jest unikalna w produkcie, także między pozycjami. | Czy ta sama etykieta ma blokować sloty między dwoma produktami jednego partnera? |
| `retries: 0` | Szkic MCP wymaga `retries` ≥ 1. REST pozwala na `0`. | Czy MCP ma pozwalać na webhook bez ponowień? |
