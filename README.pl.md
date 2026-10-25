<div align="center">

<br />

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/logo-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="./assets/logo-light.svg" />
  <img alt="Paymove" src="./assets/paymove-logo.png" width="340" />
</picture>

<br />
<br />

### **Oficjalny serwer Model Context Protocol (MCP) dla zakupów agentycznych, usług miejskich i błyskawicznych płatności**

*Wyszukuj i kupuj bilety do muzeów, zoo i atrakcji oraz opłacaj parkingi miejskie w **ponad 70 miastach w Polsce** — albo twórz linki płatnicze, checkouty e-commerce i samoobsługowe sklepy biletowe w jednej rozmowie z agentem AI.*

<br />

[![MCP Protocol](https://img.shields.io/badge/MCP-Streamable_HTTP-635BFF?style=for-the-badge)](https://api.paymove.io/api/mcp)
[![Tools](https://img.shields.io/badge/Narz%C4%99dzia-20_Narz%C4%99dzi_MCP-00B67A?style=for-the-badge)](./docs/tools.md)
[![Catalog](https://img.shields.io/badge/Katalog_Live-70%2B_Miast_%C2%B7_630%2B_Produkt%C3%B3w-0A85EA?style=for-the-badge)](#katalog-dost%C4%99pnych-lokalizacji-i-produkt%C3%B3w)
[![Regulated](https://img.shields.io/badge/KNF-MIP245%2F2024-F59E0B?style=for-the-badge)](https://paymove.io)
[![License](https://img.shields.io/badge/Licencja-MIT-1E293B?style=for-the-badge)](./LICENSE)

<br />

[**English (`README.md`)**](./README.md) &nbsp;·&nbsp; [**Polski**](./README.pl.md) &nbsp;·&nbsp; [**Pełny katalog miast i produktów (`docs/catalog.md`)**](./docs/catalog.md) &nbsp;·&nbsp; [**Dokumentacja 20 narzędzi (`docs/tools.md`)**](./docs/tools.md) &nbsp;·&nbsp; [**Dokumentacja API**](https://docs.paymove.io)

---

[**Szybki start (60s)**](#szybki-start-w-60-sekund) &nbsp;•&nbsp; [**Jak to działa**](#jak-to-dzia%C5%82a--architektura-dwu-trybowa) &nbsp;•&nbsp; [**Katalog lokalizacji i produktów**](#katalog-dost%C4%99pnych-lokalizacji-i-produkt%C3%B3w) &nbsp;•&nbsp; [**Referencja 20 narzędzi**](#kompletna-referencja-20-narz%C4%99dzi-mcp) &nbsp;•&nbsp; [**Reguły dla agentów**](#kluczowe-regu%C5%82y-dla-agent%C3%B3w-ai) &nbsp;•&nbsp; [**Dlaczego Paymove**](#dlaczego-paymove)

</div>

<br />

## Czym jest Paymove MCP Server?

**Paymove MCP Server** (`https://api.paymove.io/api/mcp`) to zdalny, niewymagający instalacji serwer **Streamable HTTP**, który łączy agentów AI (Claude Code, Cursor, Claude Desktop, Windsurf, ChatGPT oraz własne aplikacje MCP) bezpośrednio z infrastrukturą płatniczą i miejską **Paymove**.

Paymove to polski fintech nadzorowany przez **Komisję Nadzoru Finansowego (KNF — licencja `MIP245/2024`)**. Jedno połączenie MCP pozwala agentom działać w dwóch uzupełniających się trybach:

1. **Tryb Public Discovery (`Zero-Auth` — Zakupy Agentyczne w Mieście)** — **Nie wymaga klucza API.** Każdy agent AI może przeszukiwać publiczny katalog usług miejskich, sprawdzać aktualne ceny biletów do zoo, muzeów, parków rozrywki, na lotniska i do komunikacji miejskiej, weryfikować stawki w Strefach Płatnego Parkowania (**SPP**) w **ponad 70 polskich miastach** i zwracać gotowy link do płatności **BLIK / Apple Pay / Google Pay**.
2. **Tryb Partner & Merchant (`X-API-KEY`)** — Uwierzytelnieni partnerzy i deweloperzy otrzymują dostęp do pełnego zestawu **20 narzędzi w 4 domenach**: tworzenia linków płatniczych (`PAY`), checkoutów e-commerce (`create-subproduct`), samoobsługowych sklepów biletowych (`GO`) z generowaniem grafik AI i tłumaczeniami wielojęzycznymi oraz zarządzania strefami parkingowymi (`PARKING`).

<br />

---

<br />

## Jak to działa — Architektura Dwu-Trybowa

```text
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                              Agent AI / Klient MCP                                   │
│              (Claude Code · Cursor · Claude Desktop · Windsurf · Custom)             │
└───────────────────┬──────────────────────────────────────────────┬───────────────────┘
                    │                                              │
     Tryb 1: Public Discovery (Zero-Auth)            Tryb 2: Zarządzanie Partnera
            (Bez klucza API)                             (Nagłówek: X-API-KEY)
                    │                                              │
                    ▼                                              ▼
┌───────────────────────────────────────────┐  ┌───────────────────────────────────────┐
│  • search-public-products                 │  │  • Płatności i Checkouty PAY (7)      │
│  • go-get-product                         │  │  • Bilety i Atrakcje Pay&Go + AI (8)  │
│  • parking-get-pricing                    │  │  • Strefy Parkingowe i Eventy (3)     │
│  • list-pay-pricing-entries               │  │  • Katalog Produktów Partnera (2)     │
└───────────────────┬───────────────────────┘  └───────────────────┬───────────────────┘
                    │                                              │
                    └──────────────────────┬───────────────────────┘
                                           ▼
┌──────────────────────────────────────────────────────────────────────────────────────┐
│               Natychmiastowy Checkout Mobilny i Webowy (Bez aplikacji)               │
│     go.paymove.io/{kod}    ·   park.paymove.io/{kod}    ·   pay.paymove.io/{kod}     │
│                  BLIK  ·  Apple Pay  ·  Google Pay  ·  Karty  ·  PayPo               │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

<br />

| Endpoint / Środowisko | Adres URL | Przeznaczenie |
| :--- | :--- | :--- |
| **Główny Serwer MCP (Produkcja)** | `https://api.paymove.io/api/mcp` | Endpoint Streamable HTTP MCP dla trybu Zero-Auth oraz Partner (`X-API-KEY`) |
| **Alternatywny Serwer MCP** | `https://mcp-api.paymove.io/mcp` | Bezpośredni alias produkcyjnego serwera Streamable HTTP MCP |
| **Produkcyjne REST API** | `https://api.paymove.io` | Produkcyjne REST API do tworzenia płatności po stronie serwera i obsługi webhooków |
| **Sandbox REST API** | `https://gateway-api.sandbox.paymove.io` | Środowisko testowe dla kluczy `sk_test_...` oraz testowych kodów BLIK `777xxx` |
| **Panel Partnera (Back Office)** | [`https://panel.paymove.io`](https://panel.paymove.io) | Panel do generowania kluczy API (`sk_live_...` / `sk_test_...`), konfiguracji produktów i rozliczeń |
| **Indeks Dokumentacji dla LLM** | [`https://docs.paymove.io/llms.txt`](https://docs.paymove.io/llms.txt) | Spis dokumentacji dla modeli AI, specyfikacja OpenAPI oraz procedura [`skill.md`](https://docs.paymove.io/skill.md) |

<br />

---

<br />

## Szybki Start w 60 Sekund

### Wariant A — Tryb Publiczny `Zero-Auth` *(Zakupy agentyczne w mieście — bez klucza API)*

Podłącz dowolnego agenta AI bezpośrednio do `https://api.paymove.io/api/mcp` bez żadnych nagłówków, aby wyszukiwać i kupować bilety, atrakcje miejskie oraz opłacać parkingi w całej Polsce.

#### 1. Claude Code (CLI)

```bash
claude mcp add --transport http paymove https://api.paymove.io/api/mcp
```

#### 2. Cursor (`.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "paymove": {
      "url": "https://api.paymove.io/api/mcp"
    }
  }
}
```

#### 3. Claude Desktop (`claude_desktop_config.json`)

```json
{
  "mcpServers": {
    "paymove": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://api.paymove.io/api/mcp"]
    }
  }
}
```

<br />

### Wariant B — Tryb Partnera / Merchanta *(Z kluczem `X-API-KEY`)*

Wygeneruj klucz API w [**panel.paymove.io**](https://panel.paymove.io) (`sk_live_...` dla produkcji, `sk_test_...` dla sandboxa) i przekaż go w nagłówku `X-API-KEY`.

#### 1. Claude Code (CLI)

```bash
claude mcp add --transport http paymove https://api.paymove.io/api/mcp \
  --header "X-API-KEY: YOUR_PAYMOVE_API_KEY"
```

#### 2. Cursor (`.cursor/mcp.json` — zobacz [`examples/cursor-mcp.json`](./examples/cursor-mcp.json))

```json
{
  "mcpServers": {
    "paymove": {
      "url": "https://api.paymove.io/api/mcp",
      "headers": {
        "X-API-KEY": "YOUR_PAYMOVE_API_KEY"
      }
    }
  }
}
```

#### 3. Claude Desktop (`claude_desktop_config.json` — zobacz [`examples/claude_desktop_config.json`](./examples/claude_desktop_config.json))

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
        "PAYMOVE_API_KEY": "YOUR_PAYMOVE_API_KEY"
      }
    }
  }
}
```

> [!TIP]
> **Przekierowanie na Sandbox:** Dodaj nagłówek `"X-SANDBOX-API-KEY": "sk_test_..."` obok `X-API-KEY`, aby kierować operacje narzędzi MCP bezpośrednio na środowisko testowe Paymove Sandbox (`pay.sandbox.paymove.io` / `go.sandbox.paymove.io`).

<br />

### Przykładowe Prompty do Agenta

| Scenariusz | Przykładowe polecenie dla agenta | Wykorzystywane narzędzia |
| :--- | :--- | :--- |
| **Zakup biletu do ZOO lub muzeum (Zero-Auth)** | *„Znajdź bilety do ZOO w Gdańsku albo Muzeum POLIN w Warszawie, sprawdź rodzaje i ceny biletów i podaj mi link do płatności BLIK-iem.”* | `search-public-products` → `go-get-product` |
| **Opłacenie parkingu w mieście (Zero-Auth)** | *„Sprawdź dostępne strefy parkowania w Pucku, Kołobrzegu albo we Wrocławiu, zweryfikuj stawkę godzinową i podaj bezpośredni link do opłacenia postoju.”* | `search-public-products` → `parking-get-pricing` |
| **Rodzinny weekend w Trójmieście (Zero-Auth)** | *„Jakie atrakcje dla dzieci są dostępne przez Paymove w Gdańsku i Sopocie? Porównaj ceny biletów do Jungle Jump, Słonika Balonika i Happy Kangur.”* | `search-public-products` → `go-get-product` |
| **Utworzenie linku płatniczego (Merchant)** | *„Utwórz produkt płatniczy Paymove dla Konsultacji Prawnej za 350 PLN i zwróć gotowy link `pay.paymove.io`.”* | `create-pay-product` |
| **Sklep biletowy z grafiką AI (Merchant)** | *„Stwórz produkt biletowy Pay&Go na 'Warsztat Poland Tech Week' w Warszawie z biletem Normalnym (99 PLN) i Ulgowym (49 PLN), dodaj opisy PL/EN i wygeneruj ilustrację okładkową AI.”* | `go-create-product` → `go-set-translations` → `go-generate-image` |

<br />

---

<br />

## Katalog Dostępnych Lokalizacji i Produktów

Paymove obsługuje **zakupy agentyczne za usługi miejskie** w **ponad 70 miastach w Polsce** oraz **ponad 630 aktywnych produktach publicznych**. Każdy poniższy produkt może zostać wyszukany przez `search-public-products` i odczytany w czasie rzeczywistym bez klucza API.

> [!NOTE]
> Pełny, **670-wierszowy wykaz wszystkich lokalizacji i ulic** (w tym wszystkie **396 odcinków ulic SPP w Szczecinie** oraz komplet identyfikatorów UUID) znajduje się w pliku [**`docs/catalog.md`**](./docs/catalog.md).

<br />

### 1. Publiczne Katalogi Tematyczne (`catalog.paymove.io`)

| Slug katalogu | Publiczny adres URL | Region i zakres | Dostępne produkty w katalogu |
| :--- | :--- | :--- | :--- |
| **`gogda`** | [**`catalog.paymove.io/gogda`**](https://catalog.paymove.io/gogda) | **Gdańsk, Sopot i Pomorze** *(Katalog atrakcji Sun & Snow)* | **ZOO Gdańsk** (`cb62`), **Dyniowe Love Rotmanka** (`738`), **Park Dmuchańców Słonik Balonik** (`899`), **Park Dmuchańców Happy Kangur Sopot** (`0dd2`), **Jungle Jump CH Osowa** (`d9e6`) |
| **`wcs`** | [**`catalog.paymove.io/wcs`**](https://catalog.paymove.io/wcs) | **Arena Legionowo** *(Aglomeracja Warszawska)* | **World Cat Show — Sobota 07.11** (`dw57`), **World Cat Show — Niedziela 08.11** (`dw66`) |
| **`rudy-las`** | [**`catalog.paymove.io/rudy-las`**](https://catalog.paymove.io/rudy-las) | **Rudy (Woj. Śląskie)** | **Rudy Las — Bal Andrzejkowy** (`ad55`), **Rudy Las — Kolejka wąskotorowa** (`km75`) |

<br />

### 2. `GO` — Bilety, Muzea, ZOO, Atrakcje, Lotniska VIP i Komunikacja Miejska

#### 2.1 Muzea i Instytucje Kultury

| Miasto | Instytucja / Wystawa | Partner | Kod | Bezpośredni link zakupowy | Aktualne warianty biletów i ceny (`PLN`) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Warszawa** | **Muzeum Historii Żydów Polskich POLIN** | MHŻP POLIN × Biledo | `91a4` | [`go.paymove.io/91a4`](https://go.paymove.io/91a4) | **Normalny:** `45.00 PLN` · **Ulgowy:** `35.00 PLN` · **Muzeum za złotówkę:** `1.00 PLN` *(W czwartki wstęp bezpłatny)* |
| **Warszawa** | **POLIN — Darowizny na cele statutowe** | MHŻP POLIN | `b780` | [`go.paymove.io/b780`](https://go.paymove.io/b780) | **Darowizna:** `10.00 PLN` / `20.00 PLN` / `50.00 PLN` / dowolna kwota |
| **Lublin** | **Muzeum Narodowe w Lublinie — Kaplica Trójcy Świętej** | Muzeum Narodowe w Lublinie × Biledo | `6b58` | [`go.paymove.io/6b58`](https://go.paymove.io/6b58) | Bilety na konkretne godziny wejścia z harmonogramu Biledo (`go-get-product`) |
| **Lublin** | **Muzeum Narodowe w Lublinie — Tamara Łempicka: ponad granicami** | Muzeum Narodowe w Lublinie × Biledo | `1ef4` | [`go.paymove.io/1ef4`](https://go.paymove.io/1ef4) | Bilety na wystawę czasową z harmonogramu Biledo (`go-get-product`) |
| **Krosno** | **Centrum Dziedzictwa Szkła — Miasto Szkła Krosno** | CDS Krosno × Biledo | `aoff` | [`go.paymove.io/aoff`](https://go.paymove.io/aoff) | **Normalny:** `45.00 PLN` · **Ulgowy:** `35.00 PLN` · **Ulgowy z Kartą Dużej Rodziny:** `30.00 PLN` |
| **Sulejówek** | **Muzeum Józefa Piłsudskiego w Sulejówku** | MJPwS × Biledo | `mjpws` | Integracja partnerska Biledo | Bilety wstępu na wystawę stałą i czasową |

<br />

#### 2.2 Ogrody Zoologiczne, Wystawy Świetlne (`Garden of Lights`) i Parki Rozrywki

| Miasto | Atrakcja / Obiekt | Partner | Kod | Bezpośredni link zakupowy | Aktualne warianty biletów i ceny (`PLN`) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Gdańsk** | **Gdański Ogród Zoologiczny (ZOO Gdańsk)** | Ogród Zoologiczny Gdańsk × Biledo | `cb60` | [`go.paymove.io/cb60`](https://go.paymove.io/cb60) | **Normalny:** `30.00 PLN` · **Ulgowy:** `20.00 PLN` · **Rodzinny:** `90.00 PLN` · **Do 3 r.ż.:** `0.00 PLN` |
| **Gdańsk** | **Bilety ZOO Gdańsk — Katalog Sun & Snow** | Ogród Zoologiczny Gdańsk × Sun & Snow | `cb62` | [`go.paymove.io/cb62`](https://go.paymove.io/cb62) | **Normalny:** `40.50 PLN` · **Ulgowy:** `31.50 PLN` · **Rodzinny:** `126.00 PLN` · **Do 3 r.ż.:** `0.00 PLN` |
| **Gdańsk** | **Fundacja Lynx — Gdański Ogród Zoologiczny** | Fundacja Gdańskiego Ogrodu Zoologicznego Lynx | `81ef` | [`go.paymove.io/81ef`](https://go.paymove.io/81ef) | **Darowizna przy wybiegach ZOO:** `10.00 PLN` / `20.00 PLN` / `50.00 PLN` / dowolna kwota |
| **Gdańsk** | **Jungle Jump — Park Rozrywki (CH Osowa, ul. Spacerowa 48)** | Wielka Fabryka Elfów Sp. z o.o. | `d9e6` | [`go.paymove.io/d9e6`](https://go.paymove.io/d9e6) | **Bilet 1h:** `34.00 PLN` · **1h + 5× Amazon River:** `50.00 PLN` · **3h:** `54.00 PLN` · **3h + 10× Amazon River:** `90.00 PLN` |
| **Gdańsk** | **Wielka Fabryka Elfów — Warsztaty Świąteczne** *(ul. Budowlanych 21A)* | Wielka Fabryka Elfów Sp. z o.o. | `7def` | [`go.paymove.io/7def`](https://go.paymove.io/7def) | **Świąteczny witraż:** `25.00 PLN` · **Reniferowy łapacz snów:** `30.00 PLN` · **Bombka akrylowa:** `30.00 PLN` |
| **Gdańsk Brzeźno** | **Park Dmuchańców Słonik Balonik** *(ul. Południowa obok Domu Zdrojowego)* | FH Alfreda Stodolniak-Matelska | `899` / `899d` | [`go.paymove.io/899`](https://go.paymove.io/899) | **Bilet regularny 1h:** `55.00 PLN` · **Bilet Social Media 1h:** `50.00 PLN` · **Kolejna godzina:** `20.00 PLN` |
| **Sopot** | **Park Dmuchańców Happy Kangur** *(ul. Bitwy pod Płowcami 57, wejście nr 35)* | FH Alfreda Stodolniak-Matelska | `0dd2` / `Odd2` | [`go.paymove.io/0dd2`](https://go.paymove.io/0dd2) | **Bilet regularny 1h:** `59.00 PLN` · **Bilet Social Media 1h:** `55.00 PLN` · **Kolejna godzina:** `20.00 PLN` |
| **Rotmanka** *(k. Gdańska)* | **Dyniowe Love — Farma Dyniowa** *(ul. Zaczarowana 58)* | Paweł Łys Dyniowe Love | `738` / `738b` | [`go.paymove.io/738`](https://go.paymove.io/738) | **Wejście:** `15.00–25.00 PLN` · **Park linowy:** `25.00 PLN` · **Dmuchańce:** `35.00 PLN` · **Combo całodzienny:** `60.00 PLN` |
| **Warszawa** | **Garden of Lights — Warszawa** | Wonderful Lighting Sp. z o.o. | `5f3d` | [`go.paymove.io/5f3d`](https://go.paymove.io/5f3d) | **Dorośli i młodzież (12–60):** `42.00 PLN` · **Dzieci / Seniorzy 60+ / OzN:** `37.00 PLN` · **Dzieci do 100 cm:** `1.00 PLN` |
| **Kraków** | **Garden of Lights — Kraków** | Wonderful Lighting Sp. z o.o. | `62be` | [`go.paymove.io/62be`](https://go.paymove.io/62be) | **Dorośli i młodzież (12–60):** `42.00 PLN` · **Dzieci / Seniorzy 60+ / OzN:** `37.00 PLN` · **Dzieci do 100 cm:** `1.00 PLN` |
| **Wrocław** | **Garden of Lights — Wrocław** | Wonderful Lighting Sp. z o.o. | `0797` | [`go.paymove.io/0797`](https://go.paymove.io/0797) | **Dorośli i młodzież (12–60):** `42.00 PLN` · **Dzieci / Seniorzy 60+ / OzN:** `37.00 PLN` · **Dzieci do 100 cm:** `1.00 PLN` |
| **Szczecin** | **Garden of Lights — Szczecin** | Wonderful Lighting Sp. z o.o. | `71fe` | [`go.paymove.io/71fe`](https://go.paymove.io/71fe) | **Dorośli i młodzież (12–60):** `44.00 PLN` · **Dzieci / Seniorzy 60+ / OzN:** `39.00 PLN` · **Dzieci do 100 cm:** `1.00 PLN` |
| **Gdynia** | **Garden of Lights — Gdynia** | Wonderful Lighting Sp. z o.o. | `7a38` | [`go.paymove.io/7a38`](https://go.paymove.io/7a38) | Bilety wstępu pod adresem `go.paymove.io/7a38` |

<br />

#### 2.3 Lotniska VIP, Komunikacja Miejska, Rekreacja, SPA i Wydarzenia

| Miasto / Region | Usługa / Obiekt | Partner | Kod | Bezpośredni link zakupowy | Aktualne warianty biletów i ceny (`PLN`) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Gdańsk** | **Port Lotniczy Gdańsk im. Lecha Wałęsy — Usługi VIP** | Port Lotniczy Gdańsk | `lotnisko-gdansk` | Terminale odlotów PLG | **Fast Track (bramka kontroli bezpieczeństwa QR):** `50.00 PLN` · **Salon Executive (Business Lounge QR):** `150.00 PLN` |
| **Polska (Transport)** | **Komunikacja Miejska (Linia A & Linia B)** | Paymove Mobility | `ab12` / `km10` | [`go.paymove.io/ab12`](https://go.paymove.io/ab12) | **15 min:** `1.00 PLN` (ulgowy) / `2.00 PLN` (normalny) · **30 min:** `2.00 / 3.00 PLN` · **60 min:** `3.00 / 5.00 PLN` |
| **Stronie Śląskie** | **Stroński Park Aktywności — Łowisko** | SPA „Jaskinia Niedźwiedzia” Sp. z o.o. | `d872` | [`go.paymove.io/d872`](https://go.paymove.io/d872) | **Karnet 1 dzień:** `20.00 PLN` · **Karnet 3 dni:** `50.00 PLN` · **Karnet 7 dni:** `80.00 PLN` |
| **Stronie Śląskie** | **Stroński Park Aktywności — Kąpielisko** | SPA „Jaskinia Niedźwiedzia” Sp. z o.o. | `5823` | [`go.paymove.io/5823`](https://go.paymove.io/5823) | **Bilet normalny:** `17.00 PLN` · **Bilet ulgowy:** `10.00 PLN` |
| **Ustronie Morskie** | **AMARI Holistic SPA** *(The One by Sun & Snow)* | Sun & Snow × AMARI SPA | `8c4b` | [`go.paymove.io/8c4b`](https://go.paymove.io/8c4b) | **Refleksoterapia (30 min):** `200.00 PLN` · **Masaż relaksacyjny / BIOaloes / Thai Slim (60 min):** `250.00 PLN` · **90 min:** `350.00 PLN` |
| **Rudy** *(k. Raciborza)* | **Rudy Las — Przejazd Kolejką Wąskotorową** | Rudy Las | `km75` | [`go.paymove.io/km75`](https://go.paymove.io/km75) | **Bilet wstępu:** `15.00 PLN` · **Wejście + Przejazd kolejką:** `49.00 PLN` |
| **Rudy** *(k. Raciborza)* | **Rudy Las — Bal Andrzejkowy** | Rudy Las | `ad55` | [`go.paymove.io/ad55`](https://go.paymove.io/ad55) | **Bilet pojedynczy:** `299.00 PLN` · **Bilet dla par:** `599.00 PLN` |
| **Legionowo** | **World Cat Show — Międzynarodowa Wystawa Kotów Rasowych** | Stowarzyszenie Koty Rasowe | `dw57` / `dw66` | [`go.paymove.io/dw57`](https://go.paymove.io/dw57) | **Bilet normalny (Sobota / Niedziela):** `35.00 PLN` · **Bilet ulgowy:** `25.00 PLN` |
| **Dąbrowa Tarnowska** | **Parafia pw. NMP Szkaplerznej — Wirtualna Taca & Świece** | Parafia pw. NMP Szkaplerznej | `5aa2` / `fe67` | [`go.paymove.io/5aa2`](https://go.paymove.io/5aa2) | **Wirtualna Taca:** `1.00 / 20.00 / 50.00 / 100.00 PLN` · **Świeca wotywna:** `2.00 / 5.00 PLN` |

<br />

---

<br />

### 3. `PARKING` — Strefy Płatnego Parkowania (SPP) i Parkingi Miejskie (70+ Miast)

Paymove obsługuje **ponad 592 aktywne strefy parkingowe na produkcji** (`https://park.paymove.io/{id}`) w **ponad 70 miastach w Polsce** — obejmując miejskie **Strefy Płatnego Parkowania (SPP)**, **parkingi przy dworcach PKP**, **największe hale widowiskowo-sportowe i stadiony** (*Ergo Arena*, *Tarczyński Arena*, *Tauron Arena*, *Arena Toruń*, *Enea Arena*), **szpitale**, **kurorty nadmorskie i górskie** oraz parkingi komercyjne (*EuroPark*, *WEIP*, *ParkEMI*, *nEverest*, *DZP*, *CTECH*, *FitParking*, *Indigo*, *Roan*).

#### 3.1 Największe Wdrożenia Miejskie i Wielostrefowe

| Miasto | Aktywne strefy | Kluczowe lokalizacje, areny i zakres miejskiego SPP | Przykładowy link do opłaty |
| :--- | :---: | :--- | :--- |
| **Szczecin** | **396** | **395 ulicznych stref SPP** (`NiOL`) + **Płatny Parking Niestrzeżony pod Trasą Zamkową** (`86061819`) + **Enea Arena** | [`park.paymove.io/86061819…`](https://park.paymove.io/86061819-bfbb-4ecd-a098-d97c90ac280b) |
| **Kołobrzeg** | **17** | **Dworzec PKP Kołobrzeg**, **Port Pasażerski**, **Port Rybacki**, **Amfiteatr**, **Hala Milenium**, **Marina Solna**, **Bałtycka**, **Kasprowicza**, **Fredry**, **Kościuszki**, **Kamienna**, **Młyńska**, **Myśliwska**, **Obrońców Westerplatte**, **Korty Tenisowe**, **Nadmorskie Tarasy**, **Unii Lubelskiej** | [`park.paymove.io/c93977c0…`](https://park.paymove.io/c93977c0-6906-4475-b28f-4cc6469492a7) |
| **Puck** | **16** | **Miejska SPP i PP:** Plac Obrońców Wybrzeża, Morska, Aleja Lipowa, Aleja Ceynowy, 1-go Maja, 10-go Lutego (SPP i PP), Nowy Świat (SPP i PP), kpt. Mamerta Stankiewicza PP, Elizy Orzeszkowej, Judyckiego, Męczenników Piaśnicy, Pokoju, Sambora, Wałowa | [`park.paymove.io/a4d30541…`](https://park.paymove.io/a4d30541-3f68-4fc1-8eb0-cd026cb46888) |
| **Wrocław** | **14** | **Dworzec PKP Wrocław Główny** (naziemny i podziemny + ul. Joannitów i ul. Żelazna), **Tarczyński Arena** (9 stref: Ogólna, VIP/Le Mans, Broadcast, 6 wariantów Camper Park), **ul. Awicenny 45** | [`park.paymove.io/6bf749b6…`](https://park.paymove.io/6bf749b6-776d-402b-a6a8-dfbfe0d519cc) |
| **Kielce** | **10** | **ul. Marii Konopnickiej**, **ul. Barwinek 29**, **SM Bocianek**, **ul. Bodzentyńska 15**, **ul. Ćwiklińskiej 2**, **ul. Szajnowicza-Iwanowa 17**, **ul. Szydłówek Górny 6 i 10**, **ul. Wapiennikowa** (`cc4f`), **ul. Warszawska 147 i 218d** | [`park.paymove.io/cc4f`](https://park.paymove.io/cc4f) |
| **Warszawa** | **8** | **Dworzec PKP Warszawa Centralna** (`50d4cd96`), **PKP Warszawa Gdańska** (`adaeac32`), **PKP Warszawa Wschodnia** (Główny + ul. Lubelska krótkoterminowy `091a`, długoterminowy `16ce`, autobusy `767f`), **PKP Warszawa Towarowa** (`84f3`) | [`park.paymove.io/091a`](https://park.paymove.io/091a) |
| **Gdańsk** | **7** | **Ergo Arena** (osobowe `8898` i autokary/kampery `22a2`), **Dworzec PKP Gdańsk Główny** (`44f942bb`), **ul. Polanki 117** (`ecf6`), **ul. Smoluchowskiego** (`c57f`), **ul. Mieszczańska** (`0bb0`), **ul. Platynowa 2** (`9a39a5de`) | [`park.paymove.io/8898`](https://park.paymove.io/8898) |
| **Wieliczka** | **7** | **FITPARKING P1** (`41610c0e`), **FITPARKING P1 Camper/Bus** (`c77d8010`), **FITPARKING P2** (`37ad6a3f`), **ul. Goliana 10** (`0fbc`), **ul. Niecała Cmentarz** (`0164`), **ul. Słowackiego 3 i 12** (`8254`, `9759`) | [`park.paymove.io/0fbc`](https://park.paymove.io/0fbc) |
| **Kościerzyna** | **6** | **Miejska SPP Kościerzyna** (`1389`), **AQUA Centrum** (`983789df`), **ul. 3 Maja** (`e2ba5048`), **ul. Lubomira Szopińskiego** (`7858e1dd`), **ul. Świętojańska** (`0c61d988`), **ul. Kapliczna** (`c6575f78`) | [`park.paymove.io/1389`](https://park.paymove.io/1389) |
| **Kraków** | **5** | **Tauron Arena / Al. Pokoju 46** (`7ddd`), **SM Podwawelska — DZP** (`cbcc`), **ul. Garbarska 18b — ParkEMI** (`c231`), **os. Kombatantów — ParkEMI** (`0a97`), **ul. Aktorów 1 i Wizjonerów 7** (`d9ed4b59`) | [`park.paymove.io/7ddd`](https://park.paymove.io/7ddd) |
| **Olsztyn** | **5** | **Warmińsko-Mazurskie Centrum Chorób Płuc** (`741db750`), **Wojewódzki Zespół Lecznictwa Psychiatrycznego** (`dcf3595f`), **ul. Żołnierska 16 i 19A**, **ul. Kołobrzeska 50** | [`park.paymove.io/741db750…`](https://park.paymove.io/741db750-1914-4d89-994f-e38665fb7f54) |
| **Rybnik** | **5** | **Miejska SPP i parkingi rekreacyjne:** Pniowska (plaża `18f8` i za groblą `91d5`), Rudzka Pniowiec (`2f92`), Sławików (`d2bf`), Za Komendą (`dd57`) | [`park.paymove.io/dd57`](https://park.paymove.io/dd57) |
| **Toruń** | **5** | **Arena Toruń** (osobowe `0804132b`, autokary `6dcc27d3`, abonamenty 30 dni `9dccd4e8` i `7a67966e`), **ul. Podgórska 12a** (`c41a13a8`) | [`park.paymove.io/0804132b…`](https://park.paymove.io/0804132b-0d27-4fb5-b1a8-e51be65b0f09) |
| **Zabrze** | **5** | **ul. 3 Maja 93** (`80ef`), **ul. De Gaulle'a 75** (`6bb4e596`), **ul. Banachiewicza 15a** (`235df86c`), **ul. Skłodowskiej-Curie 24** (`770275e1`), **ul. Tatarkiewicza 12** (`c9093a12`) | [`park.paymove.io/80ef`](https://park.paymove.io/80ef) |
| **Łódź** | **5** | **ul. Bandurskiego 49** (`2ade47e5`), **ul. Rydla 31** (`ae293c0a`), **ul. Łagiewnicka 54/56** (`2888e2ee`), **Dworzec PKP Łódź Kaliska** (`d5c4`, `805c`) | [`park.paymove.io/2ade47e5…`](https://park.paymove.io/2ade47e5-2d61-4e35-8753-da3f4310391a) |
| **Lublin** | **4** | **MOSiR Bystrzyca — ul. Stadionowa 1** (osobowe `39f3` i autokary `378a`), **S.M. Rudnik** (`4d42`), **Lublin Okopowa PKP** (`6024`) | [`park.paymove.io/39f3`](https://park.paymove.io/39f3) |
| **Sopot** | **4** | **Sofitel Grand Sopot** (`09d6ce12`), **Sopot Tenis Klub** (ul. Tenisowa `984399af` i ul. Osiedlowa `489d404d`), **ul. Ogrodowa 6a** (`81c4`) | [`park.paymove.io/81c4`](https://park.paymove.io/81c4) |
| **Władysławowo** | **4** | **Miejska SPP Władysławowo** (`1870`, `4a84`), **ul. Bohaterów Kaszubskich** (`85c8`), **ul. Starowiejska** (`94b1`) | [`park.paymove.io/85c8`](https://park.paymove.io/85c8) |
| **Bydgoszcz** | **3** | **Dworzec PKP Bydgoszcz Główna** (`67fa0d96`), **ul. Gdańska 47** (`44614a4e`), **Hala Sportowa i Lodowisko ul. Toruńska 59** (`6a689c59`) | [`park.paymove.io/67fa0d96…`](https://park.paymove.io/67fa0d96-a482-4567-b71c-d24e164b6def) |
| **Poznań** | **3** | **Poznań ZOO** (osobowe `2a3e32e1` i autobusy `17cd38f8`), **ul. Dymka — WEIP** (`fa079b39`) | [`park.paymove.io/2a3e32e1…`](https://park.paymove.io/2a3e32e1-c1f0-4a8e-9a4a-8c340b71f377) |

<br />

<details>
<summary><strong>Kliknij, aby rozwinąć: Pełna tabela 197 parkingów miejskich, dworców PKP, aren i stref SPP (poza indeksem ulic Szczecina)</strong></summary>

<br />

| Miasto / Lokalizacja | Nazwa strefy / parkingu | Kod krótki | UUID produktu | Bezpośredni link |
| :--- | :--- | :--- | :--- | :--- |
| **Białka Tatrzańska** | Parking Stajanie | `6c47` | `5c69049e-8769-4aca-82d9-a79827496c47` | [`park.paymove.io/6c47`](https://park.paymove.io/6c47) |
| **Bolesławiec** | Bolesławiec, Chrobrego 35 – F458 | `—` | `9c7a2839-6a6f-4ac7-ba34-6303239b4f36` | [`park.paymove.io/9c7a2839`](https://park.paymove.io/9c7a2839-6a6f-4ac7-ba34-6303239b4f36) |
| **Bolesławiec** | Dworzec PKP Bolesławiec | `—` | `3a5efb46-afee-4654-8a6d-7ae247bd0814` | [`park.paymove.io/3a5efb46`](https://park.paymove.io/3a5efb46-afee-4654-8a6d-7ae247bd0814) |
| **Bydgoszcz** | Bydgoszcz, Gdańska 47 - F413 | `—` | `44614a4e-c4b7-4238-af99-8be4ce8f88c1` | [`park.paymove.io/44614a4e`](https://park.paymove.io/44614a4e-c4b7-4238-af99-8be4ce8f88c1) |
| **Bydgoszcz** | Dworzec PKP Bydgoszcz Główna | `—` | `67fa0d96-a482-4567-b71c-d24e164b6def` | [`park.paymove.io/67fa0d96`](https://park.paymove.io/67fa0d96-a482-4567-b71c-d24e164b6def) |
| **Bydgoszcz** | Parking przy halach sportowych i lodowisku ul. Toruńska 59 | `—` | `6a689c59-1744-49df-a067-e49541e1bb37` | [`park.paymove.io/6a689c59`](https://park.paymove.io/6a689c59-1744-49df-a067-e49541e1bb37) |
| **Chojnice** | I Strefa Płatnego Parkowania w Chojnicach | `8800` | `e3a5bc2a-b123-49e6-8241-6292beae8800` | [`park.paymove.io/8800`](https://park.paymove.io/8800) |
| **Czechowice-Dziedzice** | ul. Barlickiego 34 | `—` | `dee84323-13f8-4e69-8b59-bcf68ebf8a06` | [`park.paymove.io/dee84323`](https://park.paymove.io/dee84323-13f8-4e69-8b59-bcf68ebf8a06) |
| **Gdańsk** | Dworzec PKP Gdańsk Główny | `—` | `44f942bb-9d87-4d2b-a568-25884b386ec5` | [`park.paymove.io/44f942bb`](https://park.paymove.io/44f942bb-9d87-4d2b-a568-25884b386ec5) |
| **Gdańsk** | Ergo Arena - autokar, bus, kamper | `22a2` | `15deee04-9798-41ab-a355-d838896822a2` | [`park.paymove.io/22a2`](https://park.paymove.io/22a2) |
| **Gdańsk** | Ergo Arena - pojazd osobowy, jednoślad | `8898` | `a87db6c1-24a7-4716-9589-1627d9748898` | [`park.paymove.io/8898`](https://park.paymove.io/8898) |
| **Gdańsk** | Gdańsk, Polanki 117 - Parking zewnętrzny | `ecf6` | `3f2a9c1e-7d4b-4c8f-9a21-5d8e73a4ecf6` | [`park.paymove.io/ecf6`](https://park.paymove.io/ecf6) |
| **Gdańsk** | Mieszczańska | `0bb0` | `e56bef8a-5ea8-462c-8c43-6196e1eb0bb0` | [`park.paymove.io/0bb0`](https://park.paymove.io/0bb0) |
| **Gdańsk** | Smoluchowskiego | `c57f` | `85053be7-65d9-403b-b75f-83c25f15c57f` | [`park.paymove.io/c57f`](https://park.paymove.io/c57f) |
| **Gdańsk** | ul. Platynowa 2 | `—` | `9a39a5de-9476-4ae6-848d-8e099c2254da` | [`park.paymove.io/9a39a5de`](https://park.paymove.io/9a39a5de-9476-4ae6-848d-8e099c2254da) |
| **Gdynia** | Centrum Rodzinne Witawa - ul. Wielkokacka 2-4 | `—` | `3181a076-7089-4cd8-841a-52019fc8bcd9` | [`park.paymove.io/3181a076`](https://park.paymove.io/3181a076-7089-4cd8-841a-52019fc8bcd9) |
| **Gdynia** | Gdynia – Gniewska | `—` | `2384af30-62b7-466a-9d87-ea470df00256` | [`park.paymove.io/2384af30`](https://park.paymove.io/2384af30-62b7-466a-9d87-ea470df00256) |
| **Gniezno** | Dworzec PKP Gniezno | `—` | `4871a9f1-7250-4759-9192-4fd40acae5ac` | [`park.paymove.io/4871a9f1`](https://park.paymove.io/4871a9f1-7250-4759-9192-4fd40acae5ac) |
| **Gniezno** | SPP - PODSTREFA C (zielona) | `12cc` | `a80c0348-9890-4549-ba70-042ea5bc12cc` | [`park.paymove.io/12cc`](https://park.paymove.io/12cc) |
| **Goczałkowice-Zdrój** | ul. Uzdrowiskowa 41 | `—` | `c32a13b8-b0e2-44f4-b9fe-14d88c2b0feb` | [`park.paymove.io/c32a13b8`](https://park.paymove.io/c32a13b8-b0e2-44f4-b9fe-14d88c2b0feb) |
| **Gorzów Wielkopolski** | Gorzów Wielkopolski - Walczaka 23h | `11df` | `8e96dae5-6964-4a1a-b979-20a49c3611df` | [`park.paymove.io/11df`](https://park.paymove.io/11df) |
| **Gorzów Wielkopolski** | Gorzów Wielkopolski, Witosa 50 – F443 | `—` | `ccfb34ea-cc84-4e32-98da-34c97844bda9` | [`park.paymove.io/ccfb34ea`](https://park.paymove.io/ccfb34ea-cc84-4e32-98da-34c97844bda9) |
| **Grodzisk Mazowiecki** | ul. 11 Listopada 33 | `db54` | `5d60d671-ba10-41b6-bb31-31a16187db54` | [`park.paymove.io/db54`](https://park.paymove.io/db54) |
| **Hel** | Admirała Steyera - WEIP | `9d8a` | `d6a9077c-048f-446f-b4c9-2133dccb9d8a` | [`park.paymove.io/9d8a`](https://park.paymove.io/9d8a) |
| **Joannitów** | PKP Joannitów | `—` | `13f9bd2d-16cf-4629-a83f-a65245acb158` | [`park.paymove.io/13f9bd2d`](https://park.paymove.io/13f9bd2d-16cf-4629-a83f-a65245acb158) |
| **Joannitów** | PKP Joannitów - autokary | `—` | `2d1fe14c-58cc-44d9-978f-97fac81eaf64` | [`park.paymove.io/2d1fe14c`](https://park.paymove.io/2d1fe14c-58cc-44d9-978f-97fac81eaf64) |
| **Kalisz** | Wyszyńskiego 42A | `—` | `ad4122e1-8d8e-49f9-9191-aa0878db2fc6` | [`park.paymove.io/ad4122e1`](https://park.paymove.io/ad4122e1-8d8e-49f9-9191-aa0878db2fc6) |
| **Kartuzy** | Kolejowa 7a | `b042` | `17dfaa18-b9eb-40b9-9134-81c30c9bb042` | [`park.paymove.io/b042`](https://park.paymove.io/b042) |
| **Katowice** | Dworzec PKP Katowice | `c967` | `38ef2952-0538-449c-927c-5fb31721c967` | [`park.paymove.io/c967`](https://park.paymove.io/c967) |
| **Katowice** | Katowice Goeppert-Mayer PKP | `4964` | `f67041e5-55d1-4b06-8fc6-1b07ae844964` | [`park.paymove.io/4964`](https://park.paymove.io/4964) |
| **Kielce** | Kielce - Marii Konopnickiej | `—` | `cf16d5e4-26d8-43bf-a941-2b5dbeba7f52` | [`park.paymove.io/cf16d5e4`](https://park.paymove.io/cf16d5e4-26d8-43bf-a941-2b5dbeba7f52) |
| **Kielce** | Kielce - ul. Barwinek 29 | `—` | `f143e7c4-4fd5-4760-9f27-6365fb665da3` | [`park.paymove.io/f143e7c4`](https://park.paymove.io/f143e7c4-4fd5-4760-9f27-6365fb665da3) |
| **Kielce** | Spółdzielnia Mieszkaniowa Bocianek w Kielcach | `—` | `eae4af4a-2c57-47cf-90a2-4c7e9fa1dacc` | [`park.paymove.io/eae4af4a`](https://park.paymove.io/eae4af4a-2c57-47cf-90a2-4c7e9fa1dacc) |
| **Kielce** | ul. Bodzentyńska 15 | `—` | `a8c8e27c-369f-4b24-926e-0858262697d3` | [`park.paymove.io/a8c8e27c`](https://park.paymove.io/a8c8e27c-369f-4b24-926e-0858262697d3) |
| **Kielce** | ul. Szajnowicza-Iwanowa 17 | `—` | `3eaebeb7-d33d-4d8b-b57e-ab21ef21b4fe` | [`park.paymove.io/3eaebeb7`](https://park.paymove.io/3eaebeb7-d33d-4d8b-b57e-ab21ef21b4fe) |
| **Kielce** | ul. Szydłówek Górny 6 i 10 | `—` | `2fd0db3a-e3db-48bf-a72c-936d32ceca1b` | [`park.paymove.io/2fd0db3a`](https://park.paymove.io/2fd0db3a-e3db-48bf-a72c-936d32ceca1b) |
| **Kielce** | ul. Wapiennikowa - SAMOCHÓD OSOBOWY | `cc4f` | `316bf50e-1986-4672-9805-bf92361ecc4f` | [`park.paymove.io/cc4f`](https://park.paymove.io/cc4f) |
| **Kielce** | ul. Warszawska 147 | `—` | `12f138a9-44bb-45c7-9e14-3c89e8ac1a0b` | [`park.paymove.io/12f138a9`](https://park.paymove.io/12f138a9-44bb-45c7-9e14-3c89e8ac1a0b) |
| **Kielce** | ul. Warszawska 218d | `—` | `b48ccbf6-29d5-4107-b329-3bffd12db9f6` | [`park.paymove.io/b48ccbf6`](https://park.paymove.io/b48ccbf6-29d5-4107-b329-3bffd12db9f6) |
| **Kielce** | ul. Ćwiklińskiej 2 | `—` | `33bb97d7-3c3f-4da7-97d3-5cc1e1a00775` | [`park.paymove.io/33bb97d7`](https://park.paymove.io/33bb97d7-3c3f-4da7-97d3-5cc1e1a00775) |
| **Konstantynów** | Fryzjer Galeria Konstantynów | `—` | `d186ee98-93f9-46b3-82e4-ff1dc0bbb2c4` | [`park.paymove.io/d186ee98`](https://park.paymove.io/d186ee98-93f9-46b3-82e4-ff1dc0bbb2c4) |
| **Koszalin** | Koszalin, Karłowicza 28 – F439 | `—` | `5cfccfc9-4389-4924-8832-a560b1a07f7d` | [`park.paymove.io/5cfccfc9`](https://park.paymove.io/5cfccfc9-4389-4924-8832-a560b1a07f7d) |
| **Koszalin** | Koszalin, Łużycka 34 – F438 | `—` | `27bdb73c-b660-40fe-b4bf-d0aba09be495` | [`park.paymove.io/27bdb73c`](https://park.paymove.io/27bdb73c-b660-40fe-b4bf-d0aba09be495) |
| **Kołobrzeg** | Dworzec PKP Kołobrzeg - autokary | `—` | `d53d2499-5f20-4fa3-bca2-0fcb2674dcd7` | [`park.paymove.io/d53d2499`](https://park.paymove.io/d53d2499-5f20-4fa3-bca2-0fcb2674dcd7) |
| **Kołobrzeg** | Dworzec PKP Kołobrzeg - samochody osobowe | `—` | `e60cbb6f-cb19-4392-90dd-8d74c50ac764` | [`park.paymove.io/e60cbb6f`](https://park.paymove.io/e60cbb6f-cb19-4392-90dd-8d74c50ac764) |
| **Kołobrzeg** | Parking Amfiteatr | `—` | `79cd1183-ed5f-4f38-975f-e5efed861b35` | [`park.paymove.io/79cd1183`](https://park.paymove.io/79cd1183-ed5f-4f38-975f-e5efed861b35) |
| **Kołobrzeg** | Parking Bałtycka (bus, autobus) | `—` | `b32e5ee6-ee9b-4a76-b18c-f71149d87317` | [`park.paymove.io/b32e5ee6`](https://park.paymove.io/b32e5ee6-ee9b-4a76-b18c-f71149d87317) |
| **Kołobrzeg** | Parking Bałtycka - samochody osobowe | `—` | `0742d9be-c28f-4f98-bedc-791ec03fc4c9` | [`park.paymove.io/0742d9be`](https://park.paymove.io/0742d9be-c28f-4f98-bedc-791ec03fc4c9) |
| **Kołobrzeg** | Parking Hala Milenium | `—` | `cc63af6c-4ae5-4403-ad83-9cfed7461e8d` | [`park.paymove.io/cc63af6c`](https://park.paymove.io/cc63af6c-4ae5-4403-ad83-9cfed7461e8d) |
| **Kołobrzeg** | Parking Kamienna (bus, autobus) | `—` | `902b6b68-65fe-4c36-8864-1af51e899212` | [`park.paymove.io/902b6b68`](https://park.paymove.io/902b6b68-65fe-4c36-8864-1af51e899212) |
| **Kołobrzeg** | Parking Kamienna - samochody osobowe | `—` | `9e3a3939-b820-494b-92f7-140cb9335efc` | [`park.paymove.io/9e3a3939`](https://park.paymove.io/9e3a3939-b820-494b-92f7-140cb9335efc) |
| **Kołobrzeg** | Parking Marina Solna | `—` | `53436f1c-c1d9-4454-a716-c833d1a1b367` | [`park.paymove.io/53436f1c`](https://park.paymove.io/53436f1c-c1d9-4454-a716-c833d1a1b367) |
| **Kołobrzeg** | Parking Mazowiecka Park | `—` | `f15023cc-a42f-4c9a-af96-6a8f0a6d8d3d` | [`park.paymove.io/f15023cc`](https://park.paymove.io/f15023cc-a42f-4c9a-af96-6a8f0a6d8d3d) |
| **Kołobrzeg** | Parking Nadmorskie Tarasy | `—` | `5f73d6bb-52ce-4950-910c-ee6b5addd657` | [`park.paymove.io/5f73d6bb`](https://park.paymove.io/5f73d6bb-52ce-4950-910c-ee6b5addd657) |
| **Kołobrzeg** | Parking Okopowa | `—` | `e0293419-dee7-413a-91fa-ca098fd959ac` | [`park.paymove.io/e0293419`](https://park.paymove.io/e0293419-dee7-413a-91fa-ca098fd959ac) |
| **Kołobrzeg** | Parking Port Rybacki | `—` | `6e4f833e-38db-4b81-9e14-dffd585d7adb` | [`park.paymove.io/6e4f833e`](https://park.paymove.io/6e4f833e-38db-4b81-9e14-dffd585d7adb) |
| **Kołobrzeg** | Parking Restauracja Aqua | `—` | `8b1b2cd6-f32c-4e3b-8480-fb2fa320930a` | [`park.paymove.io/8b1b2cd6`](https://park.paymove.io/8b1b2cd6-f32c-4e3b-8480-fb2fa320930a) |
| **Kołobrzeg** | Parking Solna | `—` | `ee748825-ce65-4b18-a480-e8baf303796a` | [`park.paymove.io/ee748825`](https://park.paymove.io/ee748825-ce65-4b18-a480-e8baf303796a) |
| **Kołobrzeg** | Parking Unii Lubelskiej | `—` | `3b68caab-7cae-4756-b0e5-f7ab4935f2f3` | [`park.paymove.io/3b68caab`](https://park.paymove.io/3b68caab-7cae-4756-b0e5-f7ab4935f2f3) |
| **Kołobrzeg** | Parking Śliwińskiego | `—` | `6af5eec6-6be2-49c3-81d4-932efb1ed3bb` | [`park.paymove.io/6af5eec6`](https://park.paymove.io/6af5eec6-6be2-49c3-81d4-932efb1ed3bb) |
| **Kościerzyna** | Kapliczna | `—` | `c6575f78-63e2-41b1-b31c-414ccf8209a5` | [`park.paymove.io/c6575f78`](https://park.paymove.io/c6575f78-63e2-41b1-b31c-414ccf8209a5) |
| **Kościerzyna** | Kościerzyna - 3 Maja | `—` | `e2ba5048-6f6a-4ede-b48f-526e389bc3ca` | [`park.paymove.io/e2ba5048`](https://park.paymove.io/e2ba5048-6f6a-4ede-b48f-526e389bc3ca) |
| **Kościerzyna** | Kościerzyna - Lubomira Szopińskiego | `—` | `7858e1dd-e7ec-4bc4-9910-440003a71469` | [`park.paymove.io/7858e1dd`](https://park.paymove.io/7858e1dd-e7ec-4bc4-9910-440003a71469) |
| **Kościerzyna** | Kościerzyna - Strefa Płatnego Parkowania | `1389` | `426bfeb3-0f96-4e9a-9657-9109db151389` | [`park.paymove.io/1389`](https://park.paymove.io/1389) |
| **Kościerzyna** | Kościerzyna – AQUA Centrum | `—` | `983789df-0e15-4143-a380-f1b1da42c034` | [`park.paymove.io/983789df`](https://park.paymove.io/983789df-0e15-4143-a380-f1b1da42c034) |
| **Kościerzyna** | Świętojańska | `—` | `0c61d988-33db-4115-9cf0-bb07f7147595` | [`park.paymove.io/0c61d988`](https://park.paymove.io/0c61d988-33db-4115-9cf0-bb07f7147595) |
| **Kraków** | Al. Pokoju 46 | `7ddd` | `fb2f0370-387b-483f-9702-c7092e077ddd` | [`park.paymove.io/7ddd`](https://park.paymove.io/7ddd) |
| **Kraków** | Garbarska 18b - PARKEMI | `c231` | `f42b5053-36b9-4e62-910f-18c5cba8c231` | [`park.paymove.io/c231`](https://park.paymove.io/c231) |
| **Kraków** | Kraków - os. Kombatantów - PARKEMI | `0a97` | `f3249ca3-2607-4b67-9faa-897ca3910a97` | [`park.paymove.io/0a97`](https://park.paymove.io/0a97) |
| **Kraków** | SM Podwawelska - DZP | `cbcc` | `0cc1ae76-ed3c-4bdf-8626-ceb1d8b1cbcc` | [`park.paymove.io/cbcc`](https://park.paymove.io/cbcc) |
| **Kraków** | ul. Aktorów 1 i Wizjonerów 7 - bramka | `—` | `d9ed4b59-f9d4-48fb-932a-26fc94e756fc` | [`park.paymove.io/d9ed4b59`](https://park.paymove.io/d9ed4b59-f9d4-48fb-932a-26fc94e756fc) |
| **Krościenko nad Dunajcem** | Parking Trzy Korony | `15e0` | `243b08a3-302c-4ee2-af7c-1308b27215e0` | [`park.paymove.io/15e0`](https://park.paymove.io/15e0) |
| **Kutno** | Parking Miejski Kutno - Pl. Wolności | `6253` | `044a58cf-ed7a-412f-b5c6-8e7cff646253` | [`park.paymove.io/6253`](https://park.paymove.io/6253) |
| **Lubin** | ul. Kopernika 17 | `—` | `2df5a19a-e411-4789-aa42-634cdb57e2c6` | [`park.paymove.io/2df5a19a`](https://park.paymove.io/2df5a19a-e411-4789-aa42-634cdb57e2c6) |
| **Lublin** | Lublin Okopowa PKP | `6024` | `604ed48e-9356-41f2-aa33-e2b1c4476024` | [`park.paymove.io/6024`](https://park.paymove.io/6024) |
| **Lublin** | S.M. Rudnik | `4d42` | `ad061a60-6928-4598-a5b7-d0b31ee24d42` | [`park.paymove.io/4d42`](https://park.paymove.io/4d42) |
| **Lublin** | Stadionowa 1 - autokar | `378a` | `99ef9ab2-b69f-4ba9-a432-692052f7378a` | [`park.paymove.io/378a`](https://park.paymove.io/378a) |
| **Lublin** | Stadionowa 1 - samochód osobowy | `39f3` | `03e14771-3334-4454-b49f-06f96f6639f3` | [`park.paymove.io/39f3`](https://park.paymove.io/39f3) |
| **Lubrza** | ul. Świebodzińska 52A | `—` | `197937e8-062c-49ad-aa6d-1541f132db48` | [`park.paymove.io/197937e8`](https://park.paymove.io/197937e8-062c-49ad-aa6d-1541f132db48) |
| **Malbork** | Malbork · TRIATLON - WEIP | `—` | `d86a2e50-8287-4e38-8196-cdd6a4838843` | [`park.paymove.io/d86a2e50`](https://park.paymove.io/d86a2e50-8287-4e38-8196-cdd6a4838843) |
| **Mikoszewo** | Bursztynowa - samochody osobowe | `2f29` | `721bbd50-2296-409a-a65b-21dd4e932f29` | [`park.paymove.io/2f29`](https://park.paymove.io/2f29) |
| **Mikołów** | ul. Miarki 11 | `—` | `2831668a-0b3b-4aaa-9980-7c43adb60ddc` | [`park.paymove.io/2831668a`](https://park.paymove.io/2831668a-0b3b-4aaa-9980-7c43adb60ddc) |
| **Międzyrzecz** | Międzyrzecz - Plac Powstańców Wielkopolskich 4 | `—` | `8079977e-a48a-4752-afbb-91db3ffb2d8b` | [`park.paymove.io/8079977e`](https://park.paymove.io/8079977e-a48a-4752-afbb-91db3ffb2d8b) |
| **Międzyrzecz** | ul. Chrobrego 2 i 4 | `—` | `5fe33b15-7323-4ccb-ba78-3206c7dee05a` | [`park.paymove.io/5fe33b15`](https://park.paymove.io/5fe33b15-7323-4ccb-ba78-3206c7dee05a) |
| **Namysłów** | SPP w Namysłowie - Strefa B | `5343` | `cb0e6faa-154b-4762-80ed-7aeed4075343` | [`park.paymove.io/5343`](https://park.paymove.io/5343) |
| **Niepołomice** | ul. Targowa 10 | `—` | `e5c3b5c7-ea03-4d79-8a30-cdf4f1abe11b` | [`park.paymove.io/e5c3b5c7`](https://park.paymove.io/e5c3b5c7-ea03-4d79-8a30-cdf4f1abe11b) |
| **Oleśnica** | ul. Sikorskiego 6 | `—` | `444cef10-15cb-46b7-aca8-b9520ee0d7cd` | [`park.paymove.io/444cef10`](https://park.paymove.io/444cef10-15cb-46b7-aca8-b9520ee0d7cd) |
| **Olsztyn** | Olsztyn - Warmińsko-Mazurskie Centrum Chorób Płuc w Olsztynie | `—` | `741db750-f088-4e1a-8610-f67c75013059` | [`park.paymove.io/741db750`](https://park.paymove.io/741db750-f088-4e1a-8610-f67c75013059) |
| **Olsztyn** | Olsztyn - Wojewódzki Zespół Lecznictwa Psychiatrycznego w Olsztynie | `—` | `dcf3595f-ea22-4c14-80ac-bd3b87c5f34c` | [`park.paymove.io/dcf3595f`](https://park.paymove.io/dcf3595f-ea22-4c14-80ac-bd3b87c5f34c) |
| **Olsztyn** | Olsztyn – Żołnierska 16 | `—` | `4af8ec0f-bd7a-4c29-bb60-c808f703b79b` | [`park.paymove.io/4af8ec0f`](https://park.paymove.io/4af8ec0f-bd7a-4c29-bb60-c808f703b79b) |
| **Olsztyn** | Olsztyn – Żołnierska 19A | `—` | `caa890bc-5644-448e-95f5-16decb1f8007` | [`park.paymove.io/caa890bc`](https://park.paymove.io/caa890bc-5644-448e-95f5-16decb1f8007) |
| **Olsztyn** | ul. Kołobrzeska 50 | `—` | `c3aa2cb9-1a1e-4a76-842f-82b047b676fb` | [`park.paymove.io/c3aa2cb9`](https://park.paymove.io/c3aa2cb9-1a1e-4a76-842f-82b047b676fb) |
| **Opole** | Dworzec PKP Opole Główne | `—` | `cc582c91-9d21-4010-901a-89c9a0e51ee8` | [`park.paymove.io/cc582c91`](https://park.paymove.io/cc582c91-9d21-4010-901a-89c9a0e51ee8) |
| **Ostrów Wielkopolski** | Dworzec PKP Ostrów Wielkopolski | `caa0` | `c459bc73-dbc9-4adb-ae0a-cb7f1207caa0` | [`park.paymove.io/caa0`](https://park.paymove.io/caa0) |
| **Pisz** | ul. Warszawska | `—` | `50bc6b98-6497-424a-8f17-04411afeac54` | [`park.paymove.io/50bc6b98`](https://park.paymove.io/50bc6b98-6497-424a-8f17-04411afeac54) |
| **Police** | Grzybowa 1 | `—` | `413c6ca4-2b6c-413b-8449-2d48e358dbf3` | [`park.paymove.io/413c6ca4`](https://park.paymove.io/413c6ca4-2b6c-413b-8449-2d48e358dbf3) |
| **Poznań** | Poznań - Dymka - WEIP - abonament 30 dni | `—` | `fa079b39-01c6-40b7-bba5-3be0db79c369` | [`park.paymove.io/fa079b39`](https://park.paymove.io/fa079b39-01c6-40b7-bba5-3be0db79c369) |
| **Poznań** | Poznań ZOO - autobusy | `—` | `17cd38f8-4cbc-4920-b0b6-b094eec4df0b` | [`park.paymove.io/17cd38f8`](https://park.paymove.io/17cd38f8-4cbc-4920-b0b6-b094eec4df0b) |
| **Poznań** | Poznań ZOO - samochody osobowe | `—` | `2a3e32e1-33a8-46cb-8a5c-358979267b43` | [`park.paymove.io/2a3e32e1`](https://park.paymove.io/2a3e32e1-33a8-46cb-8a5c-358979267b43) |
| **Przasnysz** | Samodzielny Publiczny ZOZ, ul. Sadowa 9 | `—` | `0d262f79-07de-46cf-8626-810a5654eaf9` | [`park.paymove.io/0d262f79`](https://park.paymove.io/0d262f79-07de-46cf-8626-810a5654eaf9) |
| **Pszczyna** | Pszczyna - Dworcowa 27 | `—` | `c4a59507-4344-49ec-837f-89e9c4c8a4d3` | [`park.paymove.io/c4a59507`](https://park.paymove.io/c4a59507-4344-49ec-837f-89e9c4c8a4d3) |
| **Pszczyna** | ul. Szymanowskiego 23 | `—` | `9918c630-827f-4ab7-a396-94792d39e3b1` | [`park.paymove.io/9918c630`](https://park.paymove.io/9918c630-827f-4ab7-a396-94792d39e3b1) |
| **Puck** | 1-go Maja SPP | `—` | `176892d9-91a8-4f26-82de-87a70b5a65f5` | [`park.paymove.io/176892d9`](https://park.paymove.io/176892d9-91a8-4f26-82de-87a70b5a65f5) |
| **Puck** | 10-go Lutego PP | `—` | `1065c82e-57cf-468d-8f8c-dc56210505c5` | [`park.paymove.io/1065c82e`](https://park.paymove.io/1065c82e-57cf-468d-8f8c-dc56210505c5) |
| **Puck** | 10-go Lutego SPP | `—` | `5ad7d94b-5e12-41ee-8def-a073aca2be65` | [`park.paymove.io/5ad7d94b`](https://park.paymove.io/5ad7d94b-5e12-41ee-8def-a073aca2be65) |
| **Puck** | Aleja Ceynowy SPP | `—` | `1fa06bb4-6049-49ac-92bf-533a04045eae` | [`park.paymove.io/1fa06bb4`](https://park.paymove.io/1fa06bb4-6049-49ac-92bf-533a04045eae) |
| **Puck** | Aleja Lipowa SPP | `—` | `bf1b2162-5f1e-41af-860d-a74791dd699b` | [`park.paymove.io/bf1b2162`](https://park.paymove.io/bf1b2162-5f1e-41af-860d-a74791dd699b) |
| **Puck** | Elizy Orzeszkowej przy parku SPP | `—` | `d41a9195-3d05-4206-8ca5-aa601a67638a` | [`park.paymove.io/d41a9195`](https://park.paymove.io/d41a9195-3d05-4206-8ca5-aa601a67638a) |
| **Puck** | Elizy Orzeszkowej Starostwo Powiatowe SPP | `—` | `493cf505-0cc8-421b-b1ed-b297afdae47c` | [`park.paymove.io/493cf505`](https://park.paymove.io/493cf505-0cc8-421b-b1ed-b297afdae47c) |
| **Puck** | Judyckiego SPP | `—` | `6569e9b0-e70b-4ed6-83f9-c9630c3f0f25` | [`park.paymove.io/6569e9b0`](https://park.paymove.io/6569e9b0-e70b-4ed6-83f9-c9630c3f0f25) |
| **Puck** | Nowy Świat PP | `—` | `035b5516-007b-464a-bbf3-d3b273f466fa` | [`park.paymove.io/035b5516`](https://park.paymove.io/035b5516-007b-464a-bbf3-d3b273f466fa) |
| **Puck** | Plac Obrońców Wybrzeża SPP | `—` | `f0b1c89a-cf1e-4f89-a8b0-e00d84bbe9f3` | [`park.paymove.io/f0b1c89a`](https://park.paymove.io/f0b1c89a-cf1e-4f89-a8b0-e00d84bbe9f3) |
| **Puck** | Róg ul. 1-go Maja i Al. Lipowej PP | `—` | `7aa4ae37-0181-4568-903b-8176322ab959` | [`park.paymove.io/7aa4ae37`](https://park.paymove.io/7aa4ae37-0181-4568-903b-8176322ab959) |
| **Puck** | Sambora SPP | `—` | `5ea8bef5-beee-40b8-8352-69c450f9585e` | [`park.paymove.io/5ea8bef5`](https://park.paymove.io/5ea8bef5-beee-40b8-8352-69c450f9585e) |
| **Puck** | Wałowa PP | `—` | `af6d8495-881e-44fb-ae5f-a290dcfe2559` | [`park.paymove.io/af6d8495`](https://park.paymove.io/af6d8495-881e-44fb-ae5f-a290dcfe2559) |
| **Puck** | Wałowa SPP | `—` | `65281ca7-cefa-4a69-830a-cb96f5e124cb` | [`park.paymove.io/65281ca7`](https://park.paymove.io/65281ca7-cefa-4a69-830a-cb96f5e124cb) |
| **Puck** | Wojska Polskiego SPP | `—` | `68b94840-b299-43fc-95fc-d2c118ea3404` | [`park.paymove.io/68b94840`](https://park.paymove.io/68b94840-b299-43fc-95fc-d2c118ea3404) |
| **Puck** | Zamkowa PP | `—` | `9718b0a9-5a59-4899-adc2-f3427b2b4f81` | [`park.paymove.io/9718b0a9`](https://park.paymove.io/9718b0a9-5a59-4899-adc2-f3427b2b4f81) |
| **Radom** | ul. Wyścigowa 41 | `—` | `4fd1b936-39f0-43df-98e3-a0dfd422e149` | [`park.paymove.io/4fd1b936`](https://park.paymove.io/4fd1b936-39f0-43df-98e3-a0dfd422e149) |
| **Radzyń Podlaski** | Strefa Płatnego Parkowania w Radzyniu Podlaskim | `f5f6` | `57efb9de-2eb7-4e9e-ae5e-d3291806f5f6` | [`park.paymove.io/f5f6`](https://park.paymove.io/f5f6) |
| **Ruda Śląska** | ul. Piłsudskiego 16 | `—` | `a4e6a2d8-0172-4e4b-9d5c-14af5b79b0e4` | [`park.paymove.io/a4e6a2d8`](https://park.paymove.io/a4e6a2d8-0172-4e4b-9d5c-14af5b79b0e4) |
| **Ruda Śląska** | ul. Teatralna 7 | `—` | `dede84f9-bc3d-464e-85d2-40bec9662bb4` | [`park.paymove.io/dede84f9`](https://park.paymove.io/dede84f9-bc3d-464e-85d2-40bec9662bb4) |
| **Rybnik** | Pniowska (plaża) | `18f8` | `946c7ce4-1671-4c93-8cbe-c4c2711718f8` | [`park.paymove.io/18f8`](https://park.paymove.io/18f8) |
| **Rybnik** | Pniowska (za groblą) | `91d5` | `0fc38fdd-3e24-4337-9012-e4aa4f8a91d5` | [`park.paymove.io/91d5`](https://park.paymove.io/91d5) |
| **Rybnik** | Rudzka (Pniowiec) | `2f92` | `6520b9b6-a96a-4244-8e7b-511701e02f92` | [`park.paymove.io/2f92`](https://park.paymove.io/2f92) |
| **Rybnik** | Strefa Płatnego Parkowania w Rybniku | `fe6e` | `3e2d245b-c652-4616-a5cb-41a3abd7fe6e` | [`park.paymove.io/fe6e`](https://park.paymove.io/fe6e) |
| **Rybnik** | Sławików | `d2bf` | `29c8ef57-a5be-4f15-8e55-6968a6ddd2bf` | [`park.paymove.io/d2bf`](https://park.paymove.io/d2bf) |
| **Sopot** | Ogrodowa 6a | `81c4` | `a20497a7-df2a-4c83-9d77-ebc4679581c4` | [`park.paymove.io/81c4`](https://park.paymove.io/81c4) |
| **Sopot** | Sopot Tenis Klub Osiedlowa | `—` | `489d404d-c4fa-42e2-b230-a3014e1323c1` | [`park.paymove.io/489d404d`](https://park.paymove.io/489d404d-c4fa-42e2-b230-a3014e1323c1) |
| **Sopot** | Sopot Tenis Klub Tenisowa | `—` | `984399af-fdcb-45d8-856f-b797a076ab5c` | [`park.paymove.io/984399af`](https://park.paymove.io/984399af-fdcb-45d8-856f-b797a076ab5c) |
| **Sopot** | Sopot – Sofitel Grand Sopot | `—` | `09d6ce12-5331-4fcf-9edb-103d89845683` | [`park.paymove.io/09d6ce12`](https://park.paymove.io/09d6ce12-5331-4fcf-9edb-103d89845683) |
| **Stalowa Wola** | Okulickiego 2 | `22a0` | `e8096b57-84bd-4dc4-8760-63e7623b22a0` | [`park.paymove.io/22a0`](https://park.paymove.io/22a0) |
| **Stalowa Wola** | Okulickiego 2 - abonament 30 dni | `9d29` | `0112dcb1-a80c-4445-9805-0fd7478b9d29` | [`park.paymove.io/9d29`](https://park.paymove.io/9d29) |
| **Szczecin** | Płatny Parking Niestrzeżony pod Trasą Zamkową | `—` | `86061819-bfbb-4ecd-a098-d97c90ac280b` | [`park.paymove.io/86061819…`](https://park.paymove.io/86061819-bfbb-4ecd-a098-d97c90ac280b) |
| **Szczecin** | Nabrzeże Wieleckie Trasa Zamkowa | `lx4h` | `1f2e27cf-0a32-4fb6-9152-b38f4e050b97` | [`park.paymove.io/lx4h…`](https://park.paymove.io/lx4h) |
| **Szczytno** | Galeria Mazur | `—` | `00dfe67a-c1f5-4829-8633-d7c3b05f5011` | [`park.paymove.io/00dfe67a`](https://park.paymove.io/00dfe67a-c1f5-4829-8633-d7c3b05f5011) |
| **Sztutowo** | Morska - samochody osobowe | `9990` | `3d78d758-937d-4825-a124-f2a750f29990` | [`park.paymove.io/9990`](https://park.paymove.io/9990) |
| **Słupsk** | Słupsk, 11 Listopada – F440 | `—` | `1a15224b-bcae-484d-b0a7-786715a9805a` | [`park.paymove.io/1a15224b`](https://park.paymove.io/1a15224b-bcae-484d-b0a7-786715a9805a) |
| **Słupsk** | Słupsk, Westerplatte 64 – F430 | `—` | `9b6636d1-d927-41e8-9e64-6609758c62cb` | [`park.paymove.io/9b6636d1`](https://park.paymove.io/9b6636d1-d927-41e8-9e64-6609758c62cb) |
| **Tarnów** | Dworzec PKP Tarnów | `—` | `d4321a82-70b1-4b16-9a92-11897f1bf040` | [`park.paymove.io/d4321a82`](https://park.paymove.io/d4321a82-70b1-4b16-9a92-11897f1bf040) |
| **Tarnów** | Tarnów – Dąbrowskiego | `—` | `fbb43aeb-bdd2-4452-b653-b4e43b0559ad` | [`park.paymove.io/fbb43aeb`](https://park.paymove.io/fbb43aeb-bdd2-4452-b653-b4e43b0559ad) |
| **Toruń** | Arena Toruń - 30 dni motocykl | `—` | `7a67966e-7101-422c-8b3e-eb9a2b616b89` | [`park.paymove.io/7a67966e`](https://park.paymove.io/7a67966e-7101-422c-8b3e-eb9a2b616b89) |
| **Toruń** | Arena Toruń - 30 dni samochód osobowy | `—` | `9dccd4e8-25e8-404c-8210-d86a0b151347` | [`park.paymove.io/9dccd4e8`](https://park.paymove.io/9dccd4e8-25e8-404c-8210-d86a0b151347) |
| **Toruń** | Arena Toruń - autokary | `—` | `6dcc27d3-7829-4276-9021-4a9b019b9952` | [`park.paymove.io/6dcc27d3`](https://park.paymove.io/6dcc27d3-7829-4276-9021-4a9b019b9952) |
| **Toruń** | Arena Toruń - samochody osobowe | `—` | `0804132b-0d27-4fb5-b1a8-e51be65b0f09` | [`park.paymove.io/0804132b`](https://park.paymove.io/0804132b-0d27-4fb5-b1a8-e51be65b0f09) |
| **Toruń** | Toruń, Podgórska 12a - F429 | `—` | `c41a13a8-8843-4ae1-b804-1a0f1337ae32` | [`park.paymove.io/c41a13a8`](https://park.paymove.io/c41a13a8-8843-4ae1-b804-1a0f1337ae32) |
| **Trzebinia** | Trzebinia - Ośrodek Rekreacyjny Chechło - posiadacze karty trzebińskiej | `6a16` | `50e69696-fa3e-4cf3-b0b4-548ab6d26a16` | [`park.paymove.io/6a16`](https://park.paymove.io/6a16) |
| **Warszawa** | Dworzec PKP Warszawa Centralna | `—` | `50d4cd96-bf7d-47b9-a8b6-df636de75357` | [`park.paymove.io/50d4cd96`](https://park.paymove.io/50d4cd96-bf7d-47b9-a8b6-df636de75357) |
| **Warszawa** | Dworzec PKP Warszawa Gdańska | `—` | `adaeac32-8140-4655-9e37-202987f1b553` | [`park.paymove.io/adaeac32`](https://park.paymove.io/adaeac32-8140-4655-9e37-202987f1b553) |
| **Warszawa** | Dworzec PKP Warszawa Wschodnia | `—` | `20afc570-e99b-4902-b4e2-be9c747c84ef` | [`park.paymove.io/20afc570`](https://park.paymove.io/20afc570-e99b-4902-b4e2-be9c747c84ef) |
| **Warszawa** | Dworzec PKP Warszawa Wschodnia ul. Lubelska (parking długoterminowy) | `16ce` | `1364b589-e3f8-477a-beb8-f53219e116ce` | [`park.paymove.io/16ce`](https://park.paymove.io/16ce) |
| **Warszawa** | Dworzec PKP Warszawa Wschodnia ul. Lubelska (parking krótkoterminowy) | `091a` | `c38a2611-d1df-49cb-8545-062bbc64091a` | [`park.paymove.io/091a`](https://park.paymove.io/091a) |
| **Warszawa** | Dworzec PKP Warszawa Wschodnia ul. Lubelska (parking krótkoterminowy) - autobusy | `767f` | `978a2324-5097-4496-9ea1-92b13d89767f` | [`park.paymove.io/767f`](https://park.paymove.io/767f) |
| **Warszawa** | Parking Demonstracyjny EuroPark | `—` | `8cae0b60-d9fd-462f-854b-38fa899e6ff5` | [`park.paymove.io/8cae0b60`](https://park.paymove.io/8cae0b60-d9fd-462f-854b-38fa899e6ff5) |
| **Warszawa** | Warszawa Towarowa PKP | `84f3` | `6bad6b0d-88a3-4044-8108-1e584a5b84f3` | [`park.paymove.io/84f3`](https://park.paymove.io/84f3) |
| **Wejherowo** | Szpital Specjalistyczny im. F. Ceynowy | `—` | `67dfa69e-acda-4f16-8ee3-874c8eee65bb` | [`park.paymove.io/67dfa69e`](https://park.paymove.io/67dfa69e-acda-4f16-8ee3-874c8eee65bb) |
| **Wieliczka** | FITPARKING P1 Camper/Mały Bus | `—` | `c77d8010-2a10-43ce-86f1-08852cb27e27` | [`park.paymove.io/c77d8010`](https://park.paymove.io/c77d8010-2a10-43ce-86f1-08852cb27e27) |
| **Wieliczka** | FITPARKING P1 Wieliczka | `—` | `41610c0e-51d9-4e7f-9759-8edb750f159f` | [`park.paymove.io/41610c0e`](https://park.paymove.io/41610c0e-51d9-4e7f-9759-8edb750f159f) |
| **Wieliczka** | FITPARKING P2 Wieliczka | `—` | `37ad6a3f-77a8-4a78-adc3-62bb5da1d0c7` | [`park.paymove.io/37ad6a3f`](https://park.paymove.io/37ad6a3f-77a8-4a78-adc3-62bb5da1d0c7) |
| **Wieliczka** | Goliana 10 | `0fbc` | `57063a2c-904c-4d0d-9632-8d579ae80fbc` | [`park.paymove.io/0fbc`](https://park.paymove.io/0fbc) |
| **Wieliczka** | Niecała (Cmentarz) | `0164` | `4203b06c-381e-4f83-99af-735404150164` | [`park.paymove.io/0164`](https://park.paymove.io/0164) |
| **Wieliczka** | Słowackiego 12 | `9759` | `0c3e540f-fd6a-4935-9463-19ac9ead9759` | [`park.paymove.io/9759`](https://park.paymove.io/9759) |
| **Wieliczka** | Słowackiego 3 | `8254` | `92205db1-e340-46ab-8612-03e762ab8254` | [`park.paymove.io/8254`](https://park.paymove.io/8254) |
| **Wiązowna** | CH JARTON - bramka | `—` | `c3a160ab-1ca0-465e-8147-709e0576d269` | [`park.paymove.io/c3a160ab`](https://park.paymove.io/c3a160ab-1ca0-465e-8147-709e0576d269) |
| **Wiązowna** | ul. Lubelska 78 | `—` | `0664c524-05f7-4c00-b7ee-c3eddc53bdca` | [`park.paymove.io/0664c524`](https://park.paymove.io/0664c524-05f7-4c00-b7ee-c3eddc53bdca) |
| **Wodzisław Śląski** | Parking Miejski Niestrzeżony w Wodzisławiu Śląskim | `cc87` | `4c6c412e-9c4a-4b88-800c-1938716bcc87` | [`park.paymove.io/cc87`](https://park.paymove.io/cc87) |
| **Wodzisław Śląski** | Strefa Płatnego Parkowania w Wodzisławiu Śląskim | `2f3f` | `4853553c-3e35-4bbc-8532-0121682d2f3f` | [`park.paymove.io/2f3f`](https://park.paymove.io/2f3f) |
| **Wrocław** | Dworzec PKP Wrocław Główny | `—` | `6bf749b6-776d-402b-a6a8-dfbfe0d519cc` | [`park.paymove.io/6bf749b6`](https://park.paymove.io/6bf749b6-776d-402b-a6a8-dfbfe0d519cc) |
| **Wrocław** | Dworzec PKP Wrocław Główny (Parking podziemny) | `—` | `2434b2db-4665-4267-9f5e-c50133ff0595` | [`park.paymove.io/2434b2db`](https://park.paymove.io/2434b2db-4665-4267-9f5e-c50133ff0595) |
| **Wrocław** | TARCZYŃSKI ARENA - broadcast | `—` | `c2d42a55-e966-4611-b22a-d60736f8a133` | [`park.paymove.io/c2d42a55`](https://park.paymove.io/c2d42a55-e966-4611-b22a-d60736f8a133) |
| **Wrocław** | TARCZYŃSKI ARENA - Camper Park 4 osoby bez dostępu do prądu | `—` | `704f076a-60b8-4fe7-b980-3df5c6f9b751` | [`park.paymove.io/704f076a`](https://park.paymove.io/704f076a-60b8-4fe7-b980-3df5c6f9b751) |
| **Wrocław** | TARCZYŃSKI ARENA - Camper Park 4 osoby z dostępem do prądu | `—` | `ece1cae9-7658-4056-adfe-15aa21c31ee6` | [`park.paymove.io/ece1cae9`](https://park.paymove.io/ece1cae9-7658-4056-adfe-15aa21c31ee6) |
| **Wrocław** | TARCZYŃSKI ARENA - Camper Park 6 osób bez dostępu do prądu | `—` | `c14db515-f4f5-496d-8ca5-a43d7add395b` | [`park.paymove.io/c14db515`](https://park.paymove.io/c14db515-f4f5-496d-8ca5-a43d7add395b) |
| **Wrocław** | TARCZYŃSKI ARENA - Camper Park 6 osób z dostępem do prądu | `—` | `172e65da-51c7-4781-8f39-ad77133992dc` | [`park.paymove.io/172e65da`](https://park.paymove.io/172e65da-51c7-4781-8f39-ad77133992dc) |
| **Wrocław** | TARCZYŃSKI ARENA - Camper Park bez dostępu do prądu na 30 dni | `—` | `c0f4673b-2387-4a88-ad47-9b37f1dabbcc` | [`park.paymove.io/c0f4673b`](https://park.paymove.io/c0f4673b-2387-4a88-ad47-9b37f1dabbcc) |
| **Wrocław** | TARCZYŃSKI ARENA - Camper Park z dostępem do prądu na 30 dni | `—` | `6208aa0c-7824-414c-a1f2-044b9021fcbf` | [`park.paymove.io/6208aa0c`](https://park.paymove.io/6208aa0c-7824-414c-a1f2-044b9021fcbf) |
| **Wrocław** | TARCZYŃSKI ARENA - Le Mans | `—` | `3aa788da-3b7d-4cd3-90d1-c7ddc294b5a4` | [`park.paymove.io/3aa788da`](https://park.paymove.io/3aa788da-3b7d-4cd3-90d1-c7ddc294b5a4) |
| **Wrocław** | TARCZYŃSKI ARENA - ogólna | `—` | `af87c361-e792-41a8-bdb9-987e4e1156d3` | [`park.paymove.io/af87c361`](https://park.paymove.io/af87c361-e792-41a8-bdb9-987e4e1156d3) |
| **Wrocław** | Wrocław - Awicenny 45 - ALDI - WEIP - abonament 30 dni | `—` | `af15a635-542c-4334-a608-5db4fc8cbe1a` | [`park.paymove.io/af15a635`](https://park.paymove.io/af15a635-542c-4334-a608-5db4fc8cbe1a) |
| **Władysławowo** | Bohaterów Kaszubskich - F548 | `85c8` | `f97a6ac0-7c12-494a-863a-ccf1d13785c8` | [`park.paymove.io/85c8`](https://park.paymove.io/85c8) |
| **Władysławowo** | SPP WŁADYSŁAWOWO - od 15 VI do 31 VIII | `1870` | `3f9c2d11-7a6e-4b8c-9d52-6e4a91ab1870` | [`park.paymove.io/1870`](https://park.paymove.io/1870) |
| **Władysławowo** | SPP WŁADYSŁAWOWO - od 15 VI do 31 VIII - 2 | `4a84` | `f2ee1dbc-e9db-4ee4-98ce-bdd56e534a84` | [`park.paymove.io/4a84`](https://park.paymove.io/4a84) |
| **Władysławowo** | Starowiejska - samochody osobowe - F549 | `94b1` | `f13b4f54-bb02-4dd0-850c-80a30b1c94b1` | [`park.paymove.io/94b1`](https://park.paymove.io/94b1) |
| **Zabrze** | ul. Banachiewicza 15a | `—` | `235df86c-5ebe-414f-88c2-a8020b6d73ce` | [`park.paymove.io/235df86c`](https://park.paymove.io/235df86c-5ebe-414f-88c2-a8020b6d73ce) |
| **Zabrze** | ul. Skłodowskiej - Curie 24 | `—` | `770275e1-9337-4812-b7cc-5c36fd9dd995` | [`park.paymove.io/770275e1`](https://park.paymove.io/770275e1-9337-4812-b7cc-5c36fd9dd995) |
| **Zabrze** | ul. Tatarkiewicza 12 | `—` | `c9093a12-d44a-42a8-80b7-3e87be70d5e2` | [`park.paymove.io/c9093a12`](https://park.paymove.io/c9093a12-d44a-42a8-80b7-3e87be70d5e2) |
| **Zabrze** | Zabrze, 3 Maja 93 - samochody osobowe i motocykle | `80ef` | `363de747-9b6d-49e5-96cd-f5b3f21d80ef` | [`park.paymove.io/80ef`](https://park.paymove.io/80ef) |
| **Zabrze** | Zabrze, De Gaulle’a 75 – F235 | `—` | `6bb4e596-c3a4-4a9d-b2ee-6b2f0db6901f` | [`park.paymove.io/6bb4e596`](https://park.paymove.io/6bb4e596-c3a4-4a9d-b2ee-6b2f0db6901f) |
| **Łomża** | al. Legionów 52 | `—` | `88734ab8-f2ac-4259-8b5a-723a92af5b01` | [`park.paymove.io/88734ab8`](https://park.paymove.io/88734ab8-f2ac-4259-8b5a-723a92af5b01) |
| **Łódź** | Bandurskiego 49 | `—` | `2ade47e5-2d61-4e35-8753-da3f4310391a` | [`park.paymove.io/2ade47e5`](https://park.paymove.io/2ade47e5-2d61-4e35-8753-da3f4310391a) |
| **Łódź** | Dworzec PKP Łódź Kaliska ul. Karolewska | `d5c4` | `193fe5a5-b831-4a9e-8f2d-98b2612bd5c4` | [`park.paymove.io/d5c4`](https://park.paymove.io/d5c4) |
| **Łódź** | Dworzec PKP Łódź Kaliska ul. Unii Lubelskiej | `805c` | `ef66a5d3-0f41-4072-b320-4d354568805c` | [`park.paymove.io/805c`](https://park.paymove.io/805c) |
| **Łódź** | Rydla 31 | `—` | `ae293c0a-bcb4-4f53-82cc-856983cd8fa4` | [`park.paymove.io/ae293c0a`](https://park.paymove.io/ae293c0a-bcb4-4f53-82cc-856983cd8fa4) |
| **Łódź** | ul. Łagiewnicka 54/56 | `—` | `2888e2ee-e397-47eb-b076-19f6ae3ea322` | [`park.paymove.io/2888e2ee`](https://park.paymove.io/2888e2ee-e397-47eb-b076-19f6ae3ea322) |
| **Świdnik** | Wyszyńskiego 22 | `e2c0` | `7093cc3a-8ccf-4daf-bb71-0734b745e2c0` | [`park.paymove.io/e2c0`](https://park.paymove.io/e2c0) |
| **Świdnik** | Wyszyńskiego 22 - abonament 30 dni | `2149` | `17f9932a-e3ed-4831-a436-d38cdd7d2149` | [`park.paymove.io/2149`](https://park.paymove.io/2149) |
| **Żelazna** | PKP Żelazna | `—` | `21a9145b-6beb-4fa5-ab36-2c3c928bd023` | [`park.paymove.io/21a9145b`](https://park.paymove.io/21a9145b-6beb-4fa5-ab36-2c3c928bd023) |
| **Żory** | Żory - Bankowa 6 | `—` | `542fbe60-6399-4632-b951-64f71ffebfb9` | [`park.paymove.io/542fbe60`](https://park.paymove.io/542fbe60-6399-4632-b951-64f71ffebfb9) |

</details>

<details>
<summary><strong>Kliknij, aby rozwinąć: Pełny indeks ponad 80 miast w Polsce obsługiwanych przez Paymove (SPP, PKP i parkingi komercyjne)</strong></summary>

<br />

- **Pomorze i Wybrzeże:** Gdańsk, Gdynia, Sopot, Puck, Władysławowo, Hel, Kołobrzeg, Koszalin, Słupsk, Kościerzyna, Wejherowo, Kartuzy, Malbork, Chojnice, Starogard Gdański, Sztutowo, Mikoszewo, Rotmanka, Łubiana, Ustronie Morskie
- **Zachodniopomorskie i Lubuskie:** Szczecin (396 stref — pełna lista ulic w [`docs/catalog.md`](./docs/catalog.md)), Police, Gorzów Wielkopolski, Międzyrzecz, Lubrza, Żagań
- **Dolny Śląsk i Opolskie:** Wrocław, Bolesławiec, Oleśnica, Lubin, Zgorzelec, Kamienna Góra, Stronie Śląskie, Opole, Namysłów, Prudnik, Kluczbork
- **Śląsk i Zagłębie:** Katowice, Zabrze, Ruda Śląska, Bytom, Rybnik, Wodzisław Śląski, Żory, Pszczyna, Mikołów, Czechowice-Dziedzice, Goczałkowice-Zdrój, Żywiec, Ustroń, Rudy
- **Małopolska i Podhale:** Kraków, Wieliczka, Trzebinia, Niepołomice, Skawina, Krzeszowice, Tarnów, Białka Tatrzańska, Krościenko nad Dunajcem, Dąbrowa Tarnowska
- **Mazowsze i Łódzkie:** Warszawa, Grodzisk Mazowiecki, Wiązowna, Legionowo, Sulejówek, Grójec, Radom, Przasnysz, Łódź, Kutno, Wieluń, Konstantynów
- **Wielkopolska i Kujawy:** Poznań, Gniezno, Kalisz, Ostrów Wielkopolski, Bydgoszcz, Toruń, Grudziądz, Inowrocław, Nakło nad Notecią
- **Wschodnia i Południowo-Wschodnia Polska:** Lublin, Świdnik, Radzyń Podlaski, Kielce, Sandomierz, Stalowa Wola, Rzeszów, Dębica, Jasło, Krosno, Ustrzyki Dolne, Olsztyn, Szczytno, Pisz, Działdowo, Łomża

</details>

<br />

---

<br />

### 4. `PAY` / `FASTPAY` / `DOCPAY` — Szybkie Linki Płatnicze, Inkaso Miejskie i E-Commerce

| Kategoria | Produkt / Partner | Lokalizacja | Kod / UUID | Link / Zakres wdrożenia |
| :--- | :--- | :--- | :--- | :--- |
| **`FASTPAY`** | **Przystań Wędkarska „U ANTKA”** *(Wodowanie / Opłata portowa)* | Polska | `3e0f` | [`https://pay.paymove.io/3e0f`](https://pay.paymove.io/3e0f) (`30.00 PLN`) |
| **`FASTPAY`** | **Parafia Św. Maksymiliana Marii Kolbego** | Łubiana | `b68f` | [`https://pay.paymove.io/b68f`](https://pay.paymove.io/b68f) |
| **`FASTPAY`** | **Paymove PAY Demo** | Polska | `d9ef` | [`https://pay.paymove.io/d9ef`](https://pay.paymove.io/d9ef) |
| **`PAY`** | **Trampki na Giełdzie** | Konferencja | `a1a2` | [`https://pay.paymove.io/a1a2`](https://pay.paymove.io/a1a2) |
| **`DOCPAY`** | **NiOL Szczecin · Miasto Rybnik · RENOMA · Park In Zgorzelec** | Polska | Inkaso miejskie | Natychmiastowe płatności QR na wezwaniach do zapłaty za brak biletu SPP |
| **`CHECKOUT`** | **PilotGo (`pilotgo.ai`) · Urlop.ai · Sportigo · LegalGeek · Slowtico · ZOOL Group · PewnyLokal** | Online | API & MCP | Bramka płatnicza e-commerce (`create-subproduct`) i płatności Scan & Pay |

<br />

---

<br />

## Kompletna Referencja 20 Narzędzi MCP

Serwer Paymove MCP udostępnia **20 metod `@Tool`** podzielonych na **4 domeny funkcjonalne**. Pełna specyfikacja schematów wejściowych i wyjściowych znajduje się w pliku [**`docs/tools.md`**](./docs/tools.md).

### Domena 1 — Pay, Linki Płatnicze i Checkouty E-Commerce (`7 narzędzi`)

| Narzędzie | Autoryzacja | Opis działania |
| :--- | :---: | :--- |
| [`create-pay-product`](./docs/tools.md#2-create-pay-product) | `X-API-KEY` | Tworzy nowy produkt płatniczy `PAY` z cennikiem i zwraca gotowy link (`https://pay.paymove.io/{productId}`). |
| [`create-subproduct`](./docs/tools.md#3-create-subproduct) | `X-API-KEY` | Tworzy checkout e-commerce powiązany z zamówieniem (`externalId`, `amount` w groszach, `returnUrl`) i zwraca `redirectUrl`. |
| [`update-subproduct`](./docs/tools.md#4-update-subproduct) | `X-API-KEY` | Aktualizuje kwotę (`price` w groszach) istniejącego subproduktu zamówienia po `externalId`. |
| [`list-pay-pricing-entries`](./docs/tools.md#5-list-pay-pricing-entries) | **Zero-Auth** / Klucz | Zwraca listę wszystkich pozycji cennikowych (`entryId`, `name`, `price`) skonfigurowanych na produkcie `PAY`. |
| [`add-pay-pricing-entry`](./docs/tools.md#6-add-pay-pricing-entry) | `X-API-KEY` | Dodaje nowy wariant cenowy (`name`, `price` w groszach) do istniejącego produktu `PAY`. |
| [`update-pay-pricing-entry`](./docs/tools.md#7-update-pay-pricing-entry) | `X-API-KEY` | Aktualizuje nazwę, cenę lub szczegóły wybranej pozycji cennikowej (`entryId`). |
| [`delete-pay-pricing-entry`](./docs/tools.md#8-delete-pay-pricing-entry) | `X-API-KEY` | Usuwa wybraną pozycję cennikową (`entryId`) z produktu `PAY`. |

<br />

### Domena 2 — Pay&Go: Bilety, Atrakcje i Sklepy Samoobsługowe (`8 narzędzi`)

| Narzędzie | Autoryzacja | Opis działania |
| :--- | :---: | :--- |
| [`go-create-product`](./docs/tools.md#9-go-create-product) | `X-API-KEY` | Tworzy samoobsługowy sklep biletowy `GO` z wieloma wariantami biletów i zwraca link `https://go.paymove.io/{productId}`. |
| [`go-get-product`](./docs/tools.md#14-go-get-product) | **Zero-Auth** / Klucz | Pobiera pełne szczegóły produktu `GO`, listę biletów (`optionId`), ceny w groszach oraz opisy językowe. |
| [`go-add-ticket-option`](./docs/tools.md#10-go-add-ticket-option) | `X-API-KEY` | Dopisuje nowy wariant biletu (`name`, `price`, `description`) do istniejącego produktu `GO`. |
| [`go-update-ticket-option`](./docs/tools.md#11-go-update-ticket-option) | `X-API-KEY` | Aktualizuje pojedynczy wariant biletu (`optionId`) bez nadpisywania pozostałych opcji. |
| [`go-delete-ticket-option`](./docs/tools.md#12-go-delete-ticket-option) | `X-API-KEY` | Usuwa wskazany wariant biletu (`optionId`) z produktu `GO`. |
| [`go-update-product`](./docs/tools.md#13-go-update-product) | `X-API-KEY` | Zastępuje pełną listę biletów lub metadane (`imageDisplayType`) na produkcie `GO`. |
| [`go-set-translations`](./docs/tools.md#15-go-set-translations) | `X-API-KEY` | Ustawia tłumaczenia opisów produktu i biletów (`pl-PL`, `en-US`, `de-DE`, `uk-UA`, `fr-FR`, `es-ES`, `it-IT`, `cs-CZ`). |
| [`go-generate-image`](./docs/tools.md#16-go-generate-image) | `X-API-KEY` | Generuje ilustrację okładkową AI (`HEADER` lub `BACKGROUND`) i automatycznie podpina ją do produktu `GO`. |

<br />

### Domena 3 — Parking i Mobilność Miejska (`3 narzędzia`)

| Narzędzie | Autoryzacja | Opis działania |
| :--- | :---: | :--- |
| [`parking-create-product`](./docs/tools.md#17-parking-create-product) | `X-API-KEY` | Tworzy strefę parkingową `PARKING` z krokami czasowymi, darmowymi minutami, limitami dobowymi i harmonogramem (`https://park.paymove.io/{id}`). |
| [`parking-create-event`](./docs/tools.md#18-parking-create-event) | `X-API-KEY` | Planuje specjalną taryfę eventową (`PRICING_CHANGE`) lub wyłączenie parkingu (`PAUSE_PARKING`) w zadanym przedziale czasu. |
| [`parking-get-pricing`](./docs/tools.md#19-parking-get-pricing) | **Zero-Auth** / Klucz | Pobiera pełną konfigurację cennika, kroków czasowych, harmonogramów i aktywnych eventów dla dowolnej strefy parkingowej. |

<br />

### Domena 4 — Public Discovery i Katalog Partnera (`2 narzędzia`)

| Narzędzie | Autoryzacja | Opis działania |
| :--- | :---: | :--- |
| [`search-public-products`](./docs/tools.md#20-search-public-products) | **Zero-Auth** | Przeszukuje publiczny katalog Paymove po frazie (`query`), mieście (`location`) i typie (`GO`, `PARKING`, `PAY`), zwracając bezpośrednie linki zakupowe. |
| [`list-partner-products`](./docs/tools.md#1-list-partner-products) | `X-API-KEY` | Zwraca listę wszystkich produktów (`PAY`, `GO`, `PARKING`) należących do uwierzytelnionego konta partnera. |

<br />

---

<br />

## Kluczowe Reguły dla Agentów AI

Podczas implementacji integracji lub wywoływania narzędzi Paymove przestrzegaj poniższych reguł (pełna instrukcja w [`AGENTS.md`](./AGENTS.md) oraz [`SKILL.md`](./SKILL.md)):

> [!IMPORTANT]
> 1. **Wszystkie kwoty są liczbami całkowitymi w groszach (`1/100 PLN`).** `1000` oznacza **10.00 PLN**, a `4500` oznacza **45.00 PLN**. Przekazanie liczby zmiennoprzecinkowej (np. `12.99`) do REST API spowoduje ciche obcięcie do `12` groszy. Zawsze stosuj `Math.round(kwotaPln * 100)`.
> 2. **Autoryzacja wyłącznie nagłówkiem `X-API-KEY`**, nigdy `Authorization: Bearer`. Klucze testowe zaczynają się od `sk_test_`, a produkcyjne od `sk_live_`. Publiczne wyszukiwanie katalogu nie wymaga żadnego nagłówka.
> 3. **Zawsze weryfikuj podpis `X-Paymove-Signature` na webhookach** za pomocą HMAC-SHA256 ze stringa `"{timestamp}.{raw_body}"` przy użyciu pełnego sekretu `whsec_...` przed realizacją zamówienia. Nigdy nie oznaczaj zamówienia jako opłaconego wyłącznie na podstawie powrotu klienta na `returnUrl`.
> 4. **Testowy kod BLIK na Sandboxie:** dowolny 6-cyfrowy kod zaczynający się od **`777`** (np. `777123`).
> 5. **Minimalna kwota dla PayPo:** metoda PayPo pojawia się na checkoucie od kwoty **`1000` groszy (`10.00 PLN`)**.

<br />

---

<br />

## Dlaczego Paymove

| Parametr | Standard Paymove |
| :--- | :--- |
| **Nadzór regulacyjny** | Licencjonowana Mała Instytucja Płatnicza nadzorowana przez **KNF (`MIP245/2024`)** |
| **Prowizja transakcyjna** | Jednolita stawka **0,99%** dla wszystkich metod płatności |
| **Opłaty stałe i ukryte** | **0 PLN** za aktywację · **0 PLN** abonamentu · **0 PLN** za zwroty · **0 PLN** za wypłaty |
| **Czas rozliczenia (Settlement)** | **T+1** (środki na koncie bankowym w następnym dniu roboczym) |
| **Metody płatności** | **BLIK**, **Apple Pay**, **Google Pay**, **Karty płatnicze (Visa / Mastercard)**, **PayPo (BNPL)** |
| **Doświadczenie użytkownika** | Natychmiastowy mobilny checkout w przeglądarce (`go.paymove.io` / `park.paymove.io` / `pay.paymove.io`) — **zero pobierania aplikacji, zero rejestracji konta** |
| **Oficjalne SDK Node.js** | [`npm install @paymove-io/sdk`](https://www.npmjs.com/package/@paymove-io/sdk) (zero zależności runtime, wsparcie ESM + CJS, pełne typowanie TypeScript) |

<br />

---

<br />

## Struktura Repozytorium

```text
paymove-mcp/
├── assets/
│   ├── logo-dark.svg                  # Oficjalne wektorowe logo Paymove dla motywu ciemnego (#FAFAFA)
│   ├── logo-light.svg                 # Oficjalne wektorowe logo Paymove dla motywu jasnego (#0A0D14)
│   └── paymove-logo.png               # Logo Paymove w wysokiej rozdzielczości (PNG)
├── docs/
│   ├── catalog.md                     # Pełny katalog ponad 70 miast i 630+ publicznych produktów
│   └── tools.md                       # Dokumentacja techniczna wszystkich 20 narzędzi MCP w 4 domenach
├── examples/
│   ├── claude_desktop_config.json     # Gotowa konfiguracja dla aplikacji Claude Desktop
│   └── cursor-mcp.json                # Gotowa konfiguracja dla edytora Cursor
├── AGENTS.md                          # Zwięzłe reguły integracji Paymove dla agentów kodujących
├── SKILL.md                           # Kompletna procedura wdrożenia krok po kroku dla agentów AI
├── server.json                        # Oficjalny manifest serwera MCP (schemat 2025-10-17)
├── README.md                          # Dokumentacja w języku angielskim
├── README.pl.md                       # Dokumentacja w języku polskim (ten plik)
└── LICENSE                            # Licencja MIT
```

<br />

---

<div align="center">

**Paymove Sp. z o.o.** &nbsp;·&nbsp; KNF `MIP245/2024` &nbsp;·&nbsp; [paymove.io](https://paymove.io) &nbsp;·&nbsp; [docs.paymove.io](https://docs.paymove.io) &nbsp;·&nbsp; [panel.paymove.io](https://panel.paymove.io) &nbsp;·&nbsp; [integration@paymove.io](mailto:integration@paymove.io)

</div>
