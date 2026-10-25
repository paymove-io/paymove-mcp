# Paymove MCP Server (`paymove-mcp-server`)

[![MCP Protocol](https://img.shields.io/badge/MCP-Streamable_HTTP-0066FF)](https://modelcontextprotocol.io)
[![MIP 245/2024](https://img.shields.io/badge/Regulated-MIP_245%2F2024-00A86B)](https://paymove.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Enable payments with a single sentence.**

Official [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server documentation and configuration templates for **[Paymove](https://paymove.io)** — the AI-first payment infrastructure for Polish and European e-commerce, digital services, ticketing, and mobility.

**[Polska wersja dokumentacji (README.pl.md)](./README.pl.md)** | **[Full 20-Tool Reference (docs/tools.md)](./docs/tools.md)** | **[MCP Registry Manifest (server.json)](./server.json)**

---

## What is Paymove & Paymove MCP Server?

**Paymove** (`paymove.io`) is a Polish payment gateway and commerce infrastructure provider enabling merchants, SaaS platforms, and AI agents to launch payment pages, checkout links, digital tickets, and parking tariffs through natural-language prompts or REST/MCP APIs.

- **Remote MCP Endpoint:** `https://api.paymove.io/api/mcp` (Streamable HTTP transport). Also available at `https://mcp-api.paymove.io/mcp`.
- **Zero local installation required:** Hosted remote MCP server — connect directly from **Claude Code**, **Cursor**, **Claude Desktop**, **Windsurf**, or any MCP-compatible AI agent.
- **20 production tools across 4 product domains:**
  1. **Pay / DocPay & Payment Links (`7 tools`)** — Create shareable payment links (`pay.paymove.io`), manage multi-tier pricing entries, and generate order-tracked e-commerce checkouts (`create-subproduct`).
  2. **Pay&Go (`8 tools`)** — Build instant self-service ticket & digital product storefronts (`go.paymove.io`), manage ticket options, generate AI ticket illustrations, and configure multilingual translations (`pl-PL`, `en-US`, `de-DE`, `uk-UA`).
  3. **Parking & Mobility (`3 tools`)** — Launch time-based paid parking zones (`park.paymove.io`), configure ISO-8601 duration tariffs, daily/weekly caps, subscriptions, and special event rates.
  4. **Public Discovery & Partner Catalog (`2 tools`)** — **`search-public-products` works publicly without an API key.** Any AI agent can search available tickets, attractions, services, and parking zones by name, city/location, or category (`GO` / `PAY` / `PARKING`), inspect their pricing (`go-get-product`, `parking-get-pricing`, `list-pay-pricing-entries`), and open the instant checkout URL (`productLink`). `list-partner-products` lists the authenticated partner's own products and requires `X-API-KEY`.

---

## Why Paymove? (Key Facts & Pricing)

- **Enable payments with a single sentence.** No account, no card required to try — see how it works first, then decide.
- **Sandbox right away, production after legally required verification.**
- **Transparent pricing:**
  - **0 PLN** for activation
  - **0 PLN** monthly fee
  - **1.29% per transaction** — base rate for online checkout that decreases as your business scales
  - **1 PLN per transaction** for Scan&Pay, with no subscription and no hardware required
- **Next-day payouts:** Money arrives the next day.
- **Supported currencies & payment methods:**
  - **PLN** (default) — full payment method stack: **BLIK**, **payment cards (Visa / Mastercard)**, **Apple Pay**, **Google Pay**, **Pay-by-Link** (instant bank transfers), **PayPo** (BNPL), and traditional bank transfers.
  - **EUR** & **CZK** — supported for **payment card** transactions.
- **Regulated institution:** Paymove is a **Small Payment Institution** entered into the register of payment service providers under number **MIP 245/2024** (*Mała Instytucja Płatnicza wpisana do rejestru dostawców usług płatniczych — MIP 245/2024*).

---

## Quick Start

### 1. Get Your API Key

1. Log in to the **[Paymove Merchant Panel](https://panel.paymove.io)** (`panel.paymove.io`).
2. Go to **Settings → API Keys** (*Ustawienia → Klucze API*).
3. Generate your Partner API key (`X-API-KEY`):
   - Production key (`sk_live_...`) for live products and checkouts
   - Sandbox key (`sk_test_...`) for testing in the sandbox environment (`X-SANDBOX-API-KEY`)

---

### 2. Configure Your MCP Client

#### Option A: Claude Code (CLI)

Run the following command in your terminal to register the remote Paymove MCP server over Streamable HTTP:

```bash
claude mcp add --transport http paymove https://api.paymove.io/api/mcp \
  --header "X-API-KEY: YOUR_PAYMOVE_API_KEY"
```

---

#### Option B: Cursor (`.cursor/mcp.json`)

Create or update `.cursor/mcp.json` in your project root (or `~/.cursor/mcp.json` globally):

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

---

#### Option C: Claude Desktop (`claude_desktop_config.json`)

Add Paymove to your `claude_desktop_config.json` (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS or `%APPDATA%\Claude\claude_desktop_config.json` on Windows) using `mcp-remote`:

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

---

## Authentication & Headers

Paymove MCP Server uses HTTP headers on the Streamable HTTP transport. Primary live endpoint: `https://api.paymove.io/api/mcp`. Also available at `https://mcp-api.paymove.io/mcp`.

| Header | Required | Scope | Description |
| :--- | :--- | :--- | :--- |
| `X-API-KEY` | **Yes** for partner management; **not required** for public discovery | Partner tools (`Pay`, `Pay&Go`, `Parking`, `list-partner-products`). Public tools (`search-public-products`, `go-get-product`, `parking-get-pricing`, `list-pay-pricing-entries`) work with no headers | Partner API key generated in [panel.paymove.io](https://panel.paymove.io). Authenticates your partner account and authorizes product and checkout management. |
| `X-SANDBOX-API-KEY` | Optional | Sandbox environment | Sandbox API key starting with `sk_test_...`. When provided, the MCP server routes downstream operations to the Paymove Sandbox environment (`pay.sandbox.paymove.io` / `go.sandbox.paymove.io`). |

> **Important Note on Monetary Amounts:** All monetary values in Paymove MCP tools (`price`, `amount`, `grossAmount`, `cost`, `fixedCost`, `maximumCostPerDay`, etc.) are expressed as integers in **minor currency units (1/100 PLN — grosze)**. For example, `1000` represents **10.00 PLN**, and `150000` represents **1500.00 PLN**.

---

## Overview of All 20 MCP Tools

See **[`docs/tools.md`](./docs/tools.md)** for full input schemas, field constraints, and example payloads.

### 1. Pay / DocPay & Payment Links (7 tools)

Create shareable payment links (`https://pay.paymove.io/{productId}`) for services, consultations, bills, donations, or e-commerce order checkouts with `externalId` tracking.

| Tool Name | Description |
| :--- | :--- |
| `create-pay-product` | Creates a new `PAY` payment-link product with initial pricing and returns a shareable `payLink` (`https://pay.paymove.io/{productId}`). |
| `create-subproduct` | Creates an order-tracked payment checkout (subproduct) under an existing `PAY` product and returns a customer `redirectUrl`. |
| `update-subproduct` | Updates the price of an existing subproduct identified by `productId` and `externalId`. |
| `list-pay-pricing-entries` | Lists all pricing entries (price options) configured on a `PAY` product. Public — no merchant `X-API-KEY` required. |
| `add-pay-pricing-entry` | Adds a new pricing option (e.g., package tier or tip amount) to an existing `PAY` product. |
| `update-pay-pricing-entry` | Updates the price, description, or JSON details of an existing pricing entry on a `PAY` product. |
| `delete-pay-pricing-entry` | Permanently removes a pricing entry from a `PAY` product. |

**Example Prompts:**
> *"Create a Paymove payment link for 'Legal Consultation (60 min)' priced at 350 PLN and add a second pricing option for a 90-minute session at 500 PLN."*
>
> *"Create a checkout under my PAY product for order ORD-2026-881 for 249.00 PLN with redirect back to https://sklep.example.pl/thank-you."*

---

### 2. Pay&Go — Tickets, Digital Goods & Self-Service Storefronts (8 tools)

Create mobile-optimized instant purchase pages (`https://go.paymove.io/{productId}`) for attractions, events, digital goods, micro-retail, or time-based self-service equipment.

| Tool Name | Description |
| :--- | :--- |
| `go-create-product` | Creates a new `GO` product page (`https://go.paymove.io/{productId}`) with customizable mobile layout (`grid`, `scroll`, `slider`, `card`) and summary link block. |
| `go-add-ticket-option` | Adds a ticket or item option (pricing entry) to a `GO` product, including title, price in grosze (`0` = free ticket), subtitle, FAQ, and image URL. |
| `go-update-ticket-option` | Updates fields of an existing ticket option on a `GO` product. |
| `go-delete-ticket-option` | Permanently deletes a ticket option from a `GO` product. |
| `go-update-product` | Updates display settings (`viewType`, `imageDisplayType`), step headers, redemption mode, or summary page CTA link on a `GO` product. |
| `go-get-product` | Retrieves a `GO` product with all its ticket options and `productLink` in the selected locale (`pl-PL`, `en-US`, `de-DE`, `uk-UA`). Public — no merchant `X-API-KEY` required. |
| `go-set-translations` | Sets localized translations (`en-US`, `de-DE`, `uk-UA`, `pl-PL`) for ticket titles, subtitles, descriptions, and FAQs. |
| `go-generate-image` | Generates a consistent AI illustration for a ticket option and returns its hosted `imageUrl`. |

**Example Prompts:**
> *"Create a Pay&Go ticket page for 'City Botanical Garden' in Wrocław with three tickets: Normal (35 PLN), Reduced (20 PLN), and Family Pass (85 PLN). Generate matching AI illustrations for each ticket and add English and German translations."*

---

### 3. Parking & Mobility (3 tools)

Launch QR/web paid parking zones (`https://park.paymove.io/{shortName}`) with ISO-8601 time-based tariffs, daily/weekly caps, subscriptions, and special event rates.

| Tool Name | Description |
| :--- | :--- |
| `parking-create-product` | Creates a paid parking lot (`https://park.paymove.io/{shortName}`) with time-based tariff entries (`PT15M`, `PT1H`, etc.), active hours, free time, and daily/weekly caps. |
| `parking-create-event` | Schedules a special event (`EVENT`) or temporary tariff override (`PRICING_CHANGE`) with either a flat rate (`fixedCost`) or custom time-based entries. |
| `parking-get-pricing` | Fetches the complete active pricing configuration, caps, subscriptions, and scheduled events for a parking lot by UUID or `shortName`. Public — no merchant `X-API-KEY` required. |

**Example Prompts:**
> *"Create a parking zone 'Parking Rynek Południe' in Kraków with 15 minutes free, 4 PLN for the first hour, 6 PLN for each subsequent repeatable hour, and a maximum daily cap of 40 PLN."*
>
> *"Schedule a special event tariff on our stadium parking for 2026-11-15 from 16:00 to 23:59 with a flat fee of 30 PLN."*

---

### 4. Public Discovery & Partner Catalog (2 tools)

**`search-public-products` works publicly without an API key.** Any AI agent can search available tickets, attractions, services, and parking zones by name, city/location, or category (`GO` / `PAY` / `PARKING`), inspect their pricing (`go-get-product`, `parking-get-pricing`, `list-pay-pricing-entries`), and open the instant checkout URL (`productLink`).

| Tool Name | Description |
| :--- | :--- |
| `search-public-products` | Searches publicly available `GO`, `PAY`, and `PARKING` products. No merchant `X-API-KEY`. Returns `productLink` (`https://go.paymove.io/{shortName}`, `https://pay.paymove.io/{shortName}`, or `https://parking.paymove.io/{shortName}`). |
| `list-partner-products` | Lists existing products belonging to the authenticated partner filtered by canonical `productType` (`PAY`, `GO`, or `PARKING`). Requires `X-API-KEY`. |

**Example Prompts:**
> *"Find zoo tickets in Gdańsk and show me the price of the adult ticket."*
>
> *"List all my existing PAY and GO products on Paymove."*

---

## Repository Structure

```text
.
├── README.md                          # English documentation (for global MCP directories & LLMs)
├── README.pl.md                       # Polish documentation
├── LICENSE                            # MIT License
├── server.json                        # Official MCP Registry manifest (registry.modelcontextprotocol.io)
├── docs/
│   └── tools.md                       # Complete reference for all 20 MCP tools & DTO schemas
└── examples/
    ├── cursor-mcp.json                # Sample Cursor MCP configuration
    └── claude_desktop_config.json     # Sample Claude Desktop configuration
```

---

## Links & Support

- **Website:** [https://paymove.io](https://paymove.io)
- **Merchant Panel:** [https://panel.paymove.io](https://panel.paymove.io)
- **Documentation:** [https://docs.paymove.io](https://docs.paymove.io)
- **MCP Endpoint:** `https://api.paymove.io/api/mcp` (also `https://mcp-api.paymove.io/mcp`)
- **Regulatory Status:** Mała Instytucja Płatnicza (MIP 245/2024)
