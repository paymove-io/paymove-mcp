# Paymove MCP Server — Complete Reference of All 20 Tools

This document provides the complete technical reference for all **20 tools** across **4 categories** exposed by the production **Paymove MCP Server** (`paymove-mcp-server`, Streamable HTTP). Primary live endpoint: `https://api.paymove.io/api/mcp`. The same server is also available at `https://mcp-api.paymove.io/mcp`.

The live server exposes these **20 tools**. The [Planned tools](#planned-tools) section below is a separate contract draft (**Planned / Planowane**). Those tools are not implemented, they are not included in the count of 20, and they do not appear in `tools/list`.

---

## Table of Contents

1. [Conventions & Authentication Scope](#conventions--authentication-scope)
2. [Category 1: Pay / DocPay & Payment Links (`7 tools`)](#category-1-pay--docpay--payment-links-7-tools)
   - [`create-pay-product`](#2-create-pay-product)
   - [`create-subproduct`](#3-create-subproduct)
   - [`update-subproduct`](#4-update-subproduct)
   - [`list-pay-pricing-entries`](#5-list-pay-pricing-entries)
   - [`add-pay-pricing-entry`](#6-add-pay-pricing-entry)
   - [`update-pay-pricing-entry`](#7-update-pay-pricing-entry)
   - [`delete-pay-pricing-entry`](#8-delete-pay-pricing-entry)
3. [Category 2: Pay&Go — Tickets, Digital Goods & Self-Service (`8 tools`)](#category-2-paygo--tickets-digital-goods--self-service-8-tools)
   - [`go-create-product`](#9-go-create-product)
   - [`go-add-ticket-option`](#10-go-add-ticket-option)
   - [`go-update-ticket-option`](#11-go-update-ticket-option)
   - [`go-delete-ticket-option`](#12-go-delete-ticket-option)
   - [`go-update-product`](#13-go-update-product)
   - [`go-get-product`](#14-go-get-product)
   - [`go-set-translations`](#15-go-set-translations)
   - [`go-generate-image`](#16-go-generate-image)
4. [Category 3: Parking & Mobility (`3 tools`)](#category-3-parking--mobility-3-tools)
   - [`parking-create-product`](#17-parking-create-product)
   - [`parking-create-event`](#18-parking-create-event)
   - [`parking-get-pricing`](#19-parking-get-pricing)
5. [Category 4: Public Discovery & Partner Catalog (`2 tools`)](#category-4-public-discovery--partner-catalog-2-tools)
   - [`search-public-products`](#20-search-public-products)
   - [`list-partner-products`](#1-list-partner-products)
6. [Planned tools (Planned / Planowane — not in `tools/list`)](#planned-tools)
   - [`set-availability`](#p1-set-availability)
   - [`list-availability`](#p2-list-availability)
   - [`create-reservation`](#p3-create-reservation)
   - [`get-reservation`](#p4-get-reservation)
   - [`cancel-reservation`](#p5-cancel-reservation)
   - [`register-webhook`](#p6-register-webhook)
   - [`assign-webhook-to-product`](#p7-assign-webhook-to-product)
   - [`list-product-webhooks`](#p8-list-product-webhooks)
   - [`parking-update-pricing`](#p9-parking-update-pricing)
   - [`set-product-visibility`](#p10-set-product-visibility)
   - [`get-product-status`](#p11-get-product-status)

---

## Conventions & Authentication Scope

- **Monetary Amounts (`1/100 PLN — grosze`):** Every monetary field (`price`, `amount`, `cost`, `fixedCost`, `maximumCostPerDay`, `maximumCostPerWeek`, `minimumCostPerDay`) is an integer in **minor units (grosze)**. Send `Math.round(pln * 100)`. Never send a float.
  - `1000` = **10.00 PLN**
  - `3500` = **35.00 PLN**
  - `150000` = **1500.00 PLN**
- **Authentication:**
  - **Public:** `search-public-products` requires no API key. It returns a direct purchase link (`productLink`): `https://go.paymove.io/{shortName}`, `https://pay.paymove.io/{shortName}`, or `https://park.paymove.io/{shortName}`. When `shortName` is empty, the link uses `{productId}`. With `X-SANDBOX-API-KEY` the hosts are `go.sandbox.paymove.io`, `pay.sandbox.paymove.io`, and `park.sandbox.paymove.io`. The same tool is available when a partner key is sent.
  - **Partner:** The other 19 tools require the header `X-API-KEY: <YOUR_PAYMOVE_API_KEY>`. That includes `list-partner-products`, `go-get-product`, `parking-get-pricing`, and `list-pay-pricing-entries`. Optional `X-SANDBOX-API-KEY` (`sk_test_...`) routes those calls to the Paymove Sandbox.
  - **Public price lists (REST):** `GET https://api.paymove.io/api/go/product/{id}/pricing`, `GET https://api.paymove.io/api/parking/product/{id}/pricing`, and `GET https://api.paymove.io/api/product/{id}/public` can be called without an API key.
- **Arguments:** Most tools take a top-level `request` object. `search-public-products`, `list-partner-products`, `go-get-product`, and `parking-get-pricing` take their fields directly in `arguments`.

---

## Category 1: Pay / DocPay & Payment Links (`7 tools`)

### 2. `create-pay-product`

Creates a new payment-link product (`PAY`) with initial pricing and returns a shareable payment link (`https://pay.paymove.io/{productId}`, or `https://pay.sandbox.paymove.io/{productId}` in sandbox). Suitable for services, professional fees, bills, tips, donations, and logistics settlements.

- **Auth Scope:** Partner (`X-API-KEY`)

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `name` | `string` | **Yes** | Non-empty string | Product name (e.g., `'Premium Subscription'`, `'Consulting Session'`). |
| `price` | `integer` | **Yes** | Non-negative integer (grosze) | Price in minor units (1/100 PLN), e.g., `1000` = 10.00 PLN. When `price > 0`, automatically creates the initial pricing entry; when `0`, creates only the parent `PAY` container (used when pricing lives on subproducts via `create-subproduct`). |
| `description` | `string` | No | Defaults to `name` | Payment description shown to the customer. |
| `location` | `string` | No | Default: `'Online'` | Location label for the product. |
| `customDetails` | `object` | No | Specific item keys only | JSON object where keys are specific item names and values are formatted prices, e.g., `{"Bike": "10 PLN"}`. Do not use generic keys like `'product'` or `'price'`. |

#### Response JSON

```json
{
  "productId": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Consulting Session",
  "price": 35000,
  "entryId": "7d9e8f10-1234-4abc-9def-0123456789ab",
  "payLink": "https://pay.paymove.io/550e8400-e29b-41d4-a716-446655440000"
}
```

---

### 3. `create-subproduct`

Creates a payment checkout (subproduct) under an existing `PAY` product and returns a customer `redirectUrl`. Use this tool when the integration requires order tracking (`externalId`) and customer redirect after payment. Always call `list-partner-products` with `productType='PAY'` first if you need to discover an existing parent `productId`.

- **Auth Scope:** Partner (`X-API-KEY`)

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `productId` | `string` | **Yes** | UUID | Parent `PAY` Product ID from `list-partner-products` or `create-pay-product`. |
| `externalId` | `string` | **Yes** | Non-empty string | Unique external identifier for this subproduct/order (e.g., `'ORD-123'`). |
| `amount` | `integer` | **Yes** | Positive integer (grosze) | Payment amount in minor units (1/100 PLN), e.g., `1000` = 10.00 PLN, `150000` = 1500.00 PLN. |
| `description` | `string` | **Yes** | Non-empty string | Payment description shown to the customer. |
| `returnUrl` | `string` | **Yes** | Non-empty string | URL to redirect the customer after payment completion. |
| `bankAccount` | `string` | No | Optional | Bank account IBAN for settlement. |
| `email` | `string` | No | Optional | Customer email address. |
| `locale` | `string` | No | Default: `'pl-PL'` | Customer interface locale. |
| `customDetails` | `object` | No | Specific item keys only | JSON object where keys are item names and values are prices, e.g., `{"Bike": "10 PLN"}`. |

#### Response JSON

```json
{
  "redirectUrl": "https://checkout.paymove.io/550e8400-e29b-41d4-a716-446655440000?externalId=ec6RtwTZKb",
  "externalId": "ORD-123",
  "amount": 24900
}
```

`redirectUrl` has the form `https://checkout.paymove.io/{productId}?externalId={10charHash}` (sandbox: `https://checkout.sandbox.paymove.io/{productId}?externalId={10charHash}`). The query value is a 10-character hash generated by Paymove. The `externalId` field in this response is the identifier you sent.

---

### 4. `update-subproduct`

Updates the price of an existing subproduct (checkout) under a `PAY` product, identified by `productId` and `externalId`.

- **Auth Scope:** Partner (`X-API-KEY`)

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `productId` | `string` | **Yes** | UUID | Parent `PAY` product ID. |
| `externalId` | `string` | **Yes** | Non-empty string | The `externalId` assigned when the subproduct was created. |
| `price` | `integer` | **Yes** | Non-negative integer (grosze) | New price in minor units (1/100 PLN), e.g., `150000` = 1500.00 PLN. |

#### Response JSON

```json
{
  "productId": "550e8400-e29b-41d4-a716-446655440000",
  "externalId": "ORD-123",
  "entryId": "8a1b2c3d-4e5f-6789-abcd-ef0123456789",
  "price": 150000
}
```

---

### 5. `list-pay-pricing-entries`

Lists all pricing entries (price options) for an existing `PAY` product. Requires `X-API-KEY: <YOUR_PAYMOVE_API_KEY>`.

- **Auth Scope:** Partner (`X-API-KEY`)

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `productId` | `string` | **Yes** | UUID | Product ID from `create-pay-product`. |

#### Response JSON

```json
{
  "productId": "550e8400-e29b-41d4-a716-446655440000",
  "entries": [
    {
      "entryId": "7d9e8f10-1234-4abc-9def-0123456789ab",
      "price": 35000,
      "description": "Legal Consultation (60 min)",
      "details": {}
    }
  ]
}
```

---

### 6. `add-pay-pricing-entry`

Adds an additional pricing entry (price option, package tier, or suggested tip amount) to an existing `PAY` product.

- **Auth Scope:** Partner (`X-API-KEY`)

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `productId` | `string` | **Yes** | UUID | Product ID from `create-pay-product`. |
| `price` | `integer` | **Yes** | Non-negative integer (grosze) | Price in minor units (1/100 PLN), e.g., `1000` = 10.00 PLN. |
| `description` | `string` | No | Optional | Payment description shown to the customer. |
| `detailsJson` | `string` | No | JSON object string | Additional details as a JSON object string, e.g., `'{"Session":"90 min"}'`. |

#### Response JSON

```json
{
  "productId": "550e8400-e29b-41d4-a716-446655440000",
  "entryId": "9f8e7d6c-5b4a-3210-fedc-ba9876543210",
  "price": 50000
}
```

---

### 7. `update-pay-pricing-entry`

Updates an existing pricing entry of a `PAY` product. Omitted or null fields keep their current value; `detailsJson` overwrites the existing `details` map when provided.

- **Auth Scope:** Partner (`X-API-KEY`)

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `productId` | `string` | **Yes** | UUID | Product ID from `create-pay-product`. |
| `entryId` | `string` | **Yes** | UUID | Pricing entry ID from `list-pay-pricing-entries` or `add-pay-pricing-entry`. |
| `price` | `integer` | No | Non-negative integer (grosze) | New price in minor units (1/100 PLN), e.g., `1000` = 10.00 PLN. |
| `description` | `string` | No | Optional | New payment description shown to the customer. |
| `detailsJson` | `string` | No | JSON object string | New details as a JSON object string (`'{"key":"value"}'`). |

#### Response JSON

```json
{
  "productId": "550e8400-e29b-41d4-a716-446655440000",
  "entryId": "9f8e7d6c-5b4a-3210-fedc-ba9876543210",
  "price": 45000,
  "description": "Legal Consultation (90 min)"
}
```

---

### 8. `delete-pay-pricing-entry`

Permanently deletes a pricing entry from a `PAY` product.

- **Auth Scope:** Partner (`X-API-KEY`)

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `productId` | `string` | **Yes** | UUID | Product ID from `create-pay-product`. |
| `entryId` | `string` | **Yes** | UUID | Pricing entry ID to delete. |

#### Response JSON

```json
{
  "productId": "550e8400-e29b-41d4-a716-446655440000",
  "entryId": "9f8e7d6c-5b4a-3210-fedc-ba9876543210",
  "status": "deleted"
}
```

---

## Category 2: Pay&Go — Tickets, Digital Goods & Self-Service (`8 tools`)

### 9. `go-create-product`

Creates a new `GO` product page (`https://go.paymove.io/{productId}`) for instant fulfillment ("Pay and Get" — tickets, events, digital goods, micro-retail) or time-based self-service equipment ("Pay per minute" — car washes, laundries, space/equipment rental). Automatically resolves a unique URL slug (`shortName`) if the preferred one is omitted or already taken. After creating the product, call `go-add-ticket-option` for each ticket or item.

- **Auth Scope:** Partner (`X-API-KEY`)

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `name` | `string` | **Yes** | Non-empty string | Product display name (e.g., `'Zoo Wroclaw'`, `'Muzeum Narodowe'`). |
| `fullName` | `string` | **Yes** | Non-empty string | Full official name of the product. |
| `location` | `string` | **Yes** | Non-empty string | Location/city of the product (e.g., `'Wroclaw'`, `'Krakow'`). |
| `shortName` | `string` | No | Auto-derived from `fullName` | Preferred URL slug (letters, numbers, hyphens only). |
| `viewType` | `string` | No | Default: `'grid'` | Mobile layout: `'grid'` (2-column grid), `'scroll'` (vertical list), `'slider'` (horizontal carousel), or `'card'` (single card view). |
| `imageDisplayType` | `string` | No | Default: `'medium'` | Image display size: `'full'` (large images) or `'medium'`. |
| `notAvailableToRedeem` | `boolean` | No | Default: `false` | If `true`, items are display-only after purchase and cannot be scanned/redeemed (useful for digital goods or donations). |
| `summaryLinkTitle` | `string` | No | Optional | Title of the CTA link block shown on the payment summary page. |
| `summaryLinkDescription` | `string` | No | Optional | Description text of the link block on the payment summary page. |
| `summaryLinkButtonText` | `string` | No | Optional | Button label of the link block on the payment summary page. |
| `summaryLinkUrl` | `string` | No | Optional | Target URL the summary link block button points to (e.g., downloadable digital content). |
| `summaryLinkEnabled` | `boolean` | No | Default: `false` | If `true`, displays the summary link block on the post-payment summary page. |

#### Response JSON

```json
{
  "productId": "a1b2c3d4-e5f6-4789-abcd-112233445566",
  "name": "Ogród Botaniczny Wrocław",
  "shortName": "ogrod-botaniczny-wroclaw",
  "productLink": "https://go.paymove.io/a1b2c3d4-e5f6-4789-abcd-112233445566",
  "next_step": "Now call go-add-ticket-option for EACH ticket the user mentioned."
}
```

---

### 10. `go-add-ticket-option`

Adds a ticket or item option (pricing entry) to a `GO` product. This operation is idempotent with respect to `(productId, title, price)` — if an identical option already exists, it returns the existing `entryId`.

- **Auth Scope:** Partner (`X-API-KEY`)

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `productId` | `string` | **Yes** | UUID | Product ID returned by `go-create-product`. |
| `title` | `string` | **Yes** | Non-empty string | Ticket title shown to the customer (e.g., `'Bilet normalny'`, `'Adult Ticket'`, `'VIP Pass'`). |
| `price` | `integer` | **Yes** | Non-negative integer (grosze) | Price in minor units (grosze), e.g., `1000` = 10.00 PLN, `2500` = 25.00 PLN. Pass `0` for a free ticket (`bilet bezpłatny`). |
| `description` | `string` | No | Defaults to `title` | Short description of the ticket. |
| `subtitle` | `string` | No | Max 14 chars; default `'cena'` | Short subtitle displayed under the title (e.g., `'od osoby'`, `'za 1h'`). |
| `detailedDescription` | `string` | No | Optional | Detailed description of what the ticket includes, shown in the ticket detail view. |
| `imageUrl` | `string` | No | Optional | Image URL for the ticket option (e.g., returned by `go-generate-image`). |
| `userDefinedAmount` | `boolean` | No | Default: `false` | Allow the customer to enter their own custom amount (e.g., donations or tips). |
| `order` | `integer` | No | Default: `0` | Display order (`0` = first). |
| `faqJson` | `string` | No | JSON array string | FAQ items as a JSON array string: `'[{"question":"How long is it valid?","answer":"Valid all day"}]'`. |
| `detailsJson` | `string` | No | JSON object string | Additional key-value details as a JSON object string: `'{"Czas trwania":"4 godziny"}'`. |

#### Response JSON

```json
{
  "productId": "a1b2c3d4-e5f6-4789-abcd-112233445566",
  "title": "Bilet normalny",
  "price": 3500,
  "entryId": "11112222-3333-4444-5555-666677778888",
  "next_step": "Ticket added. Product URL: https://go.paymove.io/a1b2c3d4-e5f6-4789-abcd-112233445566"
}
```

---

### 11. `go-update-ticket-option`

Updates an existing ticket option (pricing entry) on a `GO` product. Only fields provided in the request are modified; omitted fields retain their existing values.

- **Auth Scope:** Partner (`X-API-KEY`)

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `productId` | `string` | **Yes** | UUID | Product ID. |
| `entryId` | `string` | **Yes** | UUID | Entry ID of the ticket option to update (use `go-get-product` to inspect existing `entryId`s). |
| `title` | `string` | No | Optional | New ticket title. |
| `price` | `integer` | No | Non-negative integer (grosze) | New price in minor units (grosze), e.g., `1500` = 15.00 PLN. |
| `subtitle` | `string` | No | Optional | New subtitle displayed under the title. |
| `detailedDescription` | `string` | No | Optional | New detailed description. |
| `imageUrl` | `string` | No | Optional | New image URL for the ticket option. |
| `userDefinedAmount` | `boolean` | No | Optional | Whether the customer can set their own amount. |
| `order` | `integer` | No | Optional | New display order (`0` = first). |
| `faqJson` | `string` | No | JSON array string | Updated FAQ items: `'[{"question":"...","answer":"..."}]'`. |
| `detailsJson` | `string` | No | JSON object string | Updated key-value details: `'{"key":"value"}'`. |

#### Response JSON

```json
{
  "productId": "a1b2c3d4-e5f6-4789-abcd-112233445566",
  "entryId": "11112222-3333-4444-5555-666677778888",
  "status": "updated"
}
```

---

### 12. `go-delete-ticket-option`

Permanently deletes a ticket option (pricing entry) from a `GO` product.

- **Auth Scope:** Partner (`X-API-KEY`)

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `productId` | `string` | **Yes** | UUID | Product ID. |
| `entryId` | `string` | **Yes** | UUID | Ticket option (`entryId`) to delete. |

#### Response JSON

```json
{
  "productId": "a1b2c3d4-e5f6-4789-abcd-112233445566",
  "entryId": "11112222-3333-4444-5555-666677778888",
  "status": "deleted"
}
```

---

### 13. `go-update-product`

Updates an existing `GO` product's layout (`viewType`, `imageDisplayType`), step headers, redemption flag, or post-payment summary link block.

- **Auth Scope:** Partner (`X-API-KEY`)

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `productId` | `string` | **Yes** | UUID | Product ID to update. |
| `viewType` | `string` | No | Optional | Mobile layout: `'grid'`, `'scroll'`, `'slider'`, or `'card'`. |
| `imageDisplayType` | `string` | No | Optional | Image display size: `'full'` or `'medium'`. |
| `stepHeaders` | `string` | No | Max 2 comma-separated | Step headers as comma-separated values (e.g., `'Wybierz bilet, Zapłać'`). |
| `notAvailableToRedeem` | `boolean` | No | Optional | If `true`, tickets are display-only and cannot be redeemed. |
| `summaryLinkTitle` | `string` | No | Optional | Title of the link block shown on the payment summary page. |
| `summaryLinkDescription` | `string` | No | Optional | Description text of the link block on the summary page. |
| `summaryLinkButtonText` | `string` | No | Optional | Button label of the link block on the summary page. |
| `summaryLinkUrl` | `string` | No | Optional | Target URL the summary link block button points to. |
| `summaryLinkEnabled` | `boolean` | No | Optional | If `true`, shows the link block on the summary page. |

#### Response JSON

```json
{
  "productId": "a1b2c3d4-e5f6-4789-abcd-112233445566",
  "status": "updated"
}
```

---

### 14. `go-get-product`

Fetches a `GO` product along with all its ticket options (`pricing.options`) and its public `productLink`. Requires `X-API-KEY: <YOUR_PAYMOVE_API_KEY>`.

- **Auth Scope:** Partner (`X-API-KEY`)

#### Input Parameters

| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `productId` | `string` | **Yes** | — | Product ID (UUID). |
| `locale` | `string` | No | `'pl-PL'` | Locale for translations: `'pl-PL'`, `'en-US'`, `'de-DE'`, or `'uk-UA'`. |

#### Response JSON

Returns the product JSON, including `pricing.options` (each ticket's `entryId`, `title`, `price`, `subtitle`, `detailedDescription`, `imageUrl`, `faq`, `details`) and `"productLink": "https://go.paymove.io/{productId}"`.

---

### 15. `go-set-translations`

Sets multilingual translations for a `GO` product's ticket options in a specified locale.

- **Auth Scope:** Partner (`X-API-KEY`)

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `productId` | `string` | **Yes** | UUID | Product ID. |
| `locale` | `string` | **Yes** | Non-empty string | Target locale: `'pl-PL'`, `'en-US'`, `'de-DE'`, or `'uk-UA'`. |
| `translationsJson` | `string` | **Yes** | JSON object string | JSON object mapping indexed keys to translated strings (`0`-based ticket index): `title_{index}`, `subtitle_{index}`, `description_{index}`, `question_{entryIndex}_{faqIndex}`, `answer_{entryIndex}_{faqIndex}`. Example: `'{"title_0":"Adult Ticket","subtitle_0":"price","description_0":"Full access"}'`. |

#### Response JSON

```json
{
  "productId": "a1b2c3d4-e5f6-4789-abcd-112233445566",
  "locale": "en-US",
  "status": "translations_set",
  "keysCount": 3
}
```

---

### 16. `go-generate-image`

Generates an AI illustration/graphic for a `GO` ticket option and returns its hosted `imageUrl`. Pass the returned `imageUrl` to `go-add-ticket-option` or `go-update-ticket-option`.

- **Auth Scope:** Partner (`X-API-KEY`)

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `prompt` | `string` | **Yes** | Non-empty string | Image description in English — concrete subject, mood, and composition; no text, logos, or prices. |
| `ticketIndex` | `integer` | **Yes** | Integer, minimum 1 | 1-based index of the ticket this image belongs to (`1` for the first ticket, `2` for the second, etc.). |
| `styleId` | `string` | No | Optional | Optional visual style ID (e.g., `'07'`). Use the same `styleId` across all tickets of a product for visual consistency. |

#### Response JSON

```json
{
  "ticketIndex": 1,
  "imageUrl": "https://generated-image.paymove.io/configurator/...",
  "styleId": "07"
}
```

---

## Category 3: Parking & Mobility (`3 tools`)

### 17. `parking-create-product`

Creates a new paid parking zone (`PARKING`) with complete time-based tariff configuration and returns `parkingId` and `parkingLink` (`https://park.paymove.io/{shortName}`). Automatically resolves the next available `shortName` if the requested slug is already taken.

- **Auth Scope:** Partner (`X-API-KEY`)

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `name` | `string` | **Yes** | Non-empty string | Parking display name (e.g., `'Parking Centrum'`, `'Strefa Parkowania A'`). |
| `fullName` | `string` | **Yes** | Non-empty string | Full official name of the parking lot. |
| `shortName` | `string` | **Yes** | Non-empty string | Unique URL slug (letters, numbers, hyphens only, e.g., `'parking-centrum-wroclaw'`). |
| `location` | `string` | **Yes** | Non-empty string | Location/city/address (e.g., `'Wroclaw, ul. Pilsudskiego 10'`). |
| `entriesJson` | `string` | **Yes** | JSON | Time-based tariff. Accepts an indexed object map (`"0"`, `"1"`, …) or a JSON array with shortened durations (`"15m"`, `"1h"`) and amounts. Both shapes are described below. |
| `timezone` | `string` | No | Default: `'Europe/Warsaw'` | Timezone identifier. |
| `groupId` | `string` | No | Optional (UUID) | Existing parking group UUID (only for multi-zone parkings). |
| `groupName` | `string` | No | Optional | Name for a new parking group (only if creating a multi-zone group). |
| `groupLocation` | `string` | No | Optional | Location for a new parking group. |
| `maximumCostPerDay` | `integer` | No | Optional | Maximum daily charge cap in grosze (e.g., `5000` = 50.00 PLN). |
| `maximumCostPerWeek` | `integer` | No | Optional | Maximum weekly charge cap in grosze (e.g., `20000` = 200.00 PLN). |
| `minimumCostPerDay` | `integer` | No | Default: `0` | Minimum cost per day in grosze. |
| `minimumTimePerDay` | `string` | No | Default: `'PT0S'` | Minimum parking duration per day as ISO-8601 duration. |
| `freeTimePerTicket` | `string` | No | Default: `'PT0S'` | Free parking duration included with every ticket (e.g., `'PT15M'` for 15 minutes free). |
| `restartAtMidnight` | `boolean` | No | Default: `false` | Whether to reset tariff calculation at midnight. |
| `limitOptionsToEntries` | `boolean` | No | Default: `false` | Restrict selectable durations strictly to the defined tariff entries. |
| `onlyPlatesTicket` | `boolean` | No | Default: `false` | Require license plate tickets only. |
| `toTheEndOfDay` | `boolean` | No | Default: `false` | Charge until the end of the current day rather than duration-based. |
| `subscriptionsJson` | `string` | No | JSON array string | Long-term subscriptions: `'[{"cost":10000,"duration":"PT720H","toTheEndOfDay":false,"priority":1}]'`. |
| `freeTicketsJson` | `string` | No | JSON array string | Free ticket rules: `'[{"duration":"PT15M","numberOfTickets":1,"from":"08:00","to":"18:00"}]'`. |
| `activeHoursJson` | `string` | No | JSON object string | Paid hours per day of week (`MONDAY`..`SUNDAY`): `'{"MONDAY":{"from":"08:00","to":"20:00"},...}'`. |

#### `entriesJson` formats

**1. Indexed object map.** `cost` is grosze. `duration` is ISO-8601 (`PT15M`, `PT30M`, `PT1H`, `PT24H`). `repeatable` is usually `true` only on the last bracket. `partialCost` charges a partial interval proportionally.

```json
{
  "0": {"order": 0, "cost": 100, "duration": "PT15M", "repeatable": false, "partialCost": false},
  "1": {"order": 1, "cost": 300, "duration": "PT1H", "repeatable": true, "partialCost": false}
}
```

**2. JSON array** — each element becomes the next `"0"`, `"1"`, … entry. Earlier entries are stored with `repeatable: false` and `partialCost: false`. The last accepted entry is stored with `repeatable: true`. An element with no resolvable duration or cost is skipped.

```json
[
  {"duration": "15m", "cost": 100},
  {"duration": "1h", "price": 3}
]
```

Duration, first match wins:

- `durationMinutes` or `minutes` as a positive number → that many minutes (`PT15M` for `15`).
- `duration` text that starts with `PT` (any case) → ISO-8601, uppercased (`"pt15m"` → `PT15M`).
- otherwise a leading number (default `1` when the text has none) plus a unit: `hour` / `godz` or a whole string like `1h` → hours; `min` or a whole string like `15m` → minutes; `day` / `dzie` / `dob` or a whole string like `1d` → days.

Amount, first match wins:

- `cost` (number) → grosze, used as-is (`100` = 1.00 PLN).
- `costPln` or `pricePln` (number) → `Math.round(value * 100)` grosze (`5` → `500`).
- `price` (number) → `Math.round(value * 100)` grosze (`3` → `300`).

`parking-create-event` accepts the indexed object map (format 1).

#### Response JSON

```json
{
  "parkingId": "d4e5f6a7-b8c9-4012-9345-6789abcdef01",
  "name": "Parking Rynek Południe",
  "shortName": "parking-rynek-poludnie",
  "parkingLink": "https://park.paymove.io/parking-rynek-poludnie",
  "next_step": "Parking created and ready to use! URL: https://park.paymove.io/parking-rynek-poludnie"
}
```

---

### 18. `parking-create-event`

Creates a special event (`EVENT`) or temporary tariff override (`PRICING_CHANGE`) for an existing parking lot. Specify either `fixedCost` (flat rate) OR `entriesJson` (time-based tariff), never both.

- **Auth Scope:** Partner (`X-API-KEY`)

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `parkingId` | `string` | **Yes** | UUID | Parking UUID from `parking-create-product`. |
| `from` | `string` | **Yes** | `yyyy-MM-ddTHH:mm:ss` | Event start date/time in ISO-8601 local format (e.g., `'2026-11-15T16:00:00'`). |
| `to` | `string` | **Yes** | `yyyy-MM-ddTHH:mm:ss` | Event end date/time in ISO-8601 local format (e.g., `'2026-11-15T23:59:00'`). |
| `type` | `string` | **Yes** | Non-empty string | `'EVENT'` (special event pricing) or `'PRICING_CHANGE'` (temporary tariff change). |
| `name` | `string` | No | Optional | Event name (e.g., `'Concert at Stadium'`, `'Holiday Rate'`). |
| `notes` | `string` | No | Optional | Additional notes about the event. |
| `repeatEveryDay` | `boolean` | No | Default: `false` | Repeat this event daily. |
| `repeatEveryWeek` | `boolean` | No | Default: `false` | Repeat this event weekly. |
| `fixedCost` | `integer` | No | Mutually exclusive with `entriesJson` | Flat-rate fee in grosze for the entire event (e.g., `3000` = 30.00 PLN). |
| `entriesJson` | `string` | No | Mutually exclusive with `fixedCost` | Indexed object map (format 1 of `parking-create-product`): keys `"0"`, `"1"`, … with `order`, `cost` (grosze), `duration`, `repeatable`, and `partialCost`. |
| `subscriptionsJson` | `string` | No | JSON array string | Subscriptions available during the event period. |
| `imageUrl` | `string` | No | Optional | Image URL for the event banner. |

#### Response JSON

```json
{
  "parkingId": "d4e5f6a7-b8c9-4012-9345-6789abcdef01",
  "type": "EVENT",
  "from": "2026-11-15T16:00:00",
  "to": "2026-11-15T23:59:00",
  "status": "created",
  "name": "Concert at Stadium"
}
```

---

### 19. `parking-get-pricing`

Retrieves the current pricing configuration (tariff entries, active hours, daily/weekly caps, subscriptions, free tickets, and scheduled events) for a parking lot. Requires `X-API-KEY: <YOUR_PAYMOVE_API_KEY>`.

- **Auth Scope:** Partner (`X-API-KEY`)

#### Input Parameters

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `parkingIdOrShortName` | `string` | **Yes** | Parking UUID or URL `shortName`. |

#### Response JSON

Returns JSON containing `entries`, `activeHours`, `maximumCostPerDay`, `maximumCostPerWeek`, `minimumCostPerDay`, `freeTimePerTicket`, `subscriptions`, `freeTickets`, and `events`.

---

## Category 4: Public Discovery & Partner Catalog (`2 tools`)

`search-public-products` is the only MCP tool that runs without an API key. It finds active `GO`, `PAY`, and `PARKING` products and returns a direct `productLink`. The other 19 tools require `X-API-KEY: <YOUR_PAYMOVE_API_KEY>`. `list-partner-products` returns up to 100 products belonging to the authenticated partner account.

The intended catalog rule, once [P10 `set-product-visibility`](#p10-set-product-visibility) and [P11 `get-product-status`](#p11-get-product-status) ship, is that a product appears here only when its status is `ACTIVE`, its visibility is `public`, and the owning partner has finished KYC in [panel.paymove.io](https://panel.paymove.io). That rule is **Planned / Planowane**. It does not add fields to this live tool, and it does not change the response documented below.

### 20. `search-public-products`

Searches active public Paymove products (`GO` tickets and attractions, `PAY` payments and services, `PARKING` zones) and returns direct purchase links. No API key is required. The tool also works when `X-API-KEY` is set. Results are limited to 50 products, sorted by name ascending.

- **Auth Scope:** Public (no `X-API-KEY` required; also available with a partner key)

#### Input Parameters (all optional)

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `query` | `string` | No | Search text matched against `name`, `fullName`, `shortName`, or `location` (e.g. `"zoo"`, `"muzeum"`, `"lotnisko"`). |
| `location` | `string` | No | City or location filter (e.g. `"Warszawa"`, `"Gdynia"`, `"Gdańsk"`). |
| `productType` | `string` | No | `GO`, `PAY`, or `PARKING`. Omit it to search all three. Any other value is rejected. |

#### Invalid `productType`

```json
{
  "error": "Invalid productType. Allowed values: GO, PAY, PARKING",
  "productType": "TICKET"
}
```

`productType` in that object is the raw argument the caller sent.

#### Response JSON

The response object is exactly `count`, `totalElements`, and `products`.

| Field | Type | Description |
| :--- | :--- | :--- |
| `count` | `integer` | Number of products in this response. At most `50`, ordered by `name` ascending. |
| `totalElements` | `integer` | Total number of matching products. This can be larger than `count`. |
| `products` | `array` | One object per returned product. |

Each product object always includes `productId` and `name`. The following are included only when non-null: `fullName`, `shortName`, `productType` (`GO` / `PAY` / `PARKING`), `location`, `currency` (`PLN` / `EUR` / `CZK`), and `productLink`.

`productLink` uses `shortName` when it is non-blank, otherwise `productId`:

- `GO` → `https://go.paymove.io/{shortName}` (sandbox: `https://go.sandbox.paymove.io/{shortName}`)
- `PAY` → `https://pay.paymove.io/{shortName}` (sandbox: `https://pay.sandbox.paymove.io/{shortName}`)
- `PARKING` → `https://park.paymove.io/{shortName}` (sandbox: `https://park.sandbox.paymove.io/{shortName}`)

```json
{
  "count": 1,
  "totalElements": 1,
  "products": [
    {
      "productId": "393e5f92-cdd8-4ec8-b4d1-ebb4ec2d51f7",
      "name": "Bilety Zoo Gdańsk",
      "fullName": "Gdański Ogród Zoologiczny",
      "shortName": "cb60",
      "productType": "GO",
      "location": "Gdańsk",
      "currency": "PLN",
      "productLink": "https://go.paymove.io/cb60"
    }
  ]
}
```

An empty match is `{ "count": 0, "totalElements": 0, "products": [] }`.

---

### 1. `list-partner-products`

Lists up to 100 products belonging to the authenticated partner account, filtered by product type. Call this before creating a sub-resource (for example a checkout under an existing `PAY` product). Requires `X-API-KEY: <YOUR_PAYMOVE_API_KEY>`.

- **Auth Scope:** Partner (`X-API-KEY`)

#### Input Parameters

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `productType` | `string` | **Yes** | `PAY`, `GO`, or `PARKING`. |

#### Response JSON

```json
{
  "partnerId": "c8f2b8a1-4d3c-4e12-9a01-123456789abc",
  "productType": "PAY",
  "count": 1,
  "products": [
    {
      "productId": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Legal Consultation",
      "shortName": "legal-consultation",
      "location": "Online"
    }
  ]
}
```

| Field | Type | Description |
| :--- | :--- | :--- |
| `partnerId` | `string` (UUID) | Identifier of the authenticated partner account. |
| `productType` | `string` | The `productType` you sent. |
| `count` | `integer` | Number of products in this response (at most 100). |
| `products[].productId` | `string` (UUID) | Product id. |
| `products[].name` | `string` | Product name. |
| `products[].shortName` | `string` | Present only when non-null. |
| `products[].location` | `string` | Present only when non-null. |

---

## Planned tools

> **Status: Planned / Planowane.** None of the tools in this section exist on the server. They are absent from `tools/list` on `https://api.paymove.io/api/mcp` and `https://mcp-api.paymove.io/mcp`. They are not part of the 20 live tools. An agent must not call them, must not invent a success response, and must not tell the user the call worked. Call a tool from this section only after its name appears in `tools/list`.

This section is the contract draft for partners who have finished KYC in [panel.paymove.io](https://panel.paymove.io) and want to add and run offers through MCP. A new partner product is always an instance of `PAY`, `GO`, or `PARKING`. This draft does not add a product type, and it does not add a second create tool. Tickets keep using `go-create-product`. Parking keeps using `parking-create-product`. A service without a date, and an appointment book, keep using `create-pay-product` plus pricing entries.

End-to-end sequences, with synthetic names, are in [docs/use-cases.md](./use-cases.md) and [docs/use-cases.pl.md](./use-cases.pl.md). Call payloads are in [`examples/planned/`](../examples/planned/).

### Planned conventions

- **Monetary amounts** stay integers in grosze. `1000` = 10.00 PLN. Never send a float. There is no currency field.
- **Authentication** uses `X-API-KEY`. Optional `X-SANDBOX-API-KEY` (`sk_test_...`) routes the call to the Paymove Sandbox, same as the live partner tools. Do not send `Authorization: Bearer`. Do not send an `Idempotency-Key` header.
- **Server-side only.** The key stays off the merchant page.
- **Arguments.** Write tools take a top-level `request` object. `list-availability`, `get-reservation`, `list-product-webhooks`, and `get-product-status` take their fields directly in `arguments`, same as `go-get-product` and `parking-get-pricing`.
- **Errors** use `{"status": <int>, "error": "<CODE>", "message": "<text>"}`. Branch on `status`. `error` is the stable code in this draft. `message` is for humans and is not a stable API. A live REST failure, where these tools mirror REST, stays `{"status": <int>, "message": "<text>"}`; the MCP layer adds `error` when it maps that failure.
- **Read / write** is marked on every tool as **Access**. Read tools do not create or mutate offers, holds, webhooks, tariffs, or visibility.

| `status` | `error` | When |
| :--- | :--- | :--- |
| `400` | `INVALID_REQUEST` | Missing required field, bad UUID, `end` not after `start`, `capacity` not an integer ≥ 0, `method` other than `POST`, `visibility` other than `public` or `hidden`, `retries` < 1. |
| `400` | `PRICE_NOT_ACCEPTED` | `create-reservation` included `price` or `amount`. The server computes the price. |
| `400` | `PRICE_NOT_FIXED` | The attached entry has `userDefinedAmount: true`, or the computed price is not a positive integer. The hold is not taken. |
| `400` | `ENTRIES_NOT_CANONICAL` | `parking-update-pricing` received the shorthand array. Send the indexed object map. |
| `401` | `INVALID_API_KEY` | Missing or wrong `X-API-KEY` on a partner tool. |
| `403` | `ACCESS_DENIED` | The product, entry, reservation, or webhook belongs to another partner. |
| `404` | `NOT_FOUND` | Unknown product, entry, slot, reservation, or webhook for an authenticated partner. |
| `404` | `PRODUCT_NOT_AVAILABLE` | Public `list-availability` for a product that is not searchable. |
| `409` | `SLOT_OVERLAP` | The slot overlaps another slot for the same `resource`. Nothing is written. |
| `409` | `SLOT_FULL` | Remaining capacity is lower than `quantity`. No hold is taken. |
| `409` | `SLOT_HAS_RESERVATIONS` | A replace would drop a slot that still has a `HELD` or `COMPLETED` reservation. |
| `409` | `CAPACITY_BELOW_RESERVED` | New `capacity` is lower than held plus completed seats on that slot. |
| `409` | `EXTERNAL_ID_CONFLICT` | `externalId` already belongs to a different reservation or subproduct. |
| `409` | `RESERVATION_COMPLETED` | `cancel-reservation` on a confirmed reservation. No refund is started. |
| `409` | `RESERVATION_EXPIRED` | `cancel-reservation` on an expired hold. Capacity was already released. |

### What a partner product is

| Offer | Product type | Live create tool | Sellable unit the new tools attach to |
| :--- | :--- | :--- | :--- |
| Event tickets, workshops, timed entry | `GO` | `go-create-product`, then `go-add-ticket-option` | `targetType: "GO_TICKET"` and that option's `entryId` |
| Paid parking | `PARKING` | `parking-create-product` | No slots. Edit the base tariff with `parking-update-pricing`. Temporary overrides stay on `parking-create-event`. |
| Service with no date (a fee, a package, a translation) | `PAY` | `create-pay-product`, then `add-pay-pricing-entry` | No slots. Checkout stays on `create-subproduct` or the public pay link. |
| Appointment with time slots (hairdresser, a visit) | `PAY` | `create-pay-product` with `price: 0` when each service has its own entry, then `add-pay-pricing-entry` | `targetType: "PAY_ENTRY"` and that entry's `entryId` |

KYC stays in the panel. No planned tool submits KYC.

### Availability and reservations

Slots attach to an existing `GO` ticket option or an existing `PAY` pricing entry. They are not a product. `PARKING` does not take slots.

A slot is a half-open local interval `[start, end)` in an IANA timezone. `start` and `end` use `yyyy-MM-ddTHH:mm:ss` with no offset, the same local form as `parking-create-event`. The default timezone is `Europe/Warsaw`.

`capacity` is the number of seats on that slot. Remaining seats are `capacity` minus reservations in `HELD` or `COMPLETED`. An expired or canceled hold does not consume a seat.

`resource` is an optional label the partner chooses (a stylist, a room, a chair), for example `"stylist-a"`. On one product, the same non-empty `resource` cannot have overlapping intervals, including across two entries, so one person is not booked twice. Slots with no `resource` compete only with other resourceless slots on the same `entryId`.

**Anti double-sell.** `create-reservation` locks the slot, checks remaining capacity, inserts the hold, and creates the checkout in one transaction. Two callers who take the last seat: one receives the hold, the other receives `409` `SLOT_FULL`. A repeat with the same `externalId` and the same slot does not take a second seat.

**Hold and TTL.** A new reservation is `HELD`. The proposed default TTL is **600 seconds** (10 minutes). The caller may send `ttlSeconds` from **60** to **900**. `expiresAt` is an absolute instant. When the clock passes `expiresAt` and the status is still `HELD`, the status becomes `EXPIRED` and the seats return to the pool. A `COMPLETED` reservation is never expired by the TTL job.

**Idempotency.** The idempotency key is `externalId`, unique per product, the same identifier the subproduct uses. The same `externalId` with the same `entryId`, slot, and `quantity` returns the original `reservationId` and `redirectUrl` and sets `idempotentReplay` to `true`. A different slot or quantity for that `externalId` is `409` `EXTERNAL_ID_CONFLICT`. Do not send `Idempotency-Key`.

**Server-side price.** `create-reservation` has no `price` and no `amount`. The server reads the attached entry (`GO` ticket `price`, or `PAY` pricing-entry `price`) and sets the checkout amount to `entry.price * quantity`, in grosze. Sending `price` or `amount` is `400` `PRICE_NOT_ACCEPTED`. An entry with `userDefinedAmount: true`, or a computed amount that is not a positive integer, is `400` `PRICE_NOT_FIXED` and takes no hold. The checkout is the existing subproduct flow: `redirectUrl` is `https://checkout.paymove.io/{productId}?externalId={10charHash}` (sandbox: `https://checkout.sandbox.paymove.io/{productId}?externalId={10charHash}`). The query value is Paymove's 10-character hash. The caller does not call `create-subproduct` for a slotted entry; that call would skip the hold.

**Confirmation.** Status `HELD` is a hold, not a booking. The customer opening `returnUrl` does not confirm anything. The reservation becomes `COMPLETED` only when the payment for that `externalId` reaches `COMPLETED`. The partner fulfils (email, calendar, ticket) only in the webhook handler, after verifying `X-Paymove-Signature`. There is no tool that sets `COMPLETED` by hand. `get-reservation` reports `confirmed: true` only for status `COMPLETED`.

Reservation status values: `HELD`, `EXPIRED`, `COMPLETED`, `CANCELED`.

### P1. `set-availability`

> **Status:** Planned / Planowane — not implemented, absent from `tools/list`.

Replaces or upserts bookable slots on one existing `GO` ticket option or one existing `PAY` pricing entry.

- **Auth Scope:** Partner (`X-API-KEY`, optional `X-SANDBOX-API-KEY`)
- **Access:** Write

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `targetType` | `string` | **Yes** | `GO_TICKET` or `PAY_ENTRY` | Which sellable unit the slots belong to. |
| `productId` | `string` | **Yes** | UUID | `GO` product from `go-create-product`, or `PAY` product from `create-pay-product`. Must belong to the authenticated partner. |
| `entryId` | `string` | **Yes** | UUID | Ticket `entryId` from `go-add-ticket-option` / `go-get-product`, or pricing `entryId` from `add-pay-pricing-entry` / `list-pay-pricing-entries`. |
| `timezone` | `string` | No | Default: `'Europe/Warsaw'` | IANA timezone for `start` and `end`. |
| `mode` | `string` | No | Default: `'upsert'` | `'upsert'` or `'replace'`. |
| `replaceFrom` | `string` | No | Local `yyyy-MM-ddTHH:mm:ss` | Used when `mode` is `'replace'`. Slots that start before this instant are kept. Default: the current time in `timezone`. |
| `slots` | `array` | **Yes** | At least one object | Slot objects. See the next table. |

Each element of `slots`:

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `start` | `string` | **Yes** | `yyyy-MM-ddTHH:mm:ss`, no offset | Inclusive local start. |
| `end` | `string` | **Yes** | Same form, strictly after `start` | Exclusive local end. |
| `capacity` | `integer` | **Yes** | Integer ≥ 0 | Seats on this slot. `0` closes it. |
| `resource` | `string` | No | Omit or non-empty string | Staff, room, or chair label. |

`upsert` matches an existing slot by `(entryId, start, end, resource)` and updates `capacity`. Other slots stay. `replace` makes the submitted list the full set of slots for this `entryId` that start at or after `replaceFrom`. A slot that still has a `HELD` or `COMPLETED` reservation cannot be removed, and its capacity cannot drop below the reserved seats. On `SLOT_OVERLAP`, `SLOT_HAS_RESERVATIONS`, or `CAPACITY_BELOW_RESERVED` the call writes nothing.

#### Response JSON

```json
{
  "productId": "550e8400-e29b-41d4-a716-446655440000",
  "entryId": "9f8e7d6c-5b4a-3210-fedc-ba9876543210",
  "targetType": "PAY_ENTRY",
  "timezone": "Europe/Warsaw",
  "mode": "upsert",
  "slotsWritten": 2
}
```

#### Error example

```json
{
  "status": 409,
  "error": "SLOT_OVERLAP",
  "message": "Resource stylist-a already has a slot overlapping 2026-11-20T10:00:00/2026-11-20T10:30:00."
}
```

---

### P2. `list-availability`

> **Status:** Planned / Planowane — not implemented, absent from `tools/list`.

Lists slots and remaining seats for one product. Usable without an API key when the product is searchable (active, public, and the partner has finished KYC). With `X-API-KEY`, the partner can also list their own hidden products.

- **Auth Scope:** Public for a searchable product. Partner (`X-API-KEY`, optional `X-SANDBOX-API-KEY`) for the caller's own products, including hidden ones.
- **Access:** Read

#### Input Parameters

| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `productId` | `string` | **Yes** | — | Product UUID. |
| `entryId` | `string` | No | All entries that have slots | Limit the list to one ticket option or one pricing entry. |
| `from` | `string` | No | Now, in `timezone` | Local `yyyy-MM-ddTHH:mm:ss`. Slots that end at or before `from` are omitted. |
| `to` | `string` | No | `from` plus 31 days | Local exclusive upper bound on `start`. |
| `resource` | `string` | No | All resources | Filter to one resource label. |
| `timezone` | `string` | No | `'Europe/Warsaw'` | Zone used to interpret `from` and `to`. |

A public caller who asks for a product that is missing, hidden, inactive, or owned by a partner without KYC receives `404` `PRODUCT_NOT_AVAILABLE`. The body does not say which of those applies.

The public response contains slots only. It does not contain customer data, reservation ids, or `externalId` values. `remaining` counts `HELD` and `COMPLETED` seats as taken.

#### Response JSON

```json
{
  "productId": "550e8400-e29b-41d4-a716-446655440000",
  "timezone": "Europe/Warsaw",
  "count": 1,
  "slots": [
    {
      "entryId": "9f8e7d6c-5b4a-3210-fedc-ba9876543210",
      "targetType": "PAY_ENTRY",
      "start": "2026-11-20T10:00:00",
      "end": "2026-11-20T10:30:00",
      "resource": "stylist-a",
      "capacity": 1,
      "remaining": 1
    }
  ]
}
```

---

### P3. `create-reservation`

> **Status:** Planned / Planowane — not implemented, absent from `tools/list`.

Atomically holds seats on one existing slot and opens a checkout through the existing subproduct flow. The price is computed on the server from the attached entry. The reservation is confirmed only after the payment reaches `COMPLETED`.

- **Auth Scope:** Partner (`X-API-KEY`, optional `X-SANDBOX-API-KEY`)
- **Access:** Write

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `targetType` | `string` | **Yes** | `GO_TICKET` or `PAY_ENTRY` | Must match the entry the slot was attached to. |
| `productId` | `string` | **Yes** | UUID | Parent product. |
| `entryId` | `string` | **Yes** | UUID | Ticket option or pricing entry that owns the slot. |
| `start` | `string` | **Yes** | `yyyy-MM-ddTHH:mm:ss` | Must match a slot `start` exactly. |
| `end` | `string` | **Yes** | `yyyy-MM-ddTHH:mm:ss` | Must match that slot's `end` exactly. |
| `resource` | `string` | No | Required when the slot has a resource | Resource label of the slot. Omit for a resourceless slot. |
| `quantity` | `integer` | No | Default: `1`; integer ≥ 1 | Seats to hold. Must be ≤ remaining. |
| `externalId` | `string` | **Yes** | Non-empty, unique per product | Idempotency key and the subproduct `externalId`. |
| `returnUrl` | `string` | **Yes** | Absolute `https` URL | Passed through as the subproduct `details.returnUrl`. A visit here does not confirm the reservation. |
| `ttlSeconds` | `integer` | No | Default: `600`; min `60`; max `900` | Hold length. Proposed bounds, see the open questions in the use-case guide. |
| `email` | `string` | No | Optional | Customer email stored on the checkout. |
| `locale` | `string` | No | Default: `'pl-PL'` | Checkout locale. |
| `description` | `string` | No | Defaults to the entry title or description | Text shown on the checkout. |

Do not send `price`, `amount`, or `Idempotency-Key`. The server multiplies the entry price by `quantity`.

#### Response JSON

```json
{
  "reservationId": "c1d2e3f4-a5b6-4789-8abc-def012345678",
  "externalId": "APT-1001",
  "status": "HELD",
  "confirmed": false,
  "quantity": 1,
  "price": 8000,
  "ttlSeconds": 600,
  "expiresAt": "2026-11-20T09:10:00+01:00",
  "idempotentReplay": false,
  "redirectUrl": "https://checkout.paymove.io/550e8400-e29b-41d4-a716-446655440000?externalId=ab12cd34ef",
  "slot": {
    "entryId": "9f8e7d6c-5b4a-3210-fedc-ba9876543210",
    "start": "2026-11-20T10:00:00",
    "end": "2026-11-20T10:30:00",
    "resource": "stylist-a",
    "remaining": 0
  }
}
```

`price` is grosze (`8000` = 80.00 PLN) and is the amount the server put on the subproduct. `redirectUrl` uses the live checkout host. Fulfilment waits for a verified webhook with `status: "COMPLETED"`.

#### Error example

```json
{
  "status": 409,
  "error": "SLOT_FULL",
  "message": "No remaining capacity for this slot."
}
```

---

### P4. `get-reservation`

> **Status:** Planned / Planowane — not implemented, absent from `tools/list`.

Reads one reservation. `confirmed` is `true` only when `status` is `COMPLETED`.

- **Auth Scope:** Partner (`X-API-KEY`, optional `X-SANDBOX-API-KEY`)
- **Access:** Read

#### Input Parameters

Send `reservationId`, or send both `productId` and `externalId`.

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `reservationId` | `string` | One of this or the pair below | Reservation UUID from `create-reservation`. |
| `productId` | `string` | With `externalId` | Parent product UUID. |
| `externalId` | `string` | With `productId` | The idempotency key sent to `create-reservation`. |

#### Response JSON

```json
{
  "reservationId": "c1d2e3f4-a5b6-4789-8abc-def012345678",
  "productId": "550e8400-e29b-41d4-a716-446655440000",
  "entryId": "9f8e7d6c-5b4a-3210-fedc-ba9876543210",
  "targetType": "PAY_ENTRY",
  "externalId": "APT-1001",
  "status": "HELD",
  "paymentStatus": "PENDING",
  "confirmed": false,
  "quantity": 1,
  "price": 8000,
  "expiresAt": "2026-11-20T09:10:00+01:00",
  "redirectUrl": "https://checkout.paymove.io/550e8400-e29b-41d4-a716-446655440000?externalId=ab12cd34ef",
  "slot": {
    "start": "2026-11-20T10:00:00",
    "end": "2026-11-20T10:30:00",
    "resource": "stylist-a"
  }
}
```

`paymentStatus` is the subproduct status (`INITIALIZED`, `PENDING`, `COMPLETED`, `CANCELED`, `ERROR`, `REFUNDED`) or `null` before the checkout exists. `status` is the reservation. A payment that reaches `COMPLETED` after the hold has already become `EXPIRED` does not set `confirmed` to `true`; the seat may already belong to someone else.

---

### P5. `cancel-reservation`

> **Status:** Planned / Planowane — not implemented, absent from `tools/list`.

Releases a hold that is still `HELD`. A second cancel of the same `CANCELED` reservation returns the same body and does not change capacity again.

- **Auth Scope:** Partner (`X-API-KEY`, optional `X-SANDBOX-API-KEY`)
- **Access:** Write

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `reservationId` | `string` | **Yes** | UUID | Reservation to cancel. |
| `reason` | `string` | No | Optional | Partner note stored on the reservation. It does not start a refund. |

`HELD` becomes `CANCELED` and the seats return to the slot. `EXPIRED` returns `409` `RESERVATION_EXPIRED`. `COMPLETED` returns `409` `RESERVATION_COMPLETED` and does not refund. Refunds stay on the payment API.

#### Response JSON

```json
{
  "reservationId": "c1d2e3f4-a5b6-4789-8abc-def012345678",
  "status": "CANCELED",
  "confirmed": false,
  "releasedQuantity": 1
}
```

---

### Webhooks

These three tools mirror the live webhook REST API. Until they appear in `tools/list`, register and assign webhooks with REST, as in [SKILL.md](../SKILL.md) Step 2. REST today:

- `POST /api/pay/plugin/webhook`
- `POST /api/pay/plugin/webhook/{webhookId}/products/{productId}` (no body)
- `GET /api/pay/plugin/webhook/{webhookId}/products`

Reference: https://docs.paymove.io/en/webhooks.md and https://docs.paymove.io/en/webhook-signature.md.

Signature reminder, for every webhook these tools register: Paymove sends `X-Paymove-Signature: t=<unix>,v1=<base64>`. Verify HMAC-SHA256 over `"{timestamp}.{raw_body}"` with the full `whsec_…` secret as the UTF-8 key. Reject a timestamp older than 300 seconds. Compare with a length check before a constant-time compare. Read the raw body. Respond with the HTTP status equal to `expectedCode` (use `200`). Fulfil only after that check, and only when `status` is `COMPLETED`. A hit on `returnUrl` is not payment. Webhooks fire on terminal statuses; a reservation is confirmed only by `COMPLETED`.

The live REST docs mark webhook `type: "PAYMENT"` as deprecated and tell new integrations to send `type: "TRANSACTION"` (payments and refunds). This draft accepts both. The example below uses `PAYMENT`, which is the type this contract was asked to mirror. Which value the shipped tool should default to is an open question. Omit `requestTemplate` to receive the default payload.

`signingSecret` is returned once, by `register-webhook`. The list tool does not return it. Store it as `PAYMOVE_WEBHOOK_SECRET`. The examples use a placeholder, not a real secret.

### P6. `register-webhook`

> **Status:** Planned / Planowane — not implemented, absent from `tools/list`.

Registers a webhook. Mirrors `POST /api/pay/plugin/webhook`.

- **Auth Scope:** Partner (`X-API-KEY`, optional `X-SANDBOX-API-KEY`)
- **Access:** Write

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `name` | `string` | **Yes** | Non-empty string | Webhook name, for example `'OrderPaymentHook'`. |
| `endpoint` | `string` | **Yes** | Absolute `https` URL | Public URL Paymove will call. |
| `method` | `string` | **Yes** | Must be `'POST'` | HTTP method. Any other value is `400`. |
| `expectedCode` | `integer` | **Yes** | HTTP status, typically `200` | Delivery succeeds only when the endpoint returns this status. |
| `retries` | `integer` | **Yes** | Integer ≥ 1, typically `3` | Extra attempts after the first delivery. |
| `type` | `string` | **Yes** | `'PAYMENT'` or `'TRANSACTION'` | `PAYMENT` matches the mirrored example. Live REST recommends `TRANSACTION`. |
| `partnerId` | `string` | **Yes** | UUID | Partner id assigned by Paymove. The agent asks the user. It is not guessed. |
| `headers` | `object` | No | Default: `{"Content-Type": ["application/json"]}` | Headers Paymove sends to `endpoint`. Values are string arrays, as in REST. |
| `requestTemplate` | `object` | No | Omit for the full default payload | Template object. Do not send the string `"null"`. |

#### Response JSON

```json
{
  "webhookId": "11112222-3333-4444-5555-666677778888",
  "name": "OrderPaymentHook",
  "endpoint": "https://atelier-nici.example/api/payments/webhook",
  "method": "POST",
  "expectedCode": 200,
  "retries": 3,
  "type": "PAYMENT",
  "signingSecret": "whsec_example_not_a_real_secret"
}
```

Assign the webhook next. A registered webhook that is not assigned does not receive events.

---

### P7. `assign-webhook-to-product`

> **Status:** Planned / Planowane — not implemented, absent from `tools/list`.

Links a webhook to a product. Mirrors `POST /api/pay/plugin/webhook/{webhookId}/products/{productId}` with no body. Without this step, payments still succeed and no notification is delivered.

- **Auth Scope:** Partner (`X-API-KEY`, optional `X-SANDBOX-API-KEY`)
- **Access:** Write

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `webhookId` | `string` | **Yes** | UUID | From `register-webhook`. |
| `productId` | `string` | **Yes** | UUID | `PAY`, `GO`, or `PARKING` product that should emit events to this webhook. |

#### Response JSON

```json
{
  "webhookId": "11112222-3333-4444-5555-666677778888",
  "productId": "550e8400-e29b-41d4-a716-446655440000",
  "status": "assigned"
}
```

Assigning the same pair again returns `status: "assigned"` and does not create a second link.

---

### P8. `list-product-webhooks`

> **Status:** Planned / Planowane — not implemented, absent from `tools/list`.

Lists webhook-to-product links. Mirrors `GET /api/pay/plugin/webhook/{webhookId}/products`. Pass `webhookId` to read that webhook's products. Pass `productId` to read the webhooks assigned to that product. Pass both to test one pair. At least one is required.

- **Auth Scope:** Partner (`X-API-KEY`, optional `X-SANDBOX-API-KEY`)
- **Access:** Read

#### Input Parameters

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `productId` | `string` | One of the two | Product UUID. |
| `webhookId` | `string` | One of the two | Webhook UUID. |

#### Response JSON

```json
{
  "count": 1,
  "assignments": [
    {
      "webhookId": "11112222-3333-4444-5555-666677778888",
      "productId": "550e8400-e29b-41d4-a716-446655440000",
      "name": "OrderPaymentHook",
      "endpoint": "https://atelier-nici.example/api/payments/webhook",
      "method": "POST",
      "expectedCode": 200,
      "retries": 3,
      "type": "PAYMENT"
    }
  ]
}
```

The response never includes `signingSecret`.

---

### P9. `parking-update-pricing`

> **Status:** Planned / Planowane — not implemented, absent from `tools/list`.

Replaces the base tariff of an existing `PARKING` product. It does not create a parking, and it does not edit an `EVENT` or `PRICING_CHANGE` created by `parking-create-event`. Read the current tariff with the live tool `parking-get-pricing` first, then send it back in the canonical map.

- **Auth Scope:** Partner (`X-API-KEY`, optional `X-SANDBOX-API-KEY`)
- **Access:** Write

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `parkingId` | `string` | **Yes** | UUID | From `parking-create-product`. |
| `entriesJson` | `string` | **Yes** | Canonical indexed object map | Full replacement of the base `entries` map. The shorthand array accepted by `parking-create-product` is rejected with `400` `ENTRIES_NOT_CANONICAL`. |
| `timezone` | `string` | No | Unchanged when omitted | IANA timezone. |
| `maximumCostPerDay` | `integer` | No | Grosze, ≥ 0 | Daily cap. Omit to keep the current value. |
| `maximumCostPerWeek` | `integer` | No | Grosze, ≥ 0 | Weekly cap. Omit to keep the current value. |
| `minimumCostPerDay` | `integer` | No | Grosze, ≥ 0 | Minimum charge per day. |
| `minimumTimePerDay` | `string` | No | ISO-8601 duration | For example `'PT0S'`. |
| `freeTimePerTicket` | `string` | No | ISO-8601 duration | For example `'PT15M'`. |
| `restartAtMidnight` | `boolean` | No | Optional | Reset the tariff calculation at midnight. |
| `limitOptionsToEntries` | `boolean` | No | Optional | Restrict selectable durations to the defined entries. |
| `onlyPlatesTicket` | `boolean` | No | Optional | License-plate tickets only. |
| `toTheEndOfDay` | `boolean` | No | Optional | Charge through the end of the day. |
| `subscriptionsJson` | `string` | No | JSON array string | Same shape as `parking-create-product`. Omit to keep the current list. |
| `freeTicketsJson` | `string` | No | JSON array string | Same shape as `parking-create-product`. |
| `activeHoursJson` | `string` | No | JSON object string | Paid hours per weekday, same shape as `parking-create-product`. |

#### Canonical `entriesJson`

Keys are `"0"`, `"1"`, … in order. Every value has:

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `order` | `integer` | **Yes** | Same as the key's index. |
| `cost` | `integer` | **Yes** | Grosze, ≥ 0. `300` = 3.00 PLN. Not a float, not a PLN decimal. |
| `duration` | `string` | **Yes** | ISO-8601 duration starting with `PT`, for example `'PT15M'`, `'PT1H'`, `'PT24H'`. |
| `repeatable` | `boolean` | **Yes** | Usually `true` only on the last bracket. |
| `partialCost` | `boolean` | **Yes** | When `true`, a partial interval is charged proportionally. |

```json
{
  "0": {"order": 0, "cost": 200, "duration": "PT30M", "repeatable": false, "partialCost": false},
  "1": {"order": 1, "cost": 500, "duration": "PT1H", "repeatable": true, "partialCost": false}
}
```

`entriesJson` is that object encoded as a string, the same way `parking-create-product` takes format 1.

#### Response JSON

```json
{
  "parkingId": "d4e5f6a7-b8c9-4012-9345-6789abcdef01",
  "status": "updated",
  "entries": {
    "0": {"order": 0, "cost": 200, "duration": "PT30M", "repeatable": false, "partialCost": false},
    "1": {"order": 1, "cost": 500, "duration": "PT1H", "repeatable": true, "partialCost": false}
  }
}
```

`entries` is the canonical map now stored. Event windows are unchanged. Read them with `parking-get-pricing`.

---

### Catalog visibility

`search-public-products` lists a product only when all three are true:

1. Product `status` is `ACTIVE`.
2. Visibility is `public`.
3. The owning partner has completed KYC in [panel.paymove.io](https://panel.paymove.io).

KYC is not an MCP call. `kycVerified` is read-only. A partner can set `visibility` to `public` before KYC is finished; `searchable` stays `false` and `searchableReason` is `KYC_REQUIRED`. Hidden and inactive products stay available to the owning partner's tools. Public `list-availability` follows the same searchable rule.

`searchableReason` is one of `OK`, `HIDDEN`, `INACTIVE`, `KYC_REQUIRED`. Branch on that field and on `status`, not on `message`.

### P10. `set-product-visibility`

> **Status:** Planned / Planowane — not implemented, absent from `tools/list`.

Sets whether a partner product is allowed into the public catalog. Applies to `PAY`, `GO`, and `PARKING`. It does not change `status`, KYC, or the price list.

- **Auth Scope:** Partner (`X-API-KEY`, optional `X-SANDBOX-API-KEY`)
- **Access:** Write

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `productId` | `string` | **Yes** | UUID | Product to update. |
| `visibility` | `string` | **Yes** | `'public'` or `'hidden'` | `'hidden'` removes the product from `search-public-products`. `'public'` allows listing once status is `ACTIVE` and KYC is done. |

#### Response JSON

```json
{
  "productId": "550e8400-e29b-41d4-a716-446655440000",
  "productType": "PAY",
  "status": "ACTIVE",
  "visibility": "public",
  "kycVerified": true,
  "searchable": true,
  "searchableReason": "OK"
}
```

A second call with the same `visibility` returns the same body.

---

### P11. `get-product-status`

> **Status:** Planned / Planowane — not implemented, absent from `tools/list`.

Reads status, visibility, and whether the product currently qualifies for `search-public-products`.

- **Auth Scope:** Partner (`X-API-KEY`, optional `X-SANDBOX-API-KEY`)
- **Access:** Read

#### Input Parameters

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `productId` | `string` | **Yes** | Product UUID belonging to the authenticated partner. |

#### Response JSON

```json
{
  "productId": "550e8400-e29b-41d4-a716-446655440000",
  "productType": "PAY",
  "status": "ACTIVE",
  "visibility": "hidden",
  "kycVerified": true,
  "searchable": false,
  "searchableReason": "HIDDEN"
}
```

`status` uses the product's existing lifecycle values (`ACTIVE` and any non-active value the panel already stores). This tool does not add a product type.

