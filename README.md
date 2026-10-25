<div align="center">

<br />

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/logo-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="./assets/logo-light.svg" />
  <img alt="Paymove" src="./assets/paymove-logo.png" width="320" />
</picture>

<br />
<br />

**Official Model Context Protocol (MCP) Server for [Paymove](https://paymove.io)**

Buy city tickets and pay for parking across Poland without an API key, or launch checkouts and payment links in one sentence.

<br />

[**English**](./README.md) &nbsp;·&nbsp; [**Polski**](./README.pl.md)

</div>

<br />

---

<br />

## Quick Start

**MCP Endpoint:** `https://api.paymove.io/api/mcp` *(Streamable HTTP)*

### 1. Public Mode (No API Key Required)

Any AI agent can search available city services, check ticket and parking prices, and return a direct checkout link (BLIK, Apple Pay, Google Pay, Cards, PayPo).

**Claude Code:**

```bash
claude mcp add --transport http paymove https://api.paymove.io/api/mcp
```

**Cursor (`.cursor/mcp.json`):**

```json
{
  "mcpServers": {
    "paymove": {
      "url": "https://api.paymove.io/api/mcp"
    }
  }
}
```

<br />

### 2. Merchant Mode (With `X-API-KEY`)

To create and manage your own products, payment links, tickets, or parking zones, generate an API key in [panel.paymove.io](https://panel.paymove.io) and pass it in the `X-API-KEY` header.

**Claude Code:**

```bash
claude mcp add --transport http paymove https://api.paymove.io/api/mcp \
  --header "X-API-KEY: YOUR_PAYMOVE_API_KEY"
```

**Cursor (`.cursor/mcp.json`):**

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

<br />

---

<br />

## Available Services & Locations

Paymove currently provides **615 active public services across 69 cities in Poland**:
- **32** ticket, attraction, museum, zoo, transit, and payment services (`GO` & `PAY`)
- **583** municipal paid parking zones (SPP) and city car parks (`PARKING`)

| Location | Service / Product Name | URL |
| :--- | :--- | :--- |
| Gdańsk | Gdański Ogród Zoologiczny (ZOO Gdańsk) | [https://go.paymove.io/cb60](https://go.paymove.io/cb60) |
| Gdańsk | ZOO Gdańsk — Sun & Snow | [https://go.paymove.io/cb62](https://go.paymove.io/cb62) |
| Gdańsk | Fundacja Gdańskiego Ogrodu Zoologicznego Lynx | [https://go.paymove.io/81ef](https://go.paymove.io/81ef) |
| Gdańsk | Jungle Jump — Park Rozrywki (CH Osowa) | [https://go.paymove.io/d9e6](https://go.paymove.io/d9e6) |
| Gdańsk | Park Dmuchańców Słonik Balonik (Brzeźno) | [https://go.paymove.io/899](https://go.paymove.io/899) |
| Gdańsk | Wielka Fabryka Elfów — Warsztaty | [https://go.paymove.io/7def](https://go.paymove.io/7def) |
| Gdańsk / Sopot | Katalog Atrakcji Trójmiasto i Pomorze | [https://catalog.paymove.io/gogda](https://catalog.paymove.io/gogda) |
| Gdańsk | Ergo Arena — Parking (samochody osobowe) | [https://park.paymove.io/8898](https://park.paymove.io/8898) |
| Gdańsk | Dworzec PKP Gdańsk Główny — Parking | [https://park.paymove.io/44f942bb-9d87-4d2b-a568-25884b386ec5](https://park.paymove.io/44f942bb-9d87-4d2b-a568-25884b386ec5) |
| Gdynia | Garden of Lights — Gdynia | [https://go.paymove.io/7a38](https://go.paymove.io/7a38) |
| Sopot | Park Dmuchańców Happy Kangur | [https://go.paymove.io/0dd2](https://go.paymove.io/0dd2) |
| Sopot | Sofitel Grand Sopot — Parking | [https://park.paymove.io/09d6ce12-5331-4fcf-9edb-103d89845683](https://park.paymove.io/09d6ce12-5331-4fcf-9edb-103d89845683) |
| Rotmanka | Dyniowe Love — Farma Dyniowa | [https://go.paymove.io/738](https://go.paymove.io/738) |
| Warszawa | Muzeum Historii Żydów Polskich POLIN | [https://go.paymove.io/91a4](https://go.paymove.io/91a4) |
| Warszawa | Muzeum POLIN — Darowizny | [https://go.paymove.io/b780](https://go.paymove.io/b780) |
| Warszawa | Garden of Lights — Warszawa | [https://go.paymove.io/5f3d](https://go.paymove.io/5f3d) |
| Warszawa | Dworzec PKP Warszawa Centralna — Parking | [https://park.paymove.io/50d4cd96-bf7d-47b9-a8b6-df636de75357](https://park.paymove.io/50d4cd96-bf7d-47b9-a8b6-df636de75357) |
| Warszawa | Dworzec PKP Warszawa Wschodnia — Parking | [https://park.paymove.io/091a](https://park.paymove.io/091a) |
| Legionowo | World Cat Show — Arena Legionowo (Sobota) | [https://go.paymove.io/dw57](https://go.paymove.io/dw57) |
| Legionowo | World Cat Show — Arena Legionowo (Niedziela) | [https://go.paymove.io/dw66](https://go.paymove.io/dw66) |
| Kraków | Garden of Lights — Kraków | [https://go.paymove.io/62be](https://go.paymove.io/62be) |
| Kraków | Al. Pokoju 46 (Tauron Arena) — Parking | [https://park.paymove.io/7ddd](https://park.paymove.io/7ddd) |
| Wrocław | Garden of Lights — Wrocław | [https://go.paymove.io/0797](https://go.paymove.io/0797) |
| Wrocław | Dworzec PKP Wrocław Główny — Parking | [https://park.paymove.io/6bf749b6-776d-402b-a6a8-dfbfe0d519cc](https://park.paymove.io/6bf749b6-776d-402b-a6a8-dfbfe0d519cc) |
| Wrocław | Tarczyński Arena — Parking | [https://park.paymove.io/af87c361-e792-41a8-bdb9-987e4e1156d3](https://park.paymove.io/af87c361-e792-41a8-bdb9-987e4e1156d3) |
| Szczecin | Garden of Lights — Szczecin | [https://go.paymove.io/71fe](https://go.paymove.io/71fe) |
| Szczecin | Strefa Płatnego Parkowania (396 lokalizacji SPP) | [https://park.paymove.io/lx4h](https://park.paymove.io/lx4h) |
| Lublin | Muzeum Narodowe w Lublinie — Kaplica Trójcy Świętej | [https://go.paymove.io/6b58](https://go.paymove.io/6b58) |
| Lublin | Muzeum Narodowe w Lublinie — Tamara Łempicka | [https://go.paymove.io/1ef4](https://go.paymove.io/1ef4) |
| Lublin | MOSiR Bystrzyca (ul. Stadionowa 1) — Parking | [https://park.paymove.io/39f3](https://park.paymove.io/39f3) |
| Krosno | Centrum Dziedzictwa Szkła — Miasto Szkła Krosno | [https://go.paymove.io/aoff](https://go.paymove.io/aoff) |
| Poznań | Poznań ZOO — Parking | [https://park.paymove.io/2a3e32e1-33a8-46cb-8a5c-358979267b43](https://park.paymove.io/2a3e32e1-33a8-46cb-8a5c-358979267b43) |
| Toruń | Arena Toruń — Parking | [https://park.paymove.io/0804132b-0d27-4fb5-b1a8-e51be65b0f09](https://park.paymove.io/0804132b-0d27-4fb5-b1a8-e51be65b0f09) |
| Katowice | Dworzec PKP Katowice — Parking | [https://park.paymove.io/c967](https://park.paymove.io/c967) |
| Kołobrzeg | Parkingi Miejskie i Dworzec PKP (17 stref) | [https://park.paymove.io/e60cbb6f-cb19-4392-90dd-8d74c50ac764](https://park.paymove.io/e60cbb6f-cb19-4392-90dd-8d74c50ac764) |
| Puck | Strefa Płatnego Parkowania w Pucku (16 stref) | [https://park.paymove.io/f0b1c89a-cf1e-4f89-a8b0-e00d84bbe9f3](https://park.paymove.io/f0b1c89a-cf1e-4f89-a8b0-e00d84bbe9f3) |
| Władysławowo | Strefa Płatnego Parkowania — Władysławowo | [https://park.paymove.io/85c8](https://park.paymove.io/85c8) |
| Hel | ul. Admirała Steyera — Parking | [https://park.paymove.io/9d8a](https://park.paymove.io/9d8a) |
| Kościerzyna | Strefa Płatnego Parkowania w Kościerzynie | [https://park.paymove.io/1389](https://park.paymove.io/1389) |
| Chojnice | I Strefa Płatnego Parkowania w Chojnicach | [https://park.paymove.io/8800](https://park.paymove.io/8800) |
| Gniezno | Strefa Płatnego Parkowania w Gnieźnie | [https://park.paymove.io/12cc](https://park.paymove.io/12cc) |
| Rybnik | Strefa Płatnego Parkowania w Rybniku | [https://park.paymove.io/fe6e](https://park.paymove.io/fe6e) |
| Wodzisław Śląski | Strefa Płatnego Parkowania w Wodzisławiu Śląskim | [https://park.paymove.io/2f3f](https://park.paymove.io/2f3f) |
| Radzyń Podlaski | Strefa Płatnego Parkowania w Radzyniu Podlaskim | [https://park.paymove.io/f5f6](https://park.paymove.io/f5f6) |
| Namysłów | Strefa Płatnego Parkowania w Namysłowie | [https://park.paymove.io/5343](https://park.paymove.io/5343) |
| Kutno | Parking Miejski Kutno — Pl. Wolności | [https://park.paymove.io/6253](https://park.paymove.io/6253) |
| Wieliczka | Parking ul. Goliana 10 / FitParking Wieliczka | [https://park.paymove.io/0fbc](https://park.paymove.io/0fbc) |
| Białka Tatrzańska | Parking Stajanie | [https://park.paymove.io/6c47](https://park.paymove.io/6c47) |
| Krościenko nad Dunajcem | Parking Trzy Korony | [https://park.paymove.io/15e0](https://park.paymove.io/15e0) |
| Stronie Śląskie | Stroński Park Aktywności — Łowisko | [https://go.paymove.io/d872](https://go.paymove.io/d872) |
| Stronie Śląskie | Stroński Park Aktywności — Kąpielisko | [https://go.paymove.io/5823](https://go.paymove.io/5823) |
| Ustronie Morskie | AMARI Holistic SPA (The One by Sun & Snow) | [https://go.paymove.io/8c4b](https://go.paymove.io/8c4b) |
| Rudy | Rudy Las — Kolejka Wąskotorowa | [https://go.paymove.io/km75](https://go.paymove.io/km75) |
| Rudy | Rudy Las — Bal Andrzejkowy | [https://go.paymove.io/ad55](https://go.paymove.io/ad55) |
| Polska | Komunikacja Miejska — Bilety Czasowe | [https://go.paymove.io/ab12](https://go.paymove.io/ab12) |
| Polska | Przystań Wędkarska „U Antka” | [https://pay.paymove.io/3e0f](https://pay.paymove.io/3e0f) |

<br />

<details>
<summary><strong>Show all 187 city parking zones across Poland (Location / Name / URL)</strong></summary>

<br />

| Location | Parking Zone / Car Park | URL |
| :--- | :--- | :--- |
| Białka Tatrzańska | Parking Stajanie | [https://park.paymove.io/6c47](https://park.paymove.io/6c47) |
| Bolesławiec | Bolesławiec, Chrobrego 35 | [https://park.paymove.io/9c7a2839-6a6f-4ac7-ba34-6303239b4f36](https://park.paymove.io/9c7a2839-6a6f-4ac7-ba34-6303239b4f36) |
| Bolesławiec | Dworzec PKP Bolesławiec | [https://park.paymove.io/3a5efb46-afee-4654-8a6d-7ae247bd0814](https://park.paymove.io/3a5efb46-afee-4654-8a6d-7ae247bd0814) |
| Bydgoszcz | Bydgoszcz, Gdańska 47 | [https://park.paymove.io/44614a4e-c4b7-4238-af99-8be4ce8f88c1](https://park.paymove.io/44614a4e-c4b7-4238-af99-8be4ce8f88c1) |
| Bydgoszcz | Dworzec PKP Bydgoszcz Główna | [https://park.paymove.io/67fa0d96-a482-4567-b71c-d24e164b6def](https://park.paymove.io/67fa0d96-a482-4567-b71c-d24e164b6def) |
| Bydgoszcz | Parking przy halach sportowych i lodowisku ul. Toruńska 59 | [https://park.paymove.io/6a689c59-1744-49df-a067-e49541e1bb37](https://park.paymove.io/6a689c59-1744-49df-a067-e49541e1bb37) |
| Chojnice | I Strefa Płatnego Parkowania w Chojnicach | [https://park.paymove.io/8800](https://park.paymove.io/8800) |
| Czechowice-Dziedzice | ul. Barlickiego 34 | [https://park.paymove.io/dee84323-13f8-4e69-8b59-bcf68ebf8a06](https://park.paymove.io/dee84323-13f8-4e69-8b59-bcf68ebf8a06) |
| Gdańsk | Dworzec PKP Gdańsk Główny | [https://park.paymove.io/44f942bb-9d87-4d2b-a568-25884b386ec5](https://park.paymove.io/44f942bb-9d87-4d2b-a568-25884b386ec5) |
| Gdańsk | Ergo Arena - autokar, bus, kamper | [https://park.paymove.io/22a2](https://park.paymove.io/22a2) |
| Gdańsk | Ergo Arena - pojazd osobowy, jednoślad | [https://park.paymove.io/8898](https://park.paymove.io/8898) |
| Gdańsk | Gdańsk, Polanki 117 - Parking zewnętrzny | [https://park.paymove.io/ecf6](https://park.paymove.io/ecf6) |
| Gdańsk | Mieszczańska | [https://park.paymove.io/0bb0](https://park.paymove.io/0bb0) |
| Gdańsk | Smoluchowskiego | [https://park.paymove.io/c57f](https://park.paymove.io/c57f) |
| Gdańsk | ul. Platynowa 2 | [https://park.paymove.io/9a39a5de-9476-4ae6-848d-8e099c2254da](https://park.paymove.io/9a39a5de-9476-4ae6-848d-8e099c2254da) |
| Gdynia | Centrum Rodzinne Witawa - ul. Wielkokacka 2-4 | [https://park.paymove.io/3181a076-7089-4cd8-841a-52019fc8bcd9](https://park.paymove.io/3181a076-7089-4cd8-841a-52019fc8bcd9) |
| Gdynia | Gdynia – Gniewska | [https://park.paymove.io/2384af30-62b7-466a-9d87-ea470df00256](https://park.paymove.io/2384af30-62b7-466a-9d87-ea470df00256) |
| Gniezno | Dworzec PKP Gniezno | [https://park.paymove.io/4871a9f1-7250-4759-9192-4fd40acae5ac](https://park.paymove.io/4871a9f1-7250-4759-9192-4fd40acae5ac) |
| Gniezno | SPP - PODSTREFA C (zielona) | [https://park.paymove.io/12cc](https://park.paymove.io/12cc) |
| Goczałkowice-Zdrój | ul. Uzdrowiskowa 41 | [https://park.paymove.io/c32a13b8-b0e2-44f4-b9fe-14d88c2b0feb](https://park.paymove.io/c32a13b8-b0e2-44f4-b9fe-14d88c2b0feb) |
| Gorzów Wielkopolski | Gorzów Wielkopolski - Walczaka 23h | [https://park.paymove.io/11df](https://park.paymove.io/11df) |
| Gorzów Wielkopolski | Gorzów Wielkopolski, Witosa 50 | [https://park.paymove.io/ccfb34ea-cc84-4e32-98da-34c97844bda9](https://park.paymove.io/ccfb34ea-cc84-4e32-98da-34c97844bda9) |
| Grodzisk Mazowiecki | ul. 11 Listopada 33 | [https://park.paymove.io/db54](https://park.paymove.io/db54) |
| Hel | Admirała Steyera - WEIP | [https://park.paymove.io/9d8a](https://park.paymove.io/9d8a) |
| Joannitów | PKP Joannitów | [https://park.paymove.io/13f9bd2d-16cf-4629-a83f-a65245acb158](https://park.paymove.io/13f9bd2d-16cf-4629-a83f-a65245acb158) |
| Joannitów | PKP Joannitów - autokary | [https://park.paymove.io/2d1fe14c-58cc-44d9-978f-97fac81eaf64](https://park.paymove.io/2d1fe14c-58cc-44d9-978f-97fac81eaf64) |
| Kalisz | Wyszyńskiego 42A | [https://park.paymove.io/ad4122e1-8d8e-49f9-9191-aa0878db2fc6](https://park.paymove.io/ad4122e1-8d8e-49f9-9191-aa0878db2fc6) |
| Kartuzy | Kolejowa 7a | [https://park.paymove.io/b042](https://park.paymove.io/b042) |
| Katowice | Dworzec PKP Katowice | [https://park.paymove.io/c967](https://park.paymove.io/c967) |
| Katowice | Katowice Goeppert-Mayer PKP | [https://park.paymove.io/4964](https://park.paymove.io/4964) |
| Kielce | Kielce - Marii Konopnickiej | [https://park.paymove.io/cf16d5e4-26d8-43bf-a941-2b5dbeba7f52](https://park.paymove.io/cf16d5e4-26d8-43bf-a941-2b5dbeba7f52) |
| Kielce | Kielce - ul. Barwinek 29 | [https://park.paymove.io/f143e7c4-4fd5-4760-9f27-6365fb665da3](https://park.paymove.io/f143e7c4-4fd5-4760-9f27-6365fb665da3) |
| Kielce | Spółdzielnia Mieszkaniowa Bocianek w Kielcach | [https://park.paymove.io/eae4af4a-2c57-47cf-90a2-4c7e9fa1dacc](https://park.paymove.io/eae4af4a-2c57-47cf-90a2-4c7e9fa1dacc) |
| Kielce | ul. Bodzentyńska 15 | [https://park.paymove.io/a8c8e27c-369f-4b24-926e-0858262697d3](https://park.paymove.io/a8c8e27c-369f-4b24-926e-0858262697d3) |
| Kielce | ul. Szajnowicza-Iwanowa 17 | [https://park.paymove.io/3eaebeb7-d33d-4d8b-b57e-ab21ef21b4fe](https://park.paymove.io/3eaebeb7-d33d-4d8b-b57e-ab21ef21b4fe) |
| Kielce | ul. Szydłówek Górny 6 i 10 | [https://park.paymove.io/2fd0db3a-e3db-48bf-a72c-936d32ceca1b](https://park.paymove.io/2fd0db3a-e3db-48bf-a72c-936d32ceca1b) |
| Kielce | ul. Wapiennikowa - SAMOCHÓD OSOBOWY | [https://park.paymove.io/cc4f](https://park.paymove.io/cc4f) |
| Kielce | ul. Warszawska 147 | [https://park.paymove.io/12f138a9-44bb-45c7-9e14-3c89e8ac1a0b](https://park.paymove.io/12f138a9-44bb-45c7-9e14-3c89e8ac1a0b) |
| Kielce | ul. Warszawska 218d | [https://park.paymove.io/b48ccbf6-29d5-4107-b329-3bffd12db9f6](https://park.paymove.io/b48ccbf6-29d5-4107-b329-3bffd12db9f6) |
| Kielce | ul. Ćwiklińskiej 2 | [https://park.paymove.io/33bb97d7-3c3f-4da7-97d3-5cc1e1a00775](https://park.paymove.io/33bb97d7-3c3f-4da7-97d3-5cc1e1a00775) |
| Konstantynów | Fryzjer Galeria Konstantynów | [https://park.paymove.io/d186ee98-93f9-46b3-82e4-ff1dc0bbb2c4](https://park.paymove.io/d186ee98-93f9-46b3-82e4-ff1dc0bbb2c4) |
| Koszalin | Koszalin, Karłowicza 28 | [https://park.paymove.io/5cfccfc9-4389-4924-8832-a560b1a07f7d](https://park.paymove.io/5cfccfc9-4389-4924-8832-a560b1a07f7d) |
| Koszalin | Koszalin, Łużycka 34 | [https://park.paymove.io/27bdb73c-b660-40fe-b4bf-d0aba09be495](https://park.paymove.io/27bdb73c-b660-40fe-b4bf-d0aba09be495) |
| Kołobrzeg | Dworzec PKP Kołobrzeg - autokary | [https://park.paymove.io/d53d2499-5f20-4fa3-bca2-0fcb2674dcd7](https://park.paymove.io/d53d2499-5f20-4fa3-bca2-0fcb2674dcd7) |
| Kołobrzeg | Dworzec PKP Kołobrzeg - samochody osobowe | [https://park.paymove.io/e60cbb6f-cb19-4392-90dd-8d74c50ac764](https://park.paymove.io/e60cbb6f-cb19-4392-90dd-8d74c50ac764) |
| Kołobrzeg | Parking Amfiteatr | [https://park.paymove.io/79cd1183-ed5f-4f38-975f-e5efed861b35](https://park.paymove.io/79cd1183-ed5f-4f38-975f-e5efed861b35) |
| Kołobrzeg | Parking Hala Milenium | [https://park.paymove.io/cc63af6c-4ae5-4403-ad83-9cfed7461e8d](https://park.paymove.io/cc63af6c-4ae5-4403-ad83-9cfed7461e8d) |
| Kołobrzeg | Parking Marina Solna | [https://park.paymove.io/53436f1c-c1d9-4454-a716-c833d1a1b367](https://park.paymove.io/53436f1c-c1d9-4454-a716-c833d1a1b367) |
| Kołobrzeg | Parking Mazowiecka Park | [https://park.paymove.io/f15023cc-a42f-4c9a-af96-6a8f0a6d8d3d](https://park.paymove.io/f15023cc-a42f-4c9a-af96-6a8f0a6d8d3d) |
| Kołobrzeg | Parking Nadmorskie Tarasy | [https://park.paymove.io/5f73d6bb-52ce-4950-910c-ee6b5addd657](https://park.paymove.io/5f73d6bb-52ce-4950-910c-ee6b5addd657) |
| Kołobrzeg | Parking Port Rybacki | [https://park.paymove.io/6e4f833e-38db-4b81-9e14-dffd585d7adb](https://park.paymove.io/6e4f833e-38db-4b81-9e14-dffd585d7adb) |
| Kołobrzeg | Parking Restauracja Aqua | [https://park.paymove.io/8b1b2cd6-f32c-4e3b-8480-fb2fa320930a](https://park.paymove.io/8b1b2cd6-f32c-4e3b-8480-fb2fa320930a) |
| Kołobrzeg | Parking Solna | [https://park.paymove.io/ee748825-ce65-4b18-a480-e8baf303796a](https://park.paymove.io/ee748825-ce65-4b18-a480-e8baf303796a) |
| Kołobrzeg | Parking Unii Lubelskiej | [https://park.paymove.io/3b68caab-7cae-4756-b0e5-f7ab4935f2f3](https://park.paymove.io/3b68caab-7cae-4756-b0e5-f7ab4935f2f3) |
| Kościerzyna | Kapliczna | [https://park.paymove.io/c6575f78-63e2-41b1-b31c-414ccf8209a5](https://park.paymove.io/c6575f78-63e2-41b1-b31c-414ccf8209a5) |
| Kościerzyna | Kościerzyna - 3 Maja | [https://park.paymove.io/e2ba5048-6f6a-4ede-b48f-526e389bc3ca](https://park.paymove.io/e2ba5048-6f6a-4ede-b48f-526e389bc3ca) |
| Kościerzyna | Kościerzyna - Lubomira Szopińskiego | [https://park.paymove.io/7858e1dd-e7ec-4bc4-9910-440003a71469](https://park.paymove.io/7858e1dd-e7ec-4bc4-9910-440003a71469) |
| Kościerzyna | Kościerzyna - Strefa Płatnego Parkowania | [https://park.paymove.io/1389](https://park.paymove.io/1389) |
| Kościerzyna | Kościerzyna – AQUA Centrum | [https://park.paymove.io/983789df-0e15-4143-a380-f1b1da42c034](https://park.paymove.io/983789df-0e15-4143-a380-f1b1da42c034) |
| Kościerzyna | Świętojańska | [https://park.paymove.io/0c61d988-33db-4115-9cf0-bb07f7147595](https://park.paymove.io/0c61d988-33db-4115-9cf0-bb07f7147595) |
| Kraków | Al. Pokoju 46 | [https://park.paymove.io/7ddd](https://park.paymove.io/7ddd) |
| Kraków | Garbarska 18b - PARKEMI | [https://park.paymove.io/c231](https://park.paymove.io/c231) |
| Kraków | Kraków - os. Kombatantów - PARKEMI | [https://park.paymove.io/0a97](https://park.paymove.io/0a97) |
| Kraków | SM Podwawelska - DZP | [https://park.paymove.io/cbcc](https://park.paymove.io/cbcc) |
| Kraków | ul. Aktorów 1 i Wizjonerów 7 - bramka | [https://park.paymove.io/d9ed4b59-f9d4-48fb-932a-26fc94e756fc](https://park.paymove.io/d9ed4b59-f9d4-48fb-932a-26fc94e756fc) |
| Krościenko nad Dunajcem | Parking Trzy Korony | [https://park.paymove.io/15e0](https://park.paymove.io/15e0) |
| Kutno | Parking Miejski Kutno - Pl. Wolności | [https://park.paymove.io/6253](https://park.paymove.io/6253) |
| Lubin | ul. Kopernika 17 | [https://park.paymove.io/2df5a19a-e411-4789-aa42-634cdb57e2c6](https://park.paymove.io/2df5a19a-e411-4789-aa42-634cdb57e2c6) |
| Lublin | Lublin Okopowa PKP | [https://park.paymove.io/6024](https://park.paymove.io/6024) |
| Lublin | S.M. Rudnik | [https://park.paymove.io/4d42](https://park.paymove.io/4d42) |
| Lublin | Stadionowa 1 - autokar | [https://park.paymove.io/378a](https://park.paymove.io/378a) |
| Lublin | Stadionowa 1 - samochód osobowy | [https://park.paymove.io/39f3](https://park.paymove.io/39f3) |
| Lubrza | ul. Świebodzińska 52A | [https://park.paymove.io/197937e8-062c-49ad-aa6d-1541f132db48](https://park.paymove.io/197937e8-062c-49ad-aa6d-1541f132db48) |
| Malbork | Malbork · TRIATLON - WEIP | [https://park.paymove.io/d86a2e50-8287-4e38-8196-cdd6a4838843](https://park.paymove.io/d86a2e50-8287-4e38-8196-cdd6a4838843) |
| Mikołów | ul. Miarki 11 | [https://park.paymove.io/2831668a-0b3b-4aaa-9980-7c43adb60ddc](https://park.paymove.io/2831668a-0b3b-4aaa-9980-7c43adb60ddc) |
| Międzyrzecz | Międzyrzecz - Plac Powstańców Wielkopolskich 4 | [https://park.paymove.io/8079977e-a48a-4752-afbb-91db3ffb2d8b](https://park.paymove.io/8079977e-a48a-4752-afbb-91db3ffb2d8b) |
| Międzyrzecz | ul. Chrobrego 2 i 4 | [https://park.paymove.io/5fe33b15-7323-4ccb-ba78-3206c7dee05a](https://park.paymove.io/5fe33b15-7323-4ccb-ba78-3206c7dee05a) |
| Namysłów | SPP w Namysłowie - Strefa B | [https://park.paymove.io/5343](https://park.paymove.io/5343) |
| Niepołomice | ul. Targowa 10 | [https://park.paymove.io/e5c3b5c7-ea03-4d79-8a30-cdf4f1abe11b](https://park.paymove.io/e5c3b5c7-ea03-4d79-8a30-cdf4f1abe11b) |
| Oleśnica | ul. Sikorskiego 6 | [https://park.paymove.io/444cef10-15cb-46b7-aca8-b9520ee0d7cd](https://park.paymove.io/444cef10-15cb-46b7-aca8-b9520ee0d7cd) |
| Olsztyn | Olsztyn - Warmińsko-Mazurskie Centrum Chorób Płuc w Olsztynie | [https://park.paymove.io/741db750-f088-4e1a-8610-f67c75013059](https://park.paymove.io/741db750-f088-4e1a-8610-f67c75013059) |
| Olsztyn | Olsztyn - Wojewódzki Zespół Lecznictwa Psychiatrycznego w Olsztynie | [https://park.paymove.io/dcf3595f-ea22-4c14-80ac-bd3b87c5f34c](https://park.paymove.io/dcf3595f-ea22-4c14-80ac-bd3b87c5f34c) |
| Olsztyn | Olsztyn – Żołnierska 16 | [https://park.paymove.io/4af8ec0f-bd7a-4c29-bb60-c808f703b79b](https://park.paymove.io/4af8ec0f-bd7a-4c29-bb60-c808f703b79b) |
| Olsztyn | Olsztyn – Żołnierska 19A | [https://park.paymove.io/caa890bc-5644-448e-95f5-16decb1f8007](https://park.paymove.io/caa890bc-5644-448e-95f5-16decb1f8007) |
| Olsztyn | ul. Kołobrzeska 50 | [https://park.paymove.io/c3aa2cb9-1a1e-4a76-842f-82b047b676fb](https://park.paymove.io/c3aa2cb9-1a1e-4a76-842f-82b047b676fb) |
| Opole | Dworzec PKP Opole Główne | [https://park.paymove.io/cc582c91-9d21-4010-901a-89c9a0e51ee8](https://park.paymove.io/cc582c91-9d21-4010-901a-89c9a0e51ee8) |
| Ostrów Wielkopolski | Dworzec PKP Ostrów Wielkopolski | [https://park.paymove.io/caa0](https://park.paymove.io/caa0) |
| Pisz | ul. Warszawska | [https://park.paymove.io/50bc6b98-6497-424a-8f17-04411afeac54](https://park.paymove.io/50bc6b98-6497-424a-8f17-04411afeac54) |
| Police | Grzybowa 1 | [https://park.paymove.io/413c6ca4-2b6c-413b-8449-2d48e358dbf3](https://park.paymove.io/413c6ca4-2b6c-413b-8449-2d48e358dbf3) |
| Poznań | Poznań - Dymka - WEIP - abonament 30 dni | [https://park.paymove.io/fa079b39-01c6-40b7-bba5-3be0db79c369](https://park.paymove.io/fa079b39-01c6-40b7-bba5-3be0db79c369) |
| Poznań | Poznań ZOO - autobusy | [https://park.paymove.io/17cd38f8-4cbc-4920-b0b6-b094eec4df0b](https://park.paymove.io/17cd38f8-4cbc-4920-b0b6-b094eec4df0b) |
| Poznań | Poznań ZOO - samochody osobowe | [https://park.paymove.io/2a3e32e1-33a8-46cb-8a5c-358979267b43](https://park.paymove.io/2a3e32e1-33a8-46cb-8a5c-358979267b43) |
| Przasnysz | Samodzielny Publiczny ZOZ, ul. Sadowa 9 | [https://park.paymove.io/0d262f79-07de-46cf-8626-810a5654eaf9](https://park.paymove.io/0d262f79-07de-46cf-8626-810a5654eaf9) |
| Pszczyna | Pszczyna - Dworcowa 27 | [https://park.paymove.io/c4a59507-4344-49ec-837f-89e9c4c8a4d3](https://park.paymove.io/c4a59507-4344-49ec-837f-89e9c4c8a4d3) |
| Pszczyna | ul. Szymanowskiego 23 | [https://park.paymove.io/9918c630-827f-4ab7-a396-94792d39e3b1](https://park.paymove.io/9918c630-827f-4ab7-a396-94792d39e3b1) |
| Puck | 1-go Maja SPP | [https://park.paymove.io/176892d9-91a8-4f26-82de-87a70b5a65f5](https://park.paymove.io/176892d9-91a8-4f26-82de-87a70b5a65f5) |
| Puck | 10-go Lutego PP | [https://park.paymove.io/1065c82e-57cf-468d-8f8c-dc56210505c5](https://park.paymove.io/1065c82e-57cf-468d-8f8c-dc56210505c5) |
| Puck | 10-go Lutego SPP | [https://park.paymove.io/5ad7d94b-5e12-41ee-8def-a073aca2be65](https://park.paymove.io/5ad7d94b-5e12-41ee-8def-a073aca2be65) |
| Puck | Aleja Ceynowy SPP | [https://park.paymove.io/1fa06bb4-6049-49ac-92bf-533a04045eae](https://park.paymove.io/1fa06bb4-6049-49ac-92bf-533a04045eae) |
| Puck | Aleja Lipowa SPP | [https://park.paymove.io/bf1b2162-5f1e-41af-860d-a74791dd699b](https://park.paymove.io/bf1b2162-5f1e-41af-860d-a74791dd699b) |
| Puck | Elizy Orzeszkowej Starostwo Powiatowe SPP | [https://park.paymove.io/493cf505-0cc8-421b-b1ed-b297afdae47c](https://park.paymove.io/493cf505-0cc8-421b-b1ed-b297afdae47c) |
| Puck | Elizy Orzeszkowej przy parku SPP | [https://park.paymove.io/d41a9195-3d05-4206-8ca5-aa601a67638a](https://park.paymove.io/d41a9195-3d05-4206-8ca5-aa601a67638a) |
| Puck | Judyckiego SPP | [https://park.paymove.io/6569e9b0-e70b-4ed6-83f9-c9630c3f0f25](https://park.paymove.io/6569e9b0-e70b-4ed6-83f9-c9630c3f0f25) |
| Puck | Nowy Świat PP | [https://park.paymove.io/035b5516-007b-464a-bbf3-d3b273f466fa](https://park.paymove.io/035b5516-007b-464a-bbf3-d3b273f466fa) |
| Puck | Plac Obrońców Wybrzeża SPP | [https://park.paymove.io/f0b1c89a-cf1e-4f89-a8b0-e00d84bbe9f3](https://park.paymove.io/f0b1c89a-cf1e-4f89-a8b0-e00d84bbe9f3) |
| Puck | Róg ul. 1-go Maja i Al. Lipowej PP | [https://park.paymove.io/7aa4ae37-0181-4568-903b-8176322ab959](https://park.paymove.io/7aa4ae37-0181-4568-903b-8176322ab959) |
| Puck | Sambora SPP | [https://park.paymove.io/5ea8bef5-beee-40b8-8352-69c450f9585e](https://park.paymove.io/5ea8bef5-beee-40b8-8352-69c450f9585e) |
| Puck | Wałowa PP | [https://park.paymove.io/af6d8495-881e-44fb-ae5f-a290dcfe2559](https://park.paymove.io/af6d8495-881e-44fb-ae5f-a290dcfe2559) |
| Puck | Wałowa SPP | [https://park.paymove.io/65281ca7-cefa-4a69-830a-cb96f5e124cb](https://park.paymove.io/65281ca7-cefa-4a69-830a-cb96f5e124cb) |
| Puck | Wojska Polskiego SPP | [https://park.paymove.io/68b94840-b299-43fc-95fc-d2c118ea3404](https://park.paymove.io/68b94840-b299-43fc-95fc-d2c118ea3404) |
| Puck | Zamkowa PP | [https://park.paymove.io/9718b0a9-5a59-4899-adc2-f3427b2b4f81](https://park.paymove.io/9718b0a9-5a59-4899-adc2-f3427b2b4f81) |
| Radom | ul. Wyścigowa 41 | [https://park.paymove.io/4fd1b936-39f0-43df-98e3-a0dfd422e149](https://park.paymove.io/4fd1b936-39f0-43df-98e3-a0dfd422e149) |
| Radzyń Podlaski | Strefa Płatnego Parkowania w Radzyniu Podlaskim | [https://park.paymove.io/f5f6](https://park.paymove.io/f5f6) |
| Ruda Śląska | ul. Piłsudskiego 16 | [https://park.paymove.io/a4e6a2d8-0172-4e4b-9d5c-14af5b79b0e4](https://park.paymove.io/a4e6a2d8-0172-4e4b-9d5c-14af5b79b0e4) |
| Ruda Śląska | ul. Teatralna 7 | [https://park.paymove.io/dede84f9-bc3d-464e-85d2-40bec9662bb4](https://park.paymove.io/dede84f9-bc3d-464e-85d2-40bec9662bb4) |
| Rybnik | Pniowska (plaża) | [https://park.paymove.io/18f8](https://park.paymove.io/18f8) |
| Rybnik | Pniowska (za groblą) | [https://park.paymove.io/91d5](https://park.paymove.io/91d5) |
| Rybnik | Rudzka (Pniowiec) | [https://park.paymove.io/2f92](https://park.paymove.io/2f92) |
| Rybnik | Strefa Płatnego Parkowania w Rybniku | [https://park.paymove.io/fe6e](https://park.paymove.io/fe6e) |
| Rybnik | Sławików | [https://park.paymove.io/d2bf](https://park.paymove.io/d2bf) |
| Sopot | Ogrodowa 6a | [https://park.paymove.io/81c4](https://park.paymove.io/81c4) |
| Sopot | Sopot Tenis Klub Osiedlowa | [https://park.paymove.io/489d404d-c4fa-42e2-b230-a3014e1323c1](https://park.paymove.io/489d404d-c4fa-42e2-b230-a3014e1323c1) |
| Sopot | Sopot Tenis Klub Tenisowa | [https://park.paymove.io/984399af-fdcb-45d8-856f-b797a076ab5c](https://park.paymove.io/984399af-fdcb-45d8-856f-b797a076ab5c) |
| Sopot | Sopot – Sofitel Grand Sopot | [https://park.paymove.io/09d6ce12-5331-4fcf-9edb-103d89845683](https://park.paymove.io/09d6ce12-5331-4fcf-9edb-103d89845683) |
| Stalowa Wola | Okulickiego 2 | [https://park.paymove.io/22a0](https://park.paymove.io/22a0) |
| Stalowa Wola | Okulickiego 2 - abonament 30 dni | [https://park.paymove.io/9d29](https://park.paymove.io/9d29) |
| Szczecin | Nabrzeże Wieleckie Trasa Zamkowa *(+ 395 SPP street zones in Section 3.2)* | [https://park.paymove.io/lx4h](https://park.paymove.io/lx4h) |
| Szczecin | Płatny Parking Niestrzeżony pod Trasą Zamkową *(+ 395 SPP street zones in Section 3.2)* | [https://park.paymove.io/86061819-bfbb-4ecd-a098-d97c90ac280b](https://park.paymove.io/86061819-bfbb-4ecd-a098-d97c90ac280b) |
| Szczytno | Galeria Mazur | [https://park.paymove.io/00dfe67a-c1f5-4829-8633-d7c3b05f5011](https://park.paymove.io/00dfe67a-c1f5-4829-8633-d7c3b05f5011) |
| Słupsk | Słupsk, 11 Listopada | [https://park.paymove.io/1a15224b-bcae-484d-b0a7-786715a9805a](https://park.paymove.io/1a15224b-bcae-484d-b0a7-786715a9805a) |
| Słupsk | Słupsk, Westerplatte 64 | [https://park.paymove.io/9b6636d1-d927-41e8-9e64-6609758c62cb](https://park.paymove.io/9b6636d1-d927-41e8-9e64-6609758c62cb) |
| Tarnów | Dworzec PKP Tarnów | [https://park.paymove.io/d4321a82-70b1-4b16-9a92-11897f1bf040](https://park.paymove.io/d4321a82-70b1-4b16-9a92-11897f1bf040) |
| Tarnów | Tarnów – Dąbrowskiego | [https://park.paymove.io/fbb43aeb-bdd2-4452-b653-b4e43b0559ad](https://park.paymove.io/fbb43aeb-bdd2-4452-b653-b4e43b0559ad) |
| Toruń | Arena Toruń - 30 dni motocykl | [https://park.paymove.io/7a67966e-7101-422c-8b3e-eb9a2b616b89](https://park.paymove.io/7a67966e-7101-422c-8b3e-eb9a2b616b89) |
| Toruń | Arena Toruń - 30 dni samochód osobowy | [https://park.paymove.io/9dccd4e8-25e8-404c-8210-d86a0b151347](https://park.paymove.io/9dccd4e8-25e8-404c-8210-d86a0b151347) |
| Toruń | Arena Toruń - autokary | [https://park.paymove.io/6dcc27d3-7829-4276-9021-4a9b019b9952](https://park.paymove.io/6dcc27d3-7829-4276-9021-4a9b019b9952) |
| Toruń | Arena Toruń - samochody osobowe | [https://park.paymove.io/0804132b-0d27-4fb5-b1a8-e51be65b0f09](https://park.paymove.io/0804132b-0d27-4fb5-b1a8-e51be65b0f09) |
| Toruń | Toruń, Podgórska 12a | [https://park.paymove.io/c41a13a8-8843-4ae1-b804-1a0f1337ae32](https://park.paymove.io/c41a13a8-8843-4ae1-b804-1a0f1337ae32) |
| Trzebinia | Trzebinia - Ośrodek Rekreacyjny Chechło - posiadacze karty trzebińskiej | [https://park.paymove.io/6a16](https://park.paymove.io/6a16) |
| Warszawa | Dworzec PKP Warszawa Centralna | [https://park.paymove.io/50d4cd96-bf7d-47b9-a8b6-df636de75357](https://park.paymove.io/50d4cd96-bf7d-47b9-a8b6-df636de75357) |
| Warszawa | Dworzec PKP Warszawa Gdańska | [https://park.paymove.io/adaeac32-8140-4655-9e37-202987f1b553](https://park.paymove.io/adaeac32-8140-4655-9e37-202987f1b553) |
| Warszawa | Dworzec PKP Warszawa Wschodnia | [https://park.paymove.io/20afc570-e99b-4902-b4e2-be9c747c84ef](https://park.paymove.io/20afc570-e99b-4902-b4e2-be9c747c84ef) |
| Warszawa | Dworzec PKP Warszawa Wschodnia ul. Lubelska (parking długoterminowy) | [https://park.paymove.io/16ce](https://park.paymove.io/16ce) |
| Warszawa | Dworzec PKP Warszawa Wschodnia ul. Lubelska (parking krótkoterminowy) | [https://park.paymove.io/091a](https://park.paymove.io/091a) |
| Warszawa | Dworzec PKP Warszawa Wschodnia ul. Lubelska (parking krótkoterminowy) - autobusy | [https://park.paymove.io/767f](https://park.paymove.io/767f) |
| Warszawa | Parking Demonstracyjny EuroPark | [https://park.paymove.io/8cae0b60-d9fd-462f-854b-38fa899e6ff5](https://park.paymove.io/8cae0b60-d9fd-462f-854b-38fa899e6ff5) |
| Wejherowo | Szpital Specjalistyczny im. F. Ceynowy | [https://park.paymove.io/67dfa69e-acda-4f16-8ee3-874c8eee65bb](https://park.paymove.io/67dfa69e-acda-4f16-8ee3-874c8eee65bb) |
| Wieliczka | FITPARKING P1 Camper/Mały Bus | [https://park.paymove.io/c77d8010-2a10-43ce-86f1-08852cb27e27](https://park.paymove.io/c77d8010-2a10-43ce-86f1-08852cb27e27) |
| Wieliczka | FITPARKING P1 Wieliczka | [https://park.paymove.io/41610c0e-51d9-4e7f-9759-8edb750f159f](https://park.paymove.io/41610c0e-51d9-4e7f-9759-8edb750f159f) |
| Wieliczka | FITPARKING P2 Wieliczka | [https://park.paymove.io/37ad6a3f-77a8-4a78-adc3-62bb5da1d0c7](https://park.paymove.io/37ad6a3f-77a8-4a78-adc3-62bb5da1d0c7) |
| Wieliczka | Goliana 10 | [https://park.paymove.io/0fbc](https://park.paymove.io/0fbc) |
| Wieliczka | Niecała (Cmentarz) | [https://park.paymove.io/0164](https://park.paymove.io/0164) |
| Wieliczka | Słowackiego 12 | [https://park.paymove.io/9759](https://park.paymove.io/9759) |
| Wieliczka | Słowackiego 3 | [https://park.paymove.io/8254](https://park.paymove.io/8254) |
| Wiązowna | CH JARTON - bramka | [https://park.paymove.io/c3a160ab-1ca0-465e-8147-709e0576d269](https://park.paymove.io/c3a160ab-1ca0-465e-8147-709e0576d269) |
| Wiązowna | ul. Lubelska 78 | [https://park.paymove.io/0664c524-05f7-4c00-b7ee-c3eddc53bdca](https://park.paymove.io/0664c524-05f7-4c00-b7ee-c3eddc53bdca) |
| Wodzisław Śląski | Parking Miejski Niestrzeżony w Wodzisławiu Śląskim | [https://park.paymove.io/cc87](https://park.paymove.io/cc87) |
| Wodzisław Śląski | Strefa Płatnego Parkowania w Wodzisławiu Śląskim | [https://park.paymove.io/2f3f](https://park.paymove.io/2f3f) |
| Wrocław | Dworzec PKP Wrocław Główny | [https://park.paymove.io/6bf749b6-776d-402b-a6a8-dfbfe0d519cc](https://park.paymove.io/6bf749b6-776d-402b-a6a8-dfbfe0d519cc) |
| Wrocław | Dworzec PKP Wrocław Główny (Parking podziemny) | [https://park.paymove.io/2434b2db-4665-4267-9f5e-c50133ff0595](https://park.paymove.io/2434b2db-4665-4267-9f5e-c50133ff0595) |
| Wrocław | TARCZYŃSKI ARENA - Camper Park 4 osoby bez dostępu do prądu | [https://park.paymove.io/704f076a-60b8-4fe7-b980-3df5c6f9b751](https://park.paymove.io/704f076a-60b8-4fe7-b980-3df5c6f9b751) |
| Wrocław | TARCZYŃSKI ARENA - Camper Park 4 osoby z dostępem do prądu | [https://park.paymove.io/ece1cae9-7658-4056-adfe-15aa21c31ee6](https://park.paymove.io/ece1cae9-7658-4056-adfe-15aa21c31ee6) |
| Wrocław | TARCZYŃSKI ARENA - Camper Park 6 osób bez dostępu do prądu | [https://park.paymove.io/c14db515-f4f5-496d-8ca5-a43d7add395b](https://park.paymove.io/c14db515-f4f5-496d-8ca5-a43d7add395b) |
| Wrocław | TARCZYŃSKI ARENA - Camper Park 6 osób z dostępem do prądu | [https://park.paymove.io/172e65da-51c7-4781-8f39-ad77133992dc](https://park.paymove.io/172e65da-51c7-4781-8f39-ad77133992dc) |
| Wrocław | TARCZYŃSKI ARENA - Camper Park bez dostępu do prądu na 30 dni | [https://park.paymove.io/c0f4673b-2387-4a88-ad47-9b37f1dabbcc](https://park.paymove.io/c0f4673b-2387-4a88-ad47-9b37f1dabbcc) |
| Wrocław | TARCZYŃSKI ARENA - Camper Park z dostępem do prądu na 30 dni | [https://park.paymove.io/6208aa0c-7824-414c-a1f2-044b9021fcbf](https://park.paymove.io/6208aa0c-7824-414c-a1f2-044b9021fcbf) |
| Wrocław | TARCZYŃSKI ARENA - Le Mans | [https://park.paymove.io/3aa788da-3b7d-4cd3-90d1-c7ddc294b5a4](https://park.paymove.io/3aa788da-3b7d-4cd3-90d1-c7ddc294b5a4) |
| Wrocław | TARCZYŃSKI ARENA - broadcast | [https://park.paymove.io/c2d42a55-e966-4611-b22a-d60736f8a133](https://park.paymove.io/c2d42a55-e966-4611-b22a-d60736f8a133) |
| Wrocław | TARCZYŃSKI ARENA - ogólna | [https://park.paymove.io/af87c361-e792-41a8-bdb9-987e4e1156d3](https://park.paymove.io/af87c361-e792-41a8-bdb9-987e4e1156d3) |
| Wrocław | Wrocław - Awicenny 45 - ALDI - WEIP - abonament 30 dni | [https://park.paymove.io/af15a635-542c-4334-a608-5db4fc8cbe1a](https://park.paymove.io/af15a635-542c-4334-a608-5db4fc8cbe1a) |
| Władysławowo | Bohaterów Kaszubskich | [https://park.paymove.io/85c8](https://park.paymove.io/85c8) |
| Władysławowo | SPP WŁADYSŁAWOWO - od 15 VI do 31 VIII | [https://park.paymove.io/1870](https://park.paymove.io/1870) |
| Władysławowo | SPP WŁADYSŁAWOWO - od 15 VI do 31 VIII - 2 | [https://park.paymove.io/4a84](https://park.paymove.io/4a84) |
| Władysławowo | Starowiejska - samochody osobowe | [https://park.paymove.io/94b1](https://park.paymove.io/94b1) |
| Zabrze | Zabrze, 3 Maja 93 - samochody osobowe i motocykle | [https://park.paymove.io/80ef](https://park.paymove.io/80ef) |
| Zabrze | Zabrze, De Gaulle’a 75 | [https://park.paymove.io/6bb4e596-c3a4-4a9d-b2ee-6b2f0db6901f](https://park.paymove.io/6bb4e596-c3a4-4a9d-b2ee-6b2f0db6901f) |
| Zabrze | ul. Banachiewicza 15a | [https://park.paymove.io/235df86c-5ebe-414f-88c2-a8020b6d73ce](https://park.paymove.io/235df86c-5ebe-414f-88c2-a8020b6d73ce) |
| Zabrze | ul. Skłodowskiej - Curie 24 | [https://park.paymove.io/770275e1-9337-4812-b7cc-5c36fd9dd995](https://park.paymove.io/770275e1-9337-4812-b7cc-5c36fd9dd995) |
| Zabrze | ul. Tatarkiewicza 12 | [https://park.paymove.io/c9093a12-d44a-42a8-80b7-3e87be70d5e2](https://park.paymove.io/c9093a12-d44a-42a8-80b7-3e87be70d5e2) |
| Łomża | al. Legionów 52 | [https://park.paymove.io/88734ab8-f2ac-4259-8b5a-723a92af5b01](https://park.paymove.io/88734ab8-f2ac-4259-8b5a-723a92af5b01) |
| Łódź | Bandurskiego 49 | [https://park.paymove.io/2ade47e5-2d61-4e35-8753-da3f4310391a](https://park.paymove.io/2ade47e5-2d61-4e35-8753-da3f4310391a) |
| Łódź | Rydla 31 | [https://park.paymove.io/ae293c0a-bcb4-4f53-82cc-856983cd8fa4](https://park.paymove.io/ae293c0a-bcb4-4f53-82cc-856983cd8fa4) |
| Łódź | ul. Łagiewnicka 54/56 | [https://park.paymove.io/2888e2ee-e397-47eb-b076-19f6ae3ea322](https://park.paymove.io/2888e2ee-e397-47eb-b076-19f6ae3ea322) |
| Świdnik | Wyszyńskiego 22 | [https://park.paymove.io/e2c0](https://park.paymove.io/e2c0) |
| Świdnik | Wyszyńskiego 22 - abonament 30 dni | [https://park.paymove.io/2149](https://park.paymove.io/2149) |
| Żelazna | PKP Żelazna | [https://park.paymove.io/21a9145b-6beb-4fa5-ab36-2c3c928bd023](https://park.paymove.io/21a9145b-6beb-4fa5-ab36-2c3c928bd023) |
| Żory | Żory - Bankowa 6 | [https://park.paymove.io/542fbe60-6399-4632-b951-64f71ffebfb9](https://park.paymove.io/542fbe60-6399-4632-b951-64f71ffebfb9) |

</details>

<details>
<summary><strong>Show all 396 Municipal Paid Parking (SPP) street zones in Szczecin (Location / Name / URL)</strong></summary>

<br />

| Location | Street / Sub-Zone (Szczecin SPP) | URL |
| :--- | :--- | :--- |
| Szczecin | SPP — 3 Maja 25 Przychodnia | [https://park.paymove.io/fdlf](https://park.paymove.io/fdlf) |
| Szczecin | SPP — 3-go Maja 13a / Żabka | [https://park.paymove.io/62yj](https://park.paymove.io/62yj) |
| Szczecin | SPP — 5 -Lipca 42 | [https://park.paymove.io/c4ln](https://park.paymove.io/c4ln) |
| Szczecin | SPP — 5 Lipca / Bol. Śmiałego | [https://park.paymove.io/79dn](https://park.paymove.io/79dn) |
| Szczecin | SPP — 5 Lipca 11B | [https://park.paymove.io/pvl9](https://park.paymove.io/pvl9) |
| Szczecin | SPP — A. Mickiewicza/Pocztowa | [https://park.paymove.io/msm7](https://park.paymove.io/msm7) |
| Szczecin | SPP — Adama Mickiewicza | [https://park.paymove.io/84nm](https://park.paymove.io/84nm) |
| Szczecin | SPP — Admiralska 1 | [https://park.paymove.io/6yer](https://park.paymove.io/6yer) |
| Szczecin | SPP — Admiralska 3 Park | [https://park.paymove.io/qcbv](https://park.paymove.io/qcbv) |
| Szczecin | SPP — aleja Bohaterów Warszawy 12a | [https://park.paymove.io/86d4](https://park.paymove.io/86d4) |
| Szczecin | SPP — aleja Bohaterów Warszawy 98 | [https://park.paymove.io/spec](https://park.paymove.io/spec) |
| Szczecin | SPP — B. Krzywoustego 22 | [https://park.paymove.io/89m6](https://park.paymove.io/89m6) |
| Szczecin | SPP — B. Krzywoustego 25 | [https://park.paymove.io/qmlw](https://park.paymove.io/qmlw) |
| Szczecin | SPP — B. Krzywoustego 50 | [https://park.paymove.io/otzo](https://park.paymove.io/otzo) |
| Szczecin | SPP — B. Śmiałego 19 | [https://park.paymove.io/g6eh](https://park.paymove.io/g6eh) |
| Szczecin | SPP — B. Śmiałego 30 | [https://park.paymove.io/0v4a](https://park.paymove.io/0v4a) |
| Szczecin | SPP — B. Śmiałego 39 | [https://park.paymove.io/7z0j](https://park.paymove.io/7z0j) |
| Szczecin | SPP — B. Śmiałego 43 | [https://park.paymove.io/2id1](https://park.paymove.io/2id1) |
| Szczecin | SPP — B. Śmiałego 45 | [https://park.paymove.io/jrau](https://park.paymove.io/jrau) |
| Szczecin | SPP — B. Śmiałego 49 | [https://park.paymove.io/bc1g](https://park.paymove.io/bc1g) |
| Szczecin | SPP — Bogurodzicy 2 Pasmanteria | [https://park.paymove.io/qtfe](https://park.paymove.io/qtfe) |
| Szczecin | SPP — Bogurodzicy Bankomat PKO | [https://park.paymove.io/pz8q](https://park.paymove.io/pz8q) |
| Szczecin | SPP — Bogusława 11 Solarium | [https://park.paymove.io/umon](https://park.paymove.io/umon) |
| Szczecin | SPP — Bogusława 16 | [https://park.paymove.io/dxpw](https://park.paymove.io/dxpw) |
| Szczecin | SPP — Bogusława 40 Helios | [https://park.paymove.io/3gmf](https://park.paymove.io/3gmf) |
| Szczecin | SPP — Boh. Getta Warszawskiego 23/24 | [https://park.paymove.io/mj4m](https://park.paymove.io/mj4m) |
| Szczecin | SPP — Boh. Warszawy 52 | [https://park.paymove.io/xmku](https://park.paymove.io/xmku) |
| Szczecin | SPP — Boh. Warszawy 6 | [https://park.paymove.io/jdoe](https://park.paymove.io/jdoe) |
| Szczecin | SPP — Boh.Getta Warszawskiego 12/13 | [https://park.paymove.io/qu4o](https://park.paymove.io/qu4o) |
| Szczecin | SPP — Boh.Getta Warszawskiego 18 reklamy | [https://park.paymove.io/qotw](https://park.paymove.io/qotw) |
| Szczecin | SPP — Boh.Getta Warszawskiego 6 warzywniak/kiosk | [https://park.paymove.io/9q4e](https://park.paymove.io/9q4e) |
| Szczecin | SPP — Bohaterów Warszawy 104 | [https://park.paymove.io/zh2y](https://park.paymove.io/zh2y) |
| Szczecin | SPP — Bohaterów Warszawy 118 | [https://park.paymove.io/nh9o](https://park.paymove.io/nh9o) |
| Szczecin | SPP — Bohaterów Warszawy 14 | [https://park.paymove.io/4fxm](https://park.paymove.io/4fxm) |
| Szczecin | SPP — Bohaterów Warszawy 22 | [https://park.paymove.io/4olr](https://park.paymove.io/4olr) |
| Szczecin | SPP — Bohaterów Warszawy 33 | [https://park.paymove.io/py1l](https://park.paymove.io/py1l) |
| Szczecin | SPP — Bohaterów Warszawy 74 | [https://park.paymove.io/s1vu](https://park.paymove.io/s1vu) |
| Szczecin | SPP — Bohaterów Warszawy pomiędzy rondem W. Siwka a J. Bema | [https://park.paymove.io/kpo5](https://park.paymove.io/kpo5) |
| Szczecin | SPP — Bohaterów Warszawy/Garncarska | [https://park.paymove.io/3t1q](https://park.paymove.io/3t1q) |
| Szczecin | SPP — Bohaterów Warszawy/K. Pułaskiego | [https://park.paymove.io/fe6n](https://park.paymove.io/fe6n) |
| Szczecin | SPP — Bohaterów Warszawy/Legionów Dąbrowskiego | [https://park.paymove.io/pb5v](https://park.paymove.io/pb5v) |
| Szczecin | SPP — Bulwar Piastowski 1 na dole | [https://park.paymove.io/21lg](https://park.paymove.io/21lg) |
| Szczecin | SPP — Bulwar Piastowski 2 na dole | [https://park.paymove.io/1lam](https://park.paymove.io/1lam) |
| Szczecin | SPP — Czackiego | [https://park.paymove.io/029w](https://park.paymove.io/029w) |
| Szczecin | SPP — Czarnieckiego Komenda | [https://park.paymove.io/uiau](https://park.paymove.io/uiau) |
| Szczecin | SPP — Drzymały 10 Notariusz | [https://park.paymove.io/64xx](https://park.paymove.io/64xx) |
| Szczecin | SPP — Drzymały 12 były Falck | [https://park.paymove.io/6s47](https://park.paymove.io/6s47) |
| Szczecin | SPP — Drzymały 5 | [https://park.paymove.io/612e](https://park.paymove.io/612e) |
| Szczecin | SPP — Dworcowa 1 Fontanna | [https://park.paymove.io/rwn7](https://park.paymove.io/rwn7) |
| Szczecin | SPP — Dworcowa 20 v/v Busów | [https://park.paymove.io/f5js](https://park.paymove.io/f5js) |
| Szczecin | SPP — Dworcowa 7 stare wejście do Księżnicy | [https://park.paymove.io/cqj9](https://park.paymove.io/cqj9) |
| Szczecin | SPP — Dworcowa v/v Warta | [https://park.paymove.io/m0xp](https://park.paymove.io/m0xp) |
| Szczecin | SPP — Dworzec PKP tunel | [https://park.paymove.io/b2m8](https://park.paymove.io/b2m8) |
| Szczecin | SPP — Dworzec PKP wejscie główne | [https://park.paymove.io/q4im](https://park.paymove.io/q4im) |
| Szczecin | SPP — Edmunda Bałuki 11 PKO | [https://park.paymove.io/cmnv](https://park.paymove.io/cmnv) |
| Szczecin | SPP — Edmunda Bałuki 16 Pierogarnia | [https://park.paymove.io/f7c2](https://park.paymove.io/f7c2) |
| Szczecin | SPP — Edmunda Bałuki 24 Grawer | [https://park.paymove.io/e5s6](https://park.paymove.io/e5s6) |
| Szczecin | SPP — Edmunda Bałuki 8 Park | [https://park.paymove.io/x85t](https://park.paymove.io/x85t) |
| Szczecin | SPP — F. Tarczyńskiego 4 | [https://park.paymove.io/y1ef](https://park.paymove.io/y1ef) |
| Szczecin | SPP — Farna 9 | [https://park.paymove.io/p2ff](https://park.paymove.io/p2ff) |
| Szczecin | SPP — Farna/PZU | [https://park.paymove.io/f12a](https://park.paymove.io/f12a) |
| Szczecin | SPP — Felczaka 14 przedszkole | [https://park.paymove.io/oo4t](https://park.paymove.io/oo4t) |
| Szczecin | SPP — Felczaka 16 | [https://park.paymove.io/gh38](https://park.paymove.io/gh38) |
| Szczecin | SPP — Felczaka 18 Garmażerka | [https://park.paymove.io/btds](https://park.paymove.io/btds) |
| Szczecin | SPP — Felczaka UM wjazd do SM | [https://park.paymove.io/zrrj](https://park.paymove.io/zrrj) |
| Szczecin | SPP — Felczaka/Wąska | [https://park.paymove.io/agx7](https://park.paymove.io/agx7) |
| Szczecin | SPP — G. Narutowicza 10A | [https://park.paymove.io/p5zg](https://park.paymove.io/p5zg) |
| Szczecin | SPP — G. Narutowicza 17A | [https://park.paymove.io/0utw](https://park.paymove.io/0utw) |
| Szczecin | SPP — G. Narutowicza/Królowej Jadwigi | [https://park.paymove.io/jg06](https://park.paymove.io/jg06) |
| Szczecin | SPP — Grodzka 10 | [https://park.paymove.io/3a9d](https://park.paymove.io/3a9d) |
| Szczecin | SPP — Grodzka 36 v/v szkoły | [https://park.paymove.io/7hoy](https://park.paymove.io/7hoy) |
| Szczecin | SPP — Grodzka 6 v/v Katedry | [https://park.paymove.io/5a4v](https://park.paymove.io/5a4v) |
| Szczecin | SPP — H.Pobożnego 9b v/v akademików | [https://park.paymove.io/jtld](https://park.paymove.io/jtld) |
| Szczecin | SPP — Henryka Pobożnego 1 Kwiaciarki | [https://park.paymove.io/jsju](https://park.paymove.io/jsju) |
| Szczecin | SPP — Henryka Pobożnego 4 na rogu Zygmunta Starego | [https://park.paymove.io/p6bg](https://park.paymove.io/p6bg) |
| Szczecin | SPP — Herbowa 18 | [https://park.paymove.io/ts4w](https://park.paymove.io/ts4w) |
| Szczecin | SPP — Herbowa 29 | [https://park.paymove.io/eh59](https://park.paymove.io/eh59) |
| Szczecin | SPP — J. Bema 7 | [https://park.paymove.io/rz9k](https://park.paymove.io/rz9k) |
| Szczecin | SPP — J. Bema/K. Pułaskiego | [https://park.paymove.io/qx98](https://park.paymove.io/qx98) |
| Szczecin | SPP — Jacka Malczewskiego 10 | [https://park.paymove.io/ava3](https://park.paymove.io/ava3) |
| Szczecin | SPP — Jadwigi 14 Antykwariat | [https://park.paymove.io/ldux](https://park.paymove.io/ldux) |
| Szczecin | SPP — Jadwigi 3 od Ściegiennego 1szy | [https://park.paymove.io/tdte](https://park.paymove.io/tdte) |
| Szczecin | SPP — Jadwigi 38 Genial | [https://park.paymove.io/qiix](https://park.paymove.io/qiix) |
| Szczecin | SPP — Jadwigi 42 v/v Szkoły | [https://park.paymove.io/t72j](https://park.paymove.io/t72j) |
| Szczecin | SPP — Jagiellońska 18 | [https://park.paymove.io/kagx](https://park.paymove.io/kagx) |
| Szczecin | SPP — Jagiellońska 3-4 Koch | [https://park.paymove.io/z4ua](https://park.paymove.io/z4ua) |
| Szczecin | SPP — Jagiellońska 8 Lampy | [https://park.paymove.io/8qjd](https://park.paymove.io/8qjd) |
| Szczecin | SPP — Jagiellońska 81 | [https://park.paymove.io/99tx](https://park.paymove.io/99tx) |
| Szczecin | SPP — Jagiellońska 85 SPA | [https://park.paymove.io/4bff](https://park.paymove.io/4bff) |
| Szczecin | SPP — Jagiellońska 96 Skarbiec Nocny | [https://park.paymove.io/tmxh](https://park.paymove.io/tmxh) |
| Szczecin | SPP — Jana Pawla II 15 Żabka | [https://park.paymove.io/qhwm](https://park.paymove.io/qhwm) |
| Szczecin | SPP — Jana Pawla II 20 Secesja Cafe | [https://park.paymove.io/sl41](https://park.paymove.io/sl41) |
| Szczecin | SPP — Jana Pawla II 22 | [https://park.paymove.io/6so5](https://park.paymove.io/6so5) |
| Szczecin | SPP — Jana Pawla II 33 | [https://park.paymove.io/fxs9](https://park.paymove.io/fxs9) |
| Szczecin | SPP — Jana Pawla II 38 Spondylus | [https://park.paymove.io/6mdd](https://park.paymove.io/6mdd) |
| Szczecin | SPP — Jana Pawła II 3-4 Era | [https://park.paymove.io/k8t9](https://park.paymove.io/k8t9) |
| Szczecin | SPP — Jana Pawła II 46 Dywany | [https://park.paymove.io/uaev](https://park.paymove.io/uaev) |
| Szczecin | SPP — Jana Pawła II 50 Lwowska | [https://park.paymove.io/rr2p](https://park.paymove.io/rr2p) |
| Szczecin | SPP — Jana Pawła II 7a Foto Best | [https://park.paymove.io/f88e](https://park.paymove.io/f88e) |
| Szczecin | SPP — Jana z Kolna pomiędzy Storrady-świętosławy | [https://park.paymove.io/cd18](https://park.paymove.io/cd18) |
| Szczecin | SPP — Jana z Kolna/Kapitańska | [https://park.paymove.io/rv6k](https://park.paymove.io/rv6k) |
| Szczecin | SPP — Janosika/P. Skargi | [https://park.paymove.io/vku1](https://park.paymove.io/vku1) |
| Szczecin | SPP — Jarowita 5 od Wawelskiej 2gi | [https://park.paymove.io/8kfy](https://park.paymove.io/8kfy) |
| Szczecin | SPP — Jarowita 9 1szy od Wawelskiej | [https://park.paymove.io/hd8x](https://park.paymove.io/hd8x) |
| Szczecin | SPP — Jarowita WSM wjazd | [https://park.paymove.io/lbye](https://park.paymove.io/lbye) |
| Szczecin | SPP — K. Pułaskiego 10 | [https://park.paymove.io/5988](https://park.paymove.io/5988) |
| Szczecin | SPP — Kapitańska 3A | [https://park.paymove.io/vogl](https://park.paymove.io/vogl) |
| Szczecin | SPP — Kaszubska 27b v/v Orange | [https://park.paymove.io/c0q0](https://park.paymove.io/c0q0) |
| Szczecin | SPP — Kaszubska 30 | [https://park.paymove.io/ztz3](https://park.paymove.io/ztz3) |
| Szczecin | SPP — Kaszubska 31 Podstrefa A | [https://park.paymove.io/o5nx](https://park.paymove.io/o5nx) |
| Szczecin | SPP — Kaszubska 39 komenda | [https://park.paymove.io/uhdi](https://park.paymove.io/uhdi) |
| Szczecin | SPP — Kaszubska 4 | [https://park.paymove.io/miom](https://park.paymove.io/miom) |
| Szczecin | SPP — Kaszubska 59 Modelarski | [https://park.paymove.io/a6r0](https://park.paymove.io/a6r0) |
| Szczecin | SPP — Kaszubska Sąd | [https://park.paymove.io/5lmd](https://park.paymove.io/5lmd) |
| Szczecin | SPP — Kilińskiego/Wyzwolenia | [https://park.paymove.io/ksxi](https://park.paymove.io/ksxi) |
| Szczecin | SPP — Komandorska ostatni (B) | [https://park.paymove.io/uzip](https://park.paymove.io/uzip) |
| Szczecin | SPP — Kopernika 3 Pasaż A-Z | [https://park.paymove.io/yhih](https://park.paymove.io/yhih) |
| Szczecin | SPP — Kopernika 7 | [https://park.paymove.io/jijn](https://park.paymove.io/jijn) |
| Szczecin | SPP — Kordeckiego naprzeciwko wjazdu w ks. Witolda | [https://park.paymove.io/zmx7](https://park.paymove.io/zmx7) |
| Szczecin | SPP — Korsarzy 8 Zamek | [https://park.paymove.io/xgxk](https://park.paymove.io/xgxk) |
| Szczecin | SPP — Korzeniowskiego 1 Dyrekcja  PKP | [https://park.paymove.io/yi4r](https://park.paymove.io/yi4r) |
| Szczecin | SPP — Korzeniowskiego/Słowianin | [https://park.paymove.io/1h97](https://park.paymove.io/1h97) |
| Szczecin | SPP — Korzeniowskiego/Tobruk | [https://park.paymove.io/77no](https://park.paymove.io/77no) |
| Szczecin | SPP — Kr. K.Polskiej Przychodnia | [https://park.paymove.io/4xk1](https://park.paymove.io/4xk1) |
| Szczecin | SPP — Kr.Jadwigi 19 | [https://park.paymove.io/vp3d](https://park.paymove.io/vp3d) |
| Szczecin | SPP — Królowej Jadwigi 20A | [https://park.paymove.io/ielk](https://park.paymove.io/ielk) |
| Szczecin | SPP — Królowej Jadwigi 23 | [https://park.paymove.io/xhpo](https://park.paymove.io/xhpo) |
| Szczecin | SPP — Królowej Korony Polskiej 18 | [https://park.paymove.io/9e4l](https://park.paymove.io/9e4l) |
| Szczecin | SPP — Ks. Bogusława X 20 | [https://park.paymove.io/htnp](https://park.paymove.io/htnp) |
| Szczecin | SPP — Ks. Bogusława X 24 | [https://park.paymove.io/x1vc](https://park.paymove.io/x1vc) |
| Szczecin | SPP — Ks. Bogusława X/M. Langiewicza (Pl. Dziecka) | [https://park.paymove.io/2dr3](https://park.paymove.io/2dr3) |
| Szczecin | SPP — Ks. Bogusława X/W. Jagiełły | [https://park.paymove.io/v0mf](https://park.paymove.io/v0mf) |
| Szczecin | SPP — Ks. Witolda/Wilków Morskich | [https://park.paymove.io/rs05](https://park.paymove.io/rs05) |
| Szczecin | SPP — Księcia Świętopełka 3 | [https://park.paymove.io/oh3a](https://park.paymove.io/oh3a) |
| Szczecin | SPP — Księdza Piotra Skargi 18 | [https://park.paymove.io/i3bx](https://park.paymove.io/i3bx) |
| Szczecin | SPP — Księdza Piotra Skargi 25 | [https://park.paymove.io/5imu](https://park.paymove.io/5imu) |
| Szczecin | SPP — Księżnej Przybysławy 2 | [https://park.paymove.io/t1ff](https://park.paymove.io/t1ff) |
| Szczecin | SPP — Ku Słońcu 11 | [https://park.paymove.io/k7m4](https://park.paymove.io/k7m4) |
| Szczecin | SPP — Kujawska 7 | [https://park.paymove.io/sptj](https://park.paymove.io/sptj) |
| Szczecin | SPP — Langiewicza 3A | [https://park.paymove.io/roei](https://park.paymove.io/roei) |
| Szczecin | SPP — Legionów Dąbrowskiego 3 | [https://park.paymove.io/1etk](https://park.paymove.io/1etk) |
| Szczecin | SPP — Limanowskiego Sąd Rejonowy | [https://park.paymove.io/bvxk](https://park.paymove.io/bvxk) |
| Szczecin | SPP — Lutniana/Janosika | [https://park.paymove.io/3cpg](https://park.paymove.io/3cpg) |
| Szczecin | SPP — M. Kopernika 17A | [https://park.paymove.io/5qny](https://park.paymove.io/5qny) |
| Szczecin | SPP — M. Kopernika/ W. Jagełły | [https://park.paymove.io/veta](https://park.paymove.io/veta) |
| Szczecin | SPP — M. Langiewicza/ Królowej Jadwigi | [https://park.paymove.io/chg7](https://park.paymove.io/chg7) |
| Szczecin | SPP — M. Langiewicza/Piastów | [https://park.paymove.io/4ywy](https://park.paymove.io/4ywy) |
| Szczecin | SPP — Malczewskiego 2 | [https://park.paymove.io/x7os](https://park.paymove.io/x7os) |
| Szczecin | SPP — Malczewskiego/J. Kazimierza | [https://park.paymove.io/sb39](https://park.paymove.io/sb39) |
| Szczecin | SPP — Mariacka 10 Dental Center Zalmer | [https://park.paymove.io/ct2s](https://park.paymove.io/ct2s) |
| Szczecin | SPP — Mariacka ZBILK | [https://park.paymove.io/zpyp](https://park.paymove.io/zpyp) |
| Szczecin | SPP — Mazowiecka 11-12 Przedszkole | [https://park.paymove.io/hjdp](https://park.paymove.io/hjdp) |
| Szczecin | SPP — Mazowiecka 14 Pogotowie | [https://park.paymove.io/isnq](https://park.paymove.io/isnq) |
| Szczecin | SPP — Mazurska 11 przy Podhalańskiej na rogu | [https://park.paymove.io/7rwg](https://park.paymove.io/7rwg) |
| Szczecin | SPP — Mazurska 15 Stomatolog | [https://park.paymove.io/lhm0](https://park.paymove.io/lhm0) |
| Szczecin | SPP — Mazurska 19 | [https://park.paymove.io/27zo](https://park.paymove.io/27zo) |
| Szczecin | SPP — Mazurska 25 Cukiernia Bona | [https://park.paymove.io/4ulf](https://park.paymove.io/4ulf) |
| Szczecin | SPP — Mazurska 28 | [https://park.paymove.io/yizu](https://park.paymove.io/yizu) |
| Szczecin | SPP — Mazurska 4 Szkoła Sportowa | [https://park.paymove.io/ouqq](https://park.paymove.io/ouqq) |
| Szczecin | SPP — Mazurska 45a Bomis | [https://park.paymove.io/kun5](https://park.paymove.io/kun5) |
| Szczecin | SPP — Małkowskiego 17 | [https://park.paymove.io/hav5](https://park.paymove.io/hav5) |
| Szczecin | SPP — Małkowskiego 3 Kantory | [https://park.paymove.io/bk4x](https://park.paymove.io/bk4x) |
| Szczecin | SPP — Małkowskiego 8 Kiosk | [https://park.paymove.io/5a3g](https://park.paymove.io/5a3g) |
| Szczecin | SPP — Małkowskiego/Piastów Apteka | [https://park.paymove.io/mky7](https://park.paymove.io/mky7) |
| Szczecin | SPP — Małopolska 22 Focus | [https://park.paymove.io/24ad](https://park.paymove.io/24ad) |
| Szczecin | SPP — Małopolska 3 Oleńka | [https://park.paymove.io/qszw](https://park.paymove.io/qszw) |
| Szczecin | SPP — Małopolska 43 v/v Sąd | [https://park.paymove.io/h3qu](https://park.paymove.io/h3qu) |
| Szczecin | SPP — Małopolska 46a Rybarex | [https://park.paymove.io/2t56](https://park.paymove.io/2t56) |
| Szczecin | SPP — Małopolska 52 Lexus | [https://park.paymove.io/f3y0](https://park.paymove.io/f3y0) |
| Szczecin | SPP — Małopolska 8 Play | [https://park.paymove.io/5xtx](https://park.paymove.io/5xtx) |
| Szczecin | SPP — Małopolska v/v Filharmonii | [https://park.paymove.io/sve1](https://park.paymove.io/sve1) |
| Szczecin | SPP — Moniuszki 1 Szkoła Rysunku | [https://park.paymove.io/h95h](https://park.paymove.io/h95h) |
| Szczecin | SPP — Moniuszki 6 Castellari | [https://park.paymove.io/kwm1](https://park.paymove.io/kwm1) |
| Szczecin | SPP — Monte Cassino 10 Instrumenty Muzyczne | [https://park.paymove.io/luod](https://park.paymove.io/luod) |
| Szczecin | SPP — Monte Cassino 22 1szy od Piotra Skargi | [https://park.paymove.io/gk5j](https://park.paymove.io/gk5j) |
| Szczecin | SPP — Monte Cassino 23 2gi od Piotra Skargi | [https://park.paymove.io/rqzc](https://park.paymove.io/rqzc) |
| Szczecin | SPP — Monte Cassino 27a Przedszkole Żaczek | [https://park.paymove.io/5nug](https://park.paymove.io/5nug) |
| Szczecin | SPP — Monte Cassino 3-4 Groszek | [https://park.paymove.io/wfo7](https://park.paymove.io/wfo7) |
| Szczecin | SPP — Monte Cassino 30 Turbomyjnia | [https://park.paymove.io/gb1f](https://park.paymove.io/gb1f) |
| Szczecin | SPP — Monte Cassino 32 | [https://park.paymove.io/guor](https://park.paymove.io/guor) |
| Szczecin | SPP — Mściwoja 3 przy Wyszyńskiego | [https://park.paymove.io/02qi](https://park.paymove.io/02qi) |
| Szczecin | SPP — Nabrzeże Wieleckie most Długi | [https://park.paymove.io/wttz](https://park.paymove.io/wttz) |
| Szczecin | SPP — Nabrzeże Wieleckie Trasa Zamkowa | [https://park.paymove.io/lx4h](https://park.paymove.io/lx4h) |
| Szczecin | SPP — naprzeciwko J. K. Chodkiewicza 7A | [https://park.paymove.io/ojk3](https://park.paymove.io/ojk3) |
| Szczecin | SPP — naprzeciwko Kapitańska 5/5A | [https://park.paymove.io/rsgz](https://park.paymove.io/rsgz) |
| Szczecin | SPP — naprzeciwko Parkowa 6 | [https://park.paymove.io/9n6e](https://park.paymove.io/9n6e) |
| Szczecin | SPP — naprzeciwko Sambora 4 | [https://park.paymove.io/plc2](https://park.paymove.io/plc2) |
| Szczecin | SPP — naprzeciwko Sikorskiego 3 | [https://park.paymove.io/6elv](https://park.paymove.io/6elv) |
| Szczecin | SPP — naprzeciwko Storrady-Świętosławy 1 | [https://park.paymove.io/ozhm](https://park.paymove.io/ozhm) |
| Szczecin | SPP — naprzeciwko Unisławy 16 | [https://park.paymove.io/hyyn](https://park.paymove.io/hyyn) |
| Szczecin | SPP — Narutowicza 13E | [https://park.paymove.io/nc9b](https://park.paymove.io/nc9b) |
| Szczecin | SPP — Narutowicza pomiędzy Piastów a B. Głowackiego | [https://park.paymove.io/yjia](https://park.paymove.io/yjia) |
| Szczecin | SPP — Narutowicza/B. Głowackiego | [https://park.paymove.io/ajjx](https://park.paymove.io/ajjx) |
| Szczecin | SPP — Niedziałkowskiego 16 Konsulat Węgier | [https://park.paymove.io/e0tq](https://park.paymove.io/e0tq) |
| Szczecin | SPP — Niedziałkowskiego 22 wjazd na parking | [https://park.paymove.io/m5e4](https://park.paymove.io/m5e4) |
| Szczecin | SPP — Niedziałkowskiego 49 Przedszkole | [https://park.paymove.io/zn3y](https://park.paymove.io/zn3y) |
| Szczecin | SPP — Niedziałkowskiego naprzeciwko wjazdu w A. Niegolewskiego | [https://park.paymove.io/x8uc](https://park.paymove.io/x8uc) |
| Szczecin | SPP — Niedziałkowskiego, TVP | [https://park.paymove.io/uuj7](https://park.paymove.io/uuj7) |
| Szczecin | SPP — Niedziałkowskiego/Unisławy | [https://park.paymove.io/qsui](https://park.paymove.io/qsui) |
| Szczecin | SPP — Niepodległości 13 KFC | [https://park.paymove.io/gv9c](https://park.paymove.io/gv9c) |
| Szczecin | SPP — Niepodległości 2 Dom Chleba | [https://park.paymove.io/o9kn](https://park.paymove.io/o9kn) |
| Szczecin | SPP — Niepodległości 29 | [https://park.paymove.io/xz8r](https://park.paymove.io/xz8r) |
| Szczecin | SPP — Niepodległości MCDonalds | [https://park.paymove.io/ri0g](https://park.paymove.io/ri0g) |
| Szczecin | SPP — Odrowąża | [https://park.paymove.io/ne1n](https://park.paymove.io/ne1n) |
| Szczecin | SPP — Ogińskiego 13 | [https://park.paymove.io/8f4k](https://park.paymove.io/8f4k) |
| Szczecin | SPP — Owocowa 16 kładka | [https://park.paymove.io/h69u](https://park.paymove.io/h69u) |
| Szczecin | SPP — Owocowa 4 od Kaszubskiej/garaże | [https://park.paymove.io/p3sl](https://park.paymove.io/p3sl) |
| Szczecin | SPP — Owocowa rondo Taxi | [https://park.paymove.io/79lw](https://park.paymove.io/79lw) |
| Szczecin | SPP — Owocowa schody PKP | [https://park.paymove.io/o8x1](https://park.paymove.io/o8x1) |
| Szczecin | SPP — P. Skargi 30 | [https://park.paymove.io/ignt](https://park.paymove.io/ignt) |
| Szczecin | SPP — P. Ściegiennego 12 | [https://park.paymove.io/9589](https://park.paymove.io/9589) |
| Szczecin | SPP — P. Ściegiennego 61 | [https://park.paymove.io/ovx4](https://park.paymove.io/ovx4) |
| Szczecin | SPP — P. Ściegiennego 8 | [https://park.paymove.io/ihg0](https://park.paymove.io/ihg0) |
| Szczecin | SPP — Panieńska 11 pierwszy od Baszty | [https://park.paymove.io/ispz](https://park.paymove.io/ispz) |
| Szczecin | SPP — Panieńska 16 2gi od Baszty | [https://park.paymove.io/kpln](https://park.paymove.io/kpln) |
| Szczecin | SPP — Partyzantow 3 Eko Fundusze | [https://park.paymove.io/55dr](https://park.paymove.io/55dr) |
| Szczecin | SPP — Piastow 15 KFC | [https://park.paymove.io/z14r](https://park.paymove.io/z14r) |
| Szczecin | SPP — Piastow 3 Zakłady Bukmacherskie | [https://park.paymove.io/lnd7](https://park.paymove.io/lnd7) |
| Szczecin | SPP — Piastow 65 Komputronik | [https://park.paymove.io/t5je](https://park.paymove.io/t5je) |
| Szczecin | SPP — Piastow 70 Kiosk | [https://park.paymove.io/0owy](https://park.paymove.io/0owy) |
| Szczecin | SPP — Piastow 71 Spondylus | [https://park.paymove.io/w0p1](https://park.paymove.io/w0p1) |
| Szczecin | SPP — Piastów 12 LO | [https://park.paymove.io/sapd](https://park.paymove.io/sapd) |
| Szczecin | SPP — Piastów 17 | [https://park.paymove.io/5bnm](https://park.paymove.io/5bnm) |
| Szczecin | SPP — Piastów 24A | [https://park.paymove.io/cy98](https://park.paymove.io/cy98) |
| Szczecin | SPP — Piastów 38 | [https://park.paymove.io/5msb](https://park.paymove.io/5msb) |
| Szczecin | SPP — Piastów 6/SP nr:1 | [https://park.paymove.io/2txv](https://park.paymove.io/2txv) |
| Szczecin | SPP — Piastów 76 PLUS | [https://park.paymove.io/vrbo](https://park.paymove.io/vrbo) |
| Szczecin | SPP — Piastów 9 za Żółkiewskiego | [https://park.paymove.io/uv5j](https://park.paymove.io/uv5j) |
| Szczecin | SPP — Piastów pomiędzy Plac Kościuszki a K. Pułaskiego | [https://park.paymove.io/qlng](https://park.paymove.io/qlng) |
| Szczecin | SPP — Piastów pomiędzy Szwoleżerów a Bohaterów Warszawy | [https://park.paymove.io/ukt8](https://park.paymove.io/ukt8) |
| Szczecin | SPP — Piotra i Pawła w/w 4/5 | [https://park.paymove.io/hs2l](https://park.paymove.io/hs2l) |
| Szczecin | SPP — Piłsudskiego 15 Rowerowy | [https://park.paymove.io/gi9s](https://park.paymove.io/gi9s) |
| Szczecin | SPP — Piłsudskiego 2 Konsulat | [https://park.paymove.io/akir](https://park.paymove.io/akir) |
| Szczecin | SPP — Piłsudskiego 21 Obiadek | [https://park.paymove.io/d4lh](https://park.paymove.io/d4lh) |
| Szczecin | SPP — Piłsudskiego 24 Kwiaciarki | [https://park.paymove.io/ll8h](https://park.paymove.io/ll8h) |
| Szczecin | SPP — Piłsudskiego 24b | [https://park.paymove.io/aatx](https://park.paymove.io/aatx) |
| Szczecin | SPP — Piłsudskiego 26 Elmet | [https://park.paymove.io/toan](https://park.paymove.io/toan) |
| Szczecin | SPP — Piłsudskiego 29 Aparaty Słuchowe | [https://park.paymove.io/goy8](https://park.paymove.io/goy8) |
| Szczecin | SPP — Piłsudskiego 34 Auto Test | [https://park.paymove.io/vdrc](https://park.paymove.io/vdrc) |
| Szczecin | SPP — Piłsudskiego 7 Kiosk | [https://park.paymove.io/hxdo](https://park.paymove.io/hxdo) |
| Szczecin | SPP — Pl. Batorego 5 ZAiKS | [https://park.paymove.io/z097](https://park.paymove.io/z097) |
| Szczecin | SPP — Pl. Batorego v/v 1 Apteka | [https://park.paymove.io/6rog](https://park.paymove.io/6rog) |
| Szczecin | SPP — Pl. Lotników 2-3 Karczma | [https://park.paymove.io/s472](https://park.paymove.io/s472) |
| Szczecin | SPP — Pl. Lotników 4-6 | [https://park.paymove.io/ffc4](https://park.paymove.io/ffc4) |
| Szczecin | SPP — Pl. Rodła 8  PAZIM | [https://park.paymove.io/4804](https://park.paymove.io/4804) |
| Szczecin | SPP — Pl. Zwycięstwa Basen | [https://park.paymove.io/sbov](https://park.paymove.io/sbov) |
| Szczecin | SPP — Pl. Zwycięstwa Hilton/Cepelia | [https://park.paymove.io/of1j](https://park.paymove.io/of1j) |
| Szczecin | SPP — Pl. Zwycięstwa Medicus | [https://park.paymove.io/7amc](https://park.paymove.io/7amc) |
| Szczecin | SPP — Pl. Żołnierza 16 Bank | [https://park.paymove.io/zpfr](https://park.paymove.io/zpfr) |
| Szczecin | SPP — Pl.Tadeusza Mazowieckiego róg Małopolskiej | [https://park.paymove.io/h9a0](https://park.paymove.io/h9a0) |
| Szczecin | SPP — Pl.Żołnierza 8 (Korsarzy) | [https://park.paymove.io/od85](https://park.paymove.io/od85) |
| Szczecin | SPP — Plac Batorego UM | [https://park.paymove.io/azxb](https://park.paymove.io/azxb) |
| Szczecin | SPP — Plac Teatralny 1 | [https://park.paymove.io/9p4h](https://park.paymove.io/9p4h) |
| Szczecin | SPP — Plac Witosa | [https://park.paymove.io/58qp](https://park.paymove.io/58qp) |
| Szczecin | SPP — Plantowa | [https://park.paymove.io/2pnz](https://park.paymove.io/2pnz) |
| Szczecin | SPP — Pocztowa 23 | [https://park.paymove.io/umke](https://park.paymove.io/umke) |
| Szczecin | SPP — Pocztowa 31 | [https://park.paymove.io/unzt](https://park.paymove.io/unzt) |
| Szczecin | SPP — Pocztowa 37A | [https://park.paymove.io/0a7o](https://park.paymove.io/0a7o) |
| Szczecin | SPP — Pocztowa/5 Lipca | [https://park.paymove.io/ivsh](https://park.paymove.io/ivsh) |
| Szczecin | SPP — Pocztowa/J. K. Chodkiewicza | [https://park.paymove.io/a5qn](https://park.paymove.io/a5qn) |
| Szczecin | SPP — Podgórna / szkoła | [https://park.paymove.io/m7x5](https://park.paymove.io/m7x5) |
| Szczecin | SPP — Podgórna plac zabaw | [https://park.paymove.io/coy8](https://park.paymove.io/coy8) |
| Szczecin | SPP — Podhalańska 8 | [https://park.paymove.io/tvne](https://park.paymove.io/tvne) |
| Szczecin | SPP — Potulicka  Areszt od Czarneckiego | [https://park.paymove.io/awpo](https://park.paymove.io/awpo) |
| Szczecin | SPP — Potulicka 2 rest. Rycerska | [https://park.paymove.io/p4d1](https://park.paymove.io/p4d1) |
| Szczecin | SPP — Potulicka 3a Areszt | [https://park.paymove.io/9c86](https://park.paymove.io/9c86) |
| Szczecin | SPP — Potulicka v/v 57 Pompa | [https://park.paymove.io/1dru](https://park.paymove.io/1dru) |
| Szczecin | SPP — Potulicka v/v Zomownia | [https://park.paymove.io/7hew](https://park.paymove.io/7hew) |
| Szczecin | SPP — Płatny Parking Niestrzeżony Dolny Taras | [https://park.paymove.io/de0c01ac-ea75-42f7-9f14-03a080af9e19](https://park.paymove.io/de0c01ac-ea75-42f7-9f14-03a080af9e19) |
| Szczecin | SPP — Płatny Parking Niestrzeżony Enea Arena | [https://park.paymove.io/fc345bf0-c789-4fbb-8ce9-0e8bb186d333](https://park.paymove.io/fc345bf0-c789-4fbb-8ce9-0e8bb186d333) |
| Szczecin | SPP — Płatny Parking Niestrzeżony Plac Orła Białego | [https://park.paymove.io/ddce02e9-516a-473c-bd5a-dd7ea9e024c4](https://park.paymove.io/ddce02e9-516a-473c-bd5a-dd7ea9e024c4) |
| Szczecin | SPP — Płatny Parking Niestrzeżony pod Trasą Zamkową | [https://park.paymove.io/86061819-bfbb-4ecd-a098-d97c90ac280b](https://park.paymove.io/86061819-bfbb-4ecd-a098-d97c90ac280b) |
| Szczecin | SPP — Płatny Parking Niestrzeżony przy ul. Czarnieckiego | [https://park.paymove.io/fa767317-40aa-4383-9317-3cbfc57f80b3](https://park.paymove.io/fa767317-40aa-4383-9317-3cbfc57f80b3) |
| Szczecin | SPP — Płatny Parking Niestrzeżony przy ul. Kadłubka | [https://park.paymove.io/4e813985-ce29-4759-b003-be09e4ea2540](https://park.paymove.io/4e813985-ce29-4759-b003-be09e4ea2540) |
| Szczecin | SPP — Płatny Parking Niestrzeżony przy ul. Ku Słońcu | [https://park.paymove.io/408d0325-7f84-44d1-9db0-ac14b2170136](https://park.paymove.io/408d0325-7f84-44d1-9db0-ac14b2170136) |
| Szczecin | SPP — Płatny Parking Niestrzeżony przy ul. Ogińskiego | [https://park.paymove.io/bfdbab97-f293-4fff-bfca-d60f72b8be46](https://park.paymove.io/bfdbab97-f293-4fff-bfca-d60f72b8be46) |
| Szczecin | SPP — Płatny Parking Niestrzeżony przy ul. Szymanowskiego | [https://park.paymove.io/f82fe403-68b7-423d-8c79-9041fe92bef4](https://park.paymove.io/f82fe403-68b7-423d-8c79-9041fe92bef4) |
| Szczecin | SPP — Rayskiego 16-17 Małpka | [https://park.paymove.io/uc4n](https://park.paymove.io/uc4n) |
| Szczecin | SPP — Rayskiego 24-25 Warzywniak | [https://park.paymove.io/ipux](https://park.paymove.io/ipux) |
| Szczecin | SPP — Rayskiego 39 | [https://park.paymove.io/yx5s](https://park.paymove.io/yx5s) |
| Szczecin | SPP — Rayskiego 5 Monopolowy | [https://park.paymove.io/j3we](https://park.paymove.io/j3we) |
| Szczecin | SPP — Rayskiego Szkoła | [https://park.paymove.io/d278](https://park.paymove.io/d278) |
| Szczecin | SPP — Rybacka/Podgórna Księżnica | [https://park.paymove.io/m82h](https://park.paymove.io/m82h) |
| Szczecin | SPP — S. Żółkiewskiego 4 | [https://park.paymove.io/lqi0](https://park.paymove.io/lqi0) |
| Szczecin | SPP — S. Żółkiewskiego 7A | [https://park.paymove.io/rb4a](https://park.paymove.io/rb4a) |
| Szczecin | SPP — S. Żółkiewskiego/Bohaterów Warszawy | [https://park.paymove.io/k57r](https://park.paymove.io/k57r) |
| Szczecin | SPP — Sikorskiego 10 | [https://park.paymove.io/mz1v](https://park.paymove.io/mz1v) |
| Szczecin | SPP — Sikorskiego 20A | [https://park.paymove.io/9xx0](https://park.paymove.io/9xx0) |
| Szczecin | SPP — Sikorskiego 3 | [https://park.paymove.io/13fu](https://park.paymove.io/13fu) |
| Szczecin | SPP — Sikorskiego 31 | [https://park.paymove.io/zgy6](https://park.paymove.io/zgy6) |
| Szczecin | SPP — Sikorskiego 37 | [https://park.paymove.io/q75v](https://park.paymove.io/q75v) |
| Szczecin | SPP — Sołtysia | [https://park.paymove.io/12rb](https://park.paymove.io/12rb) |
| Szczecin | SPP — Staromłyńska 21/26 Warta | [https://park.paymove.io/i0nu](https://park.paymove.io/i0nu) |
| Szczecin | SPP — Staromłyńska Muzeum | [https://park.paymove.io/990z](https://park.paymove.io/990z) |
| Szczecin | SPP — Starzyńskiego 3 Komenda | [https://park.paymove.io/j9kk](https://park.paymove.io/j9kk) |
| Szczecin | SPP — Starzyńskiego 8 v/v akademika | [https://park.paymove.io/nnbr](https://park.paymove.io/nnbr) |
| Szczecin | SPP — Starzyńskiego 9 basen | [https://park.paymove.io/7xwg](https://park.paymove.io/7xwg) |
| Szczecin | SPP — Starzyńskiego Hotel Park | [https://park.paymove.io/f75h](https://park.paymove.io/f75h) |
| Szczecin | SPP — Stoisława 27c na rogu | [https://park.paymove.io/pp7j](https://park.paymove.io/pp7j) |
| Szczecin | SPP — Stoisława 6 Potulicka na trawniku | [https://park.paymove.io/sy0u](https://park.paymove.io/sy0u) |
| Szczecin | SPP — Stoisława v/v 2 Hotel Elka-Sen | [https://park.paymove.io/prfl](https://park.paymove.io/prfl) |
| Szczecin | SPP — Storrady-Świętosławy 5/1 | [https://park.paymove.io/ly30](https://park.paymove.io/ly30) |
| Szczecin | SPP — Struga 18 - F451 | [https://park.paymove.io/26ba](https://park.paymove.io/26ba) |
| Szczecin | SPP — Swarożyca 13 | [https://park.paymove.io/f5xp](https://park.paymove.io/f5xp) |
| Szczecin | SPP — Swarożyca 3A | [https://park.paymove.io/hu5h](https://park.paymove.io/hu5h) |
| Szczecin | SPP — Szczecin, Lelewela 9 - F461 | [https://park.paymove.io/235f7db7-71b7-4ae4-83b9-3b88e48916ad](https://park.paymove.io/235f7db7-71b7-4ae4-83b9-3b88e48916ad) |
| Szczecin | SPP — Szczerbcowa 4 kiosk | [https://park.paymove.io/zo7a](https://park.paymove.io/zo7a) |
| Szczecin | SPP — Szczerbcowa/Jarowita | [https://park.paymove.io/e0sb](https://park.paymove.io/e0sb) |
| Szczecin | SPP — Szwoleżerów 18 | [https://park.paymove.io/p68y](https://park.paymove.io/p68y) |
| Szczecin | SPP — Szymanowskiego 5 | [https://park.paymove.io/0b1l](https://park.paymove.io/0b1l) |
| Szczecin | SPP — Szymanowskiego 7 przed Herbow± | [https://park.paymove.io/bcei](https://park.paymove.io/bcei) |
| Szczecin | SPP — Szymanowskiego Fontanna (od Parku) | [https://park.paymove.io/mkjf](https://park.paymove.io/mkjf) |
| Szczecin | SPP — Tkacka 50 Straż | [https://park.paymove.io/tglu](https://park.paymove.io/tglu) |
| Szczecin | SPP — Tkacka 64D/ przejazd róg | [https://park.paymove.io/liqv](https://park.paymove.io/liqv) |
| Szczecin | SPP — Tuwima/Herbowa | [https://park.paymove.io/nurz](https://park.paymove.io/nurz) |
| Szczecin | SPP — Tuwima/Lutniana | [https://park.paymove.io/2lkq](https://park.paymove.io/2lkq) |
| Szczecin | SPP — Unisławy 33 | [https://park.paymove.io/eq2a](https://park.paymove.io/eq2a) |
| Szczecin | SPP — Unisławy/Felczaka | [https://park.paymove.io/v5ju](https://park.paymove.io/v5ju) |
| Szczecin | SPP — Unisławy/Kilińskiego | [https://park.paymove.io/j40n](https://park.paymove.io/j40n) |
| Szczecin | SPP — Unisławy/pl. Witosa | [https://park.paymove.io/xqab](https://park.paymove.io/xqab) |
| Szczecin | SPP — W. Jagiełły 6 | [https://park.paymove.io/8oaw](https://park.paymove.io/8oaw) |
| Szczecin | SPP — Wawelska / Basen | [https://park.paymove.io/p1e6](https://park.paymove.io/p1e6) |
| Szczecin | SPP — Wawelska 1 Michałek | [https://park.paymove.io/eg00](https://park.paymove.io/eg00) |
| Szczecin | SPP — Wawelska boczna ściana UW | [https://park.paymove.io/8icv](https://park.paymove.io/8icv) |
| Szczecin | SPP — Wały Chrobrego 2 Rzeźbiarz | [https://park.paymove.io/2zt6](https://park.paymove.io/2zt6) |
| Szczecin | SPP — Wały Chrobrego 4 Ławki | [https://park.paymove.io/szu1](https://park.paymove.io/szu1) |
| Szczecin | SPP — Wały Chrobrego AM | [https://park.paymove.io/vjcb](https://park.paymove.io/vjcb) |
| Szczecin | SPP — Wały Chrobrego/Jarowita | [https://park.paymove.io/jyw9](https://park.paymove.io/jyw9) |
| Szczecin | SPP — Wielkopolska 14 Szkoła | [https://park.paymove.io/zyd9](https://park.paymove.io/zyd9) |
| Szczecin | SPP — Wielkopolska 18 rest. Willa | [https://park.paymove.io/jvz5](https://park.paymove.io/jvz5) |
| Szczecin | SPP — Wielkopolska 22 | [https://park.paymove.io/pcww](https://park.paymove.io/pcww) |
| Szczecin | SPP — Wielkopolska 27  Trafika | [https://park.paymove.io/w5ma](https://park.paymove.io/w5ma) |
| Szczecin | SPP — Wielkopolska 37 | [https://park.paymove.io/zbh4](https://park.paymove.io/zbh4) |
| Szczecin | SPP — Wielkopolska 41 Pleciuga | [https://park.paymove.io/pcxz](https://park.paymove.io/pcxz) |
| Szczecin | SPP — Wielkopolska 44 | [https://park.paymove.io/1a08](https://park.paymove.io/1a08) |
| Szczecin | SPP — Wielkopolska 55 | [https://park.paymove.io/lela](https://park.paymove.io/lela) |
| Szczecin | SPP — Wilków Morskich 3 | [https://park.paymove.io/hef3](https://park.paymove.io/hef3) |
| Szczecin | SPP — Wilków Morskich/Bohaterów Warszawy | [https://park.paymove.io/6rfk](https://park.paymove.io/6rfk) |
| Szczecin | SPP — Więckowskiego 1 Apteka | [https://park.paymove.io/8kah](https://park.paymove.io/8kah) |
| Szczecin | SPP — Więckowskiego w/w 5 | [https://park.paymove.io/58ii](https://park.paymove.io/58ii) |
| Szczecin | SPP — Wojciecha 12 LOK | [https://park.paymove.io/nv6w](https://park.paymove.io/nv6w) |
| Szczecin | SPP — Wojciecha 16 garaże | [https://park.paymove.io/4vic](https://park.paymove.io/4vic) |
| Szczecin | SPP — Wojciecha 1szy za kościołem | [https://park.paymove.io/0zkw](https://park.paymove.io/0zkw) |
| Szczecin | SPP — Wojciecha 2a od strony Kościóła | [https://park.paymove.io/v7ze](https://park.paymove.io/v7ze) |
| Szczecin | SPP — Wojciecha/Bogurodzicy | [https://park.paymove.io/bmtd](https://park.paymove.io/bmtd) |
| Szczecin | SPP — Wojska Polskiego 17 | [https://park.paymove.io/p8nv](https://park.paymove.io/p8nv) |
| Szczecin | SPP — Wojska Polskiego 20 | [https://park.paymove.io/r2v9](https://park.paymove.io/r2v9) |
| Szczecin | SPP — Wojska Polskiego 36 | [https://park.paymove.io/txfb](https://park.paymove.io/txfb) |
| Szczecin | SPP — Wojska Polskiego 4 | [https://park.paymove.io/9o2f](https://park.paymove.io/9o2f) |
| Szczecin | SPP — Wojska Polskiego 43 | [https://park.paymove.io/yjcd](https://park.paymove.io/yjcd) |
| Szczecin | SPP — Wojska Polskiego 46 | [https://park.paymove.io/5wou](https://park.paymove.io/5wou) |
| Szczecin | SPP — Wojska Polskiego 55 | [https://park.paymove.io/n6rt](https://park.paymove.io/n6rt) |
| Szczecin | SPP — Wojska Polskiego 58 | [https://park.paymove.io/23nv](https://park.paymove.io/23nv) |
| Szczecin | SPP — Wojska Polskiego 66 Mała Scena Rozrywki | [https://park.paymove.io/27ul](https://park.paymove.io/27ul) |
| Szczecin | SPP — Wojska Polskiego 67, NOT | [https://park.paymove.io/hqbp](https://park.paymove.io/hqbp) |
| Szczecin | SPP — Wojska Polskiego 72 ENEA | [https://park.paymove.io/7zyn](https://park.paymove.io/7zyn) |
| Szczecin | SPP — Wojska Polskiego 73 Radio | [https://park.paymove.io/vm86](https://park.paymove.io/vm86) |
| Szczecin | SPP — Wojska Polskiego 78 Dom Rzemiosła | [https://park.paymove.io/628i](https://park.paymove.io/628i) |
| Szczecin | SPP — Wojska Polskiego 83 Buchalter | [https://park.paymove.io/rtc2](https://park.paymove.io/rtc2) |
| Szczecin | SPP — Wojska Polskiego 84 | [https://park.paymove.io/funy](https://park.paymove.io/funy) |
| Szczecin | SPP — Wojska Polskiego 91 PZG | [https://park.paymove.io/0ri7](https://park.paymove.io/0ri7) |
| Szczecin | SPP — Wyszyńskiego 20 1szy od Bramy Portowej | [https://park.paymove.io/onxa](https://park.paymove.io/onxa) |
| Szczecin | SPP — Wyszyńskiego 21/27 | [https://park.paymove.io/tcbp](https://park.paymove.io/tcbp) |
| Szczecin | SPP — Wyszyńskiego 26 | [https://park.paymove.io/y4bd](https://park.paymove.io/y4bd) |
| Szczecin | SPP — Wyszyńskiego 9 Pod Arkadami | [https://park.paymove.io/ugn0](https://park.paymove.io/ugn0) |
| Szczecin | SPP — Wyszyńskiego/Hotel Campanile 3-ci od Bramy Portowej | [https://park.paymove.io/8rq0](https://park.paymove.io/8rq0) |
| Szczecin | SPP — Wyzwolenia 17 Lot | [https://park.paymove.io/5heh](https://park.paymove.io/5heh) |
| Szczecin | SPP — Wyzwolenia 37 Apteka Morska | [https://park.paymove.io/tnm1](https://park.paymove.io/tnm1) |
| Szczecin | SPP — Wyzwolenia 38 | [https://park.paymove.io/l1b4](https://park.paymove.io/l1b4) |
| Szczecin | SPP — Wyzwolenia 4a Optyk/Cepelia | [https://park.paymove.io/qekz](https://park.paymove.io/qekz) |
| Szczecin | SPP — Wyzwolenia 7 Rossman | [https://park.paymove.io/n4ud](https://park.paymove.io/n4ud) |
| Szczecin | SPP — Wyzwolenia v/v PAZIMu | [https://park.paymove.io/xiok](https://park.paymove.io/xiok) |
| Szczecin | SPP — Wąska 5a | [https://park.paymove.io/z236](https://park.paymove.io/z236) |
| Szczecin | SPP — Wąska/Kilińskiego | [https://park.paymove.io/28bg](https://park.paymove.io/28bg) |
| Szczecin | SPP — Wąska/Szymanowskiego | [https://park.paymove.io/m8h4](https://park.paymove.io/m8h4) |
| Szczecin | SPP — Władysława Jagiełły 11 | [https://park.paymove.io/gofd](https://park.paymove.io/gofd) |
| Szczecin | SPP — Zawiszy Czarnego 1 Vega | [https://park.paymove.io/zk7a](https://park.paymove.io/zk7a) |
| Szczecin | SPP — Zawiszy Czarnego 5 EKOTRADE | [https://park.paymove.io/g4nx](https://park.paymove.io/g4nx) |
| Szczecin | SPP — Zygmunta Starego 1a Cerkiew | [https://park.paymove.io/e9ok](https://park.paymove.io/e9ok) |
| Szczecin | SPP — Zygmunta Starego 2 | [https://park.paymove.io/5t42](https://park.paymove.io/5t42) |
| Szczecin | SPP — Zygmunta Starego 5 | [https://park.paymove.io/w28g](https://park.paymove.io/w28g) |
| Szczecin | SPP — Zygmunta Starego Muzeum | [https://park.paymove.io/bsb5](https://park.paymove.io/bsb5) |
| Szczecin | SPP — Łokietka 10/11 | [https://park.paymove.io/lthl](https://park.paymove.io/lthl) |
| Szczecin | SPP — Łokietka 16 Przedszkole | [https://park.paymove.io/lkog](https://park.paymove.io/lkog) |
| Szczecin | SPP — Łokietka 3/4 1szy od Kopernika | [https://park.paymove.io/80mg](https://park.paymove.io/80mg) |
| Szczecin | SPP — Ściegiennego 66 RoĽdzielnia | [https://park.paymove.io/kh69](https://park.paymove.io/kh69) |
| Szczecin | SPP — Ściegiennego 7 przy Piastów | [https://park.paymove.io/8z74](https://park.paymove.io/8z74) |
| Szczecin | SPP — Śląska 23 | [https://park.paymove.io/r0a8](https://park.paymove.io/r0a8) |
| Szczecin | SPP — Śląska 33 v/v Taxi | [https://park.paymove.io/oq6z](https://park.paymove.io/oq6z) |
| Szczecin | SPP — Śląska 40 Żabka | [https://park.paymove.io/s3hf](https://park.paymove.io/s3hf) |
| Szczecin | SPP — Śląska 5 Dom Nauczyciela | [https://park.paymove.io/zwlh](https://park.paymove.io/zwlh) |
| Szczecin | SPP — Śląska 51 Golibroda | [https://park.paymove.io/37fu](https://park.paymove.io/37fu) |
| Szczecin | SPP — Śniadeckich 1 | [https://park.paymove.io/4vq0](https://park.paymove.io/4vq0) |
| Szczecin | SPP — Św. Ducha / Warta | [https://park.paymove.io/t26j](https://park.paymove.io/t26j) |
| Szczecin | SPP — Św. Ducha 2a stomatolog | [https://park.paymove.io/8zaz](https://park.paymove.io/8zaz) |
| Szczecin | SPP — Św. Ducha poczta | [https://park.paymove.io/97po](https://park.paymove.io/97po) |

</details>

<br />

---

<br />

## Available MCP Tools (20)

Full parameter schemas are in [`docs/tools.md`](./docs/tools.md). All monetary amounts are integers in **grosze** (`1000` = `10.00 PLN`).

| Domain | Tool | Auth | Description |
| :--- | :--- | :--- | :--- |
| **Discovery** | `search-public-products` | Public | Search available tickets, parking zones, and services by query, city, or type (`GO`, `PARKING`, `PAY`) |
| **Discovery** | `list-partner-products` | `X-API-KEY` | List products belonging to the authenticated merchant account |
| **Pay&Go** | `go-get-product` | Public | Get ticket options, prices, and direct checkout URL for a `GO` product |
| **Pay&Go** | `go-create-product` | `X-API-KEY` | Create a new `GO` ticket or digital storefront (`go.paymove.io/{id}`) |
| **Pay&Go** | `go-add-ticket-option` | `X-API-KEY` | Add a ticket option to an existing `GO` product |
| **Pay&Go** | `go-update-ticket-option` | `X-API-KEY` | Update an existing ticket option on a `GO` product |
| **Pay&Go** | `go-delete-ticket-option` | `X-API-KEY` | Delete a ticket option from a `GO` product |
| **Pay&Go** | `go-update-product` | `X-API-KEY` | Update display settings or replace ticket options on a `GO` product |
| **Pay&Go** | `go-set-translations` | `X-API-KEY` | Set localized translations (`pl-PL`, `en-US`, `de-DE`, `uk-UA`) |
| **Pay&Go** | `go-generate-image` | `X-API-KEY` | Generate an AI illustration for a `GO` product |
| **Parking** | `parking-get-pricing` | Public | Get active hourly rates, free time, and daily caps for a parking zone |
| **Parking** | `parking-create-product` | `X-API-KEY` | Create a paid parking zone (`park.paymove.io/{id}`) |
| **Parking** | `parking-create-event` | `X-API-KEY` | Schedule a special event tariff or temporary parking zone pause |
| **Pay** | `list-pay-pricing-entries` | Public | List pricing options configured on a `PAY` payment link |
| **Pay** | `create-pay-product` | `X-API-KEY` | Create a shareable payment link (`pay.paymove.io/{id}`) |
| **Pay** | `create-subproduct` | `X-API-KEY` | Create an order-tracked e-commerce checkout and return `redirectUrl` |
| **Pay** | `update-subproduct` | `X-API-KEY` | Update the price of an existing checkout subproduct |
| **Pay** | `add-pay-pricing-entry` | `X-API-KEY` | Add a pricing tier to a `PAY` product |
| **Pay** | `update-pay-pricing-entry` | `X-API-KEY` | Update a pricing tier on a `PAY` product |
| **Pay** | `delete-pay-pricing-entry` | `X-API-KEY` | Remove a pricing tier from a `PAY` product |

<br />

---

<br />

## Key Facts

- **Pricing:** `0 PLN` activation, `0 PLN` monthly fee, **1.29%** base online checkout fee, **1 PLN** per Scan&Pay transaction.
- **Payouts:** Next business day (**T+1**).
- **Payment methods:** **BLIK**, **Apple Pay**, **Google Pay**, **Visa / Mastercard**, **Pay-by-Link**, and **PayPo** (PLN, plus EUR & CZK for cards).
- **Regulation:** Licensed by the Polish Financial Supervision Authority (**KNF — MIP 245/2024**).
- **Links:** [paymove.io](https://paymove.io) · [panel.paymove.io](https://panel.paymove.io) · [docs.paymove.io](https://docs.paymove.io)
