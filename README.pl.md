# Paymove MCP Server (`paymove-mcp-server`)

[![MCP Protocol](https://img.shields.io/badge/MCP-Streamable_HTTP-0066FF)](https://modelcontextprotocol.io)
[![MIP 245/2024](https://img.shields.io/badge/Regulacje-MIP_245%2F2024-00A86B)](https://paymove.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Włącz płatności jednym zdaniem.**

Oficjalna dokumentacja i szablony konfiguracji serwera [Model Context Protocol (MCP)](https://modelcontextprotocol.io) dla **[Paymove](https://paymove.io)** — infrastruktury płatniczej AI-first dla e-commerce, usług cyfrowych, sprzedaży biletów (Pay&Go), mobilności i parkingów.

**[English Documentation (README.md)](./README.md)** | **[Pełna referencja 20 narzędzi (docs/tools.md)](./docs/tools.md)** | **[Manifest MCP Registry (server.json)](./server.json)**

---

## Czym jest Paymove i serwer Paymove MCP?

**Paymove** (`paymove.io`) to polska bramka płatnicza i infrastruktura commerce, która pozwala firmom, platformom SaaS oraz agentom AI uruchamiać strony płatności, linki płatnicze, bilety cyfrowe oraz strefy parkingowe za pomocą poleceń w języku naturalnym lub przez API REST i protokół MCP.

- **Zdalny endpoint MCP:** `https://api.paymove.io/api/mcp` (transport **Streamable HTTP**). Ten sam serwer jest też dostępny pod `https://mcp-api.paymove.io/mcp`.
- **Bez lokalnej instalacji:** Zdalny serwer MCP działa w chmurze Paymove — podłącz go bezpośrednio w **Claude Code**, **Cursor**, **Claude Desktop**, **Windsurf** lub dowolnym kliencie obsługującym standard MCP.
- **20 narzędzi produkcyjnych w 4 obszarach produktowych:**
  1. **Pay / DocPay & Payment Links (`7 narzędzi`)** — Tworzenie gotowych linków płatniczych (`pay.paymove.io`), zarządzanie wariantami cenowymi oraz generowanie transakcji checkout (`create-subproduct`) z identyfikatorem zamówienia `externalId`.
  2. **Pay&Go (`8 narzędzi`)** — Budowanie samoobsługowych stron sprzedaży biletów, usług i produktów cyfrowych (`go.paymove.io`), zarządzanie cennikiem, generowanie ilustracji AI dla biletów oraz tłumaczenia wielojęzyczne (`pl-PL`, `en-US`, `de-DE`, `uk-UA`).
  3. **Parking / Mobility (`3 narzędzia`)** — Uruchamianie płatnych stref parkingowych (`park.paymove.io`), konfiguracja taryf czasowych ISO-8601, limitów dziennych i tygodniowych, abonamentów oraz wydarzeń specjalnych.
  4. **Public Discovery & Partner Catalog (`2 narzędzia`)** — **`search-public-products` działa publicznie bez klucza API.** Każdy agent AI może wyszukać dostępne bilety, atrakcje, usługi i strefy parkingowe po nazwie, mieście/lokalizacji albo kategorii (`GO` / `PAY` / `PARKING`), sprawdzić cennik (`go-get-product`, `parking-get-pricing`, `list-pay-pricing-entries`) i otworzyć link do natychmiastowej płatności (`productLink`). `list-partner-products` pokazuje produkty zalogowanego partnera i wymaga `X-API-KEY`.

---

## Dlaczego Paymove? (Najważniejsze fakty i cennik)

- **Włącz płatności jednym zdaniem.** Bez konta, bez karty. Najpierw zobacz, potem się zdecyduj.
- **Sandbox od razu, produkcja po weryfikacji wymaganej prawem.**
- **Przejrzysty cennik:**
  - **0 zł za aktywację**
  - **0 zł miesięcznie**
  - **1,29% od transakcji** — stawka bazowa (checkout), która spada wraz ze skalą Twojego biznesu
  - **1 zł od transakcji, bez abonamentu i sprzętu** (Scan&Pay)
- **Wypłaty:** Pieniądze wpadają następnego dnia.
- **Obsługiwane waluty i metody płatności:**
  - **PLN** (domyślna waluta) — pełny zestaw metod płatności: **BLIK**, **karty płatnicze (Visa / Mastercard)**, **Apple Pay**, **Google Pay**, **pay-by-link** (szybkie przelewy online), **PayPo** (płatności odroczone) oraz przelew tradycyjny.
  - **EUR** oraz **CZK** — obsługiwane dla transakcji **kartą płatniczą**.
- **Status regulacyjny:** Jesteśmy Małą Instytucją Płatniczą wpisaną do rejestru dostawców usług płatniczych (**MIP 245/2024**).

---

## Szybki start

### 1. Pobierz klucz API

1. Zaloguj się do **[Panelu Partnera Paymove](https://panel.paymove.io)** (`panel.paymove.io`).
2. Przejdź do sekcji **Ustawienia → Klucze API**.
3. Wygeneruj swój klucz API partnera (`X-API-KEY`):
   - Klucz produkcyjny (`sk_live_...`) do pracy na środowisku produkcyjnym
   - Klucz testowy (`sk_test_...`) do testów w środowisku sandbox (`X-SANDBOX-API-KEY`)

---

### 2. Skonfiguruj swojego klienta MCP

#### Opcja A: Claude Code (CLI)

Uruchom poniższe polecenie w terminalu, aby dodać zdalny serwer Paymove MCP przez Streamable HTTP:

```bash
claude mcp add --transport http paymove https://api.paymove.io/api/mcp \
  --header "X-API-KEY: TWOJ_KLUCZ_API_PAYMOVE"
```

---

#### Opcja B: Cursor (`.cursor/mcp.json`)

Utwórz lub zaktualizuj plik `.cursor/mcp.json` w katalogu projektu (lub globalnie w `~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "paymove": {
      "url": "https://api.paymove.io/api/mcp",
      "headers": {
        "X-API-KEY": "TWOJ_KLUCZ_API_PAYMOVE"
      }
    }
  }
}
```

---

#### Opcja C: Claude Desktop (`claude_desktop_config.json`)

Dodaj serwer Paymove do pliku `claude_desktop_config.json` (`~/Library/Application Support/Claude/claude_desktop_config.json` na macOS lub `%APPDATA%\Claude\claude_desktop_config.json` na Windows) przy użyciu `mcp-remote`:

```json
{
  "mcpServers": {
    "paymove": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://api.paymove.io/api/mcp",
        "--header",
        "X-API-KEY: ${PAYMOVE_API_KEY}"
      ],
      "env": {
        "PAYMOVE_API_KEY": "TWOJ_KLUCZ_API_PAYMOVE"
      }
    }
  }
}
```

---

## Uwierzytelnianie i nagłówki HTTP

Serwer Paymove MCP komunikuje się przez protokół **Streamable HTTP**. Główny adres produkcyjny: `https://api.paymove.io/api/mcp`. Ten sam serwer jest też dostępny pod `https://mcp-api.paymove.io/mcp`. Przyjmuje następujące nagłówki HTTP:

| Nagłówek | Wymagany | Zakres narzędzi | Opis |
| :--- | :--- | :--- | :--- |
| `X-API-KEY` | **Tak** dla zarządzania produktami partnera; **niewymagany** przy publicznym katalogu | Narzędzia partnera (`Pay`, `Pay&Go`, `Parking`, `list-partner-products`). Narzędzia publiczne (`search-public-products`, `go-get-product`, `parking-get-pricing`, `list-pay-pricing-entries`) działają bez nagłówków | Klucz API wygenerowany w [panel.paymove.io](https://panel.paymove.io). Uwierzytelnia konto partnera i autoryzuje tworzenie produktów oraz linków płatniczych. |
| `X-SANDBOX-API-KEY` | Opcjonalnie | Środowisko testowe (Sandbox) | Klucz API środowiska sandbox zaczynający się od prefiksu `sk_test_...`. Po jego przekazaniu serwer kieruje wywołania do środowiska testowego (`pay.sandbox.paymove.io` / `go.sandbox.paymove.io`). |

> **Ważna uwaga dotycząca kwot:** Wszystkie kwoty pieniężne w narzędziach Paymove MCP (`price`, `amount`, `grossAmount`, `cost`, `fixedCost`, `maximumCostPerDay` itd.) podawane są jako liczby całkowite w **najmniejszych jednostkach waluty (groszach, 1/100 PLN)**. Przykładowo wartość `1000` oznacza **10,00 PLN**, a `150000` oznacza **1500,00 PLN**.

---

## Przegląd wszystkich 20 narzędzi MCP

Pełna dokumentacja parametrów wejściowych i schematów DTO znajduje się w pliku **[`docs/tools.md`](./docs/tools.md)**.

### 1. Pay / DocPay & Payment Links (7 narzędzi)

Tworzenie gotowych linków płatniczych (`https://pay.paymove.io/{productId}`) dla usług, konsultacji, rachunków, napiwków oraz transakcji checkout z własnym identyfikatorem zamówienia (`externalId`).

| Nazwa narzędzia | Opis |
| :--- | :--- |
| `create-pay-product` | Tworzy nowy produkt typu `PAY` wraz z ceną początkową i zwraca gotowy link płatniczy `payLink` (`https://pay.paymove.io/{productId}`). |
| `create-subproduct` | Tworzy płatność (subprodukt / checkout zamówienia) w ramach istniejącego produktu `PAY` i zwraca adres przekierowania klienta `redirectUrl`. |
| `update-subproduct` | Aktualizuje kwotę istniejącego subproduktu zidentyfikowanego przez `productId` oraz `externalId`. |
| `list-pay-pricing-entries` | Zwraca listę wszystkich pozycji cennika (wariantów cenowych) dla produktu `PAY`. Publiczne — bez klucza `X-API-KEY`. |
| `add-pay-pricing-entry` | Dodaje nowy wariant cenowy (np. pakiet usług lub propozycję napiwku) do istniejącego produktu `PAY`. |
| `update-pay-pricing-entry` | Aktualizuje cenę, opis lub szczegóły JSON istniejącej pozycji cennika produktu `PAY`. |
| `delete-pay-pricing-entry` | Trwale usuwa wybrany wariant cenowy z produktu `PAY`. |

**Przykładowe prompty:**
> *„Utwórz link płatniczy Paymove dla usługi 'Konsultacja prawna (60 min)' w cenie 350 PLN i dodaj drugi wariant cenowy na sesję 90-minutową za 500 PLN.”*
>
> *„Wygeneruj płatność (subprodukt) dla zamówienia ORD-2026-881 na kwotę 249,00 PLN z przekierowaniem powrotnym na https://sklep.example.pl/dziekujemy.”*

---

### 2. Pay&Go — Bilety, dobra cyfrowe i samoobsługa (8 narzędzi)

Tworzenie mobilnych stron szybkiego zakupu (`https://go.paymove.io/{productId}`) dla obiektów biletowanych, wydarzeń, produktów cyfrowych, mikro-retailu oraz urządzeń rozliczanych za czas.

| Nazwa narzędzia | Opis |
| :--- | :--- |
| `go-create-product` | Tworzy nową stronę produktową `GO` (`https://go.paymove.io/{productId}`) z wybranym układem mobilnym (`grid`, `scroll`, `slider`, `card`) i opcjonalnym blokiem linku na ekranie podsumowania. |
| `go-add-ticket-option` | Dodaje opcję biletu lub produktu do strony `GO` (tytuł, cena w groszach — `0` oznacza bilet bezpłatny, podtytuł, FAQ, URL grafiki). |
| `go-update-ticket-option` | Aktualizuje pola istniejącego wariantu biletu w produkcie `GO`. |
| `go-delete-ticket-option` | Trwale usuwa wariant biletu z produktu `GO`. |
| `go-update-product` | Aktualizuje układ widoku (`viewType`, `imageDisplayType`), nagłówki kroków, tryb walidacji biletów lub sekcję linku na stronie podsumowania. |
| `go-get-product` | Pobiera pełne dane produktu `GO` wraz z listą biletów i linkiem `productLink` w wybranej wersji językowej (`pl-PL`, `en-US`, `de-DE`, `uk-UA`). Publiczne — bez klucza `X-API-KEY`. |
| `go-set-translations` | Zapisuje tłumaczenia wielojęzyczne (`en-US`, `de-DE`, `uk-UA`, `pl-PL`) dla tytułów, podtytułów, opisów oraz pytań FAQ biletów. |
| `go-generate-image` | Generuje spójną ilustrację AI dla wybranej pozycji biletowej i zwraca publiczny adres `imageUrl`. |

**Przykładowy prompt:**
> *„Stwórz stronę biletową Pay&Go dla 'Ogród Botaniczny Wrocław' z trzema biletami: Normalny (35 PLN), Ulgowy (20 PLN) i Rodzinny (85 PLN). Wygeneruj spójne ilustracje AI dla każdego biletu i dodaj tłumaczenia na język angielski oraz niemiecki.”*

---

### 3. Parking / Mobility (3 narzędzia)

Uruchamianie płatnych stref parkingowych (`https://park.paymove.io/{shortName}`) z taryfami czasowymi ISO-8601, limitami dobowymi/tygodniowymi, abonamentami i cennikami na wydarzenia specjalne.

| Nazwa narzędzia | Opis |
| :--- | :--- |
| `parking-create-product` | Tworzy nowy płatny parking (`https://park.paymove.io/{shortName}`) z taryfą czasową (`PT15M`, `PT1H` itd.), godzinami aktywności, darmowym czasem i limitami opłat. |
| `parking-create-event` | Tworzy wydarzenie specjalne (`EVENT`) lub tymczasową zmianę cennika (`PRICING_CHANGE`) ze stawką ryczałtową (`fixedCost`) albo taryfą czasową (`entriesJson`). |
| `parking-get-pricing` | Pobiera aktualną konfigurację cennika, limitów, abonamentów i wydarzeń dla parkingu po identyfikatorze UUID lub nazwie skróconej `shortName`. Publiczne — bez klucza `X-API-KEY`. |

**Przykładowe prompty:**
> *„Utwórz strefę parkingową 'Parking Rynek Południe' w Krakowie: pierwsze 15 minut bezpłatnie, pierwsza godzina 4 PLN, każda kolejna powtarzalna godzina 6 PLN, maksymalny koszt dzienny 40 PLN.”*
>
> *„Dodaj wydarzenie specjalne na naszym parkingu przy stadionie na dzień 2026-11-15 w godzinach 16:00–23:59 ze stałą opłatą ryczałtową 30 PLN.”*

---

### 4. Public Discovery & Partner Catalog (2 narzędzia)

**`search-public-products` działa publicznie bez klucza API.** Każdy agent AI może wyszukać dostępne bilety, atrakcje, usługi i strefy parkingowe po nazwie, mieście/lokalizacji albo kategorii (`GO` / `PAY` / `PARKING`), sprawdzić cennik (`go-get-product`, `parking-get-pricing`, `list-pay-pricing-entries`) i otworzyć link do natychmiastowej płatności (`productLink`).

| Nazwa narzędzia | Opis |
| :--- | :--- |
| `search-public-products` | Wyszukuje publiczne produkty `GO`, `PAY` i `PARKING`. Bez klucza `X-API-KEY`. Zwraca `productLink` (`https://go.paymove.io/{shortName}`, `https://pay.paymove.io/{shortName}` lub `https://parking.paymove.io/{shortName}`). |
| `list-partner-products` | Zwraca listę produktów należących do uwierzytelnionego partnera dla wybranego typu produktu (`PAY`, `GO` lub `PARKING`). Wymaga `X-API-KEY`. |

**Przykładowe prompty:**
> *„Znajdź bilety do zoo w Gdańsku i pokaż cenę biletu normalnego.”*
>
> *„Pokaż wszystkie moje produkty typu PAY oraz GO w Paymove.”*

---

## Struktura repozytorium

```text
.
├── README.md                          # Dokumentacja w języku angielskim (dla katalogów MCP i modeli LLM)
├── README.pl.md                       # Dokumentacja w języku polskim
├── LICENSE                            # Licencja MIT
├── server.json                        # Manifest dla oficjalnego MCP Registry (registry.modelcontextprotocol.io)
├── docs/
│   └── tools.md                       # Pełna referencja wszystkich 20 narzędzi MCP i schematów DTO
└── examples/
    ├── cursor-mcp.json                # Przykładowa konfiguracja dla edytora Cursor
    └── claude_desktop_config.json     # Przykładowa konfiguracja dla aplikacji Claude Desktop
```

---

## Linki i wsparcie

- **Strona główna:** [https://paymove.io](https://paymove.io)
- **Panel Partnera:** [https://panel.paymove.io](https://panel.paymove.io)
- **Dokumentacja techniczna:** [https://docs.paymove.io](https://docs.paymove.io)
- **Endpoint MCP:** `https://api.paymove.io/api/mcp` (także `https://mcp-api.paymove.io/mcp`)
- **Status regulacyjny:** Mała Instytucja Płatnicza wpisana do rejestru dostawców usług płatniczych (MIP 245/2024)
