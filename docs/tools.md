# Paymove MCP Server — Complete Reference of All 20 Tools

This document provides the complete technical reference for all **20 `@Tool` methods** across **4 categories** exposed by the production **Paymove MCP Server** (`paymove-mcp-server`, Streamable HTTP). Primary live endpoint: `https://api.paymove.io/api/mcp`. The same server is also available at `https://mcp-api.paymove.io/mcp`.

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

---

## Conventions & Authentication Scope

- **Monetary Amounts (`1/100 PLN — grosze`):** Every monetary field (`price`, `amount`, `grossAmount`, `cost`, `fixedCost`, `maximumCostPerDay`, `maximumCostPerWeek`, `minimumCostPerDay`) is an integer (`long`/`int`) in **minor units (grosze)**.
  - `1000` = **10.00 PLN**
  - `3500` = **35.00 PLN**
  - `150000` = **1500.00 PLN**
- **Tool Visibility (`tools/list`) / Authentication Modes:**
  - **Public Discovery Mode (no headers required):** Exposes `search-public-products` and allows inspecting public product details and pricing (`go-get-product`, `parking-get-pricing`, `list-pay-pricing-entries`) so any consumer AI agent can discover and buy services without merchant credentials.
  - **Partner Mode (`X-API-KEY`):** Exposes partner management tools across `Pay`, `Pay&Go`, and `Parking`, plus `list-partner-products`. Optional `X-SANDBOX-API-KEY` (`sk_test_...`) routes downstream operations to the Paymove Sandbox (`pay.sandbox.paymove.io` / `go.sandbox.paymove.io`). A merchant key is not required for public catalog discovery.
- **DTO Wrapping:** Tools using a request DTO take a top-level `request` object matching the schema below; tools with direct `@ToolParam` parameters (`search-public-products`, `list-partner-products`, `go-get-product`, `parking-get-pricing`) take parameters directly at the root of `arguments`.

---

## Category 1: Pay / DocPay & Payment Links (`7 tools`)

### 2. `create-pay-product`

Creates a new payment-link product (`PAY`) with initial pricing and returns a shareable payment link (`https://pay.paymove.io/{productId}`, or `https://pay.sandbox.paymove.io/{productId}` in sandbox). Suitable for services, professional fees, bills, tips, donations, and logistics settlements.

- **Service Class:** `PayToolService`
- **DTO:** `CreatePayProductRequest` (passed under `request`)
- **Auth Scope:** Partner (`X-API-KEY`)

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `name` | `string` | **Yes** | `@NotBlank` | Product name (e.g., `'Premium Subscription'`, `'Consulting Session'`). |
| `price` | `integer` (`long`) | **Yes** | `@NotNull`, `@PositiveOrZero` | Price in minor units (1/100 PLN), e.g., `1000` = 10.00 PLN. When `price > 0`, automatically creates the initial pricing entry; when `0`, creates only the parent `PAY` container (used when pricing lives on subproducts via `create-subproduct`). |
| `description` | `string` | No | Defaults to `name` | Payment description shown to the customer. |
| `location` | `string` | No | Default: `'Online'` | Location label for the product. |
| `customDetails` | `object` (`Map<String,String>`) | No | Specific item keys only | JSON object where keys are specific item names and values are formatted prices, e.g., `{"Bike": "10 PLN"}`. Do not use generic keys like `'product'` or `'price'`. |

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

- **Service Class:** `PayToolService`
- **DTO:** `CreateSubproductRequest` (passed under `request`)
- **Auth Scope:** Partner (`X-API-KEY`)

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `productId` | `string` | **Yes** | `@NotBlank` (UUID) | Parent `PAY` Product ID from `list-partner-products` or `create-pay-product`. |
| `externalId` | `string` | **Yes** | `@NotBlank` | Unique external identifier for this subproduct/order (e.g., `'ORD-123'`). |
| `amount` | `integer` (`long`) | **Yes** | `@NotNull`, `@Positive` (`> 0`) | Payment amount in minor units (1/100 PLN), e.g., `1000` = 10.00 PLN, `150000` = 1500.00 PLN. |
| `description` | `string` | **Yes** | `@NotBlank` | Payment description shown to the customer. |
| `returnUrl` | `string` | **Yes** | `@NotBlank` | URL to redirect the customer after payment completion. |
| `bankAccount` | `string` | No | Optional | Bank account IBAN for settlement. |
| `email` | `string` | No | Optional | Customer email address. |
| `locale` | `string` | No | Default: `'pl-PL'` | Customer interface locale. |
| `customDetails` | `object` (`Map<String,String>`) | No | Specific item keys only | JSON object where keys are item names and values are prices, e.g., `{"Bike": "10 PLN"}`. |

#### Response JSON

```json
{
  "redirectUrl": "https://pay.paymove.io/550e8400-e29b-41d4-a716-446655440000/ORD-123",
  "externalId": "ORD-123",
  "amount": 24900
}
```

---

### 4. `update-subproduct`

Updates the price of an existing subproduct (checkout) under a `PAY` product, identified by `productId` and `externalId`.

- **Service Class:** `PayToolService`
- **DTO:** `UpdateSubproductRequest` (passed under `request`)
- **Auth Scope:** Partner (`X-API-KEY`)

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `productId` | `string` | **Yes** | `@NotBlank` (UUID) | Parent `PAY` product ID. |
| `externalId` | `string` | **Yes** | `@NotBlank` | The `externalId` assigned when the subproduct was created. |
| `price` | `integer` (`long`) | **Yes** | `@NotNull`, `@PositiveOrZero` | New price in minor units (1/100 PLN), e.g., `150000` = 1500.00 PLN. |

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

Lists all pricing entries (price options) for an existing `PAY` product. Public catalog discovery: no merchant `X-API-KEY` is required.

- **Service Class:** `PayToolService`
- **DTO:** `ListPayPricingEntriesRequest` (passed under `request`)
- **Auth Scope:** Public (No API Key Required)

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `productId` | `string` | **Yes** | `@NotBlank` (UUID) | Product ID from `create-pay-product`. |

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

- **Service Class:** `PayToolService`
- **DTO:** `AddPayPricingEntryRequest` (passed under `request`)
- **Auth Scope:** Partner (`X-API-KEY`)

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `productId` | `string` | **Yes** | `@NotBlank` (UUID) | Product ID from `create-pay-product`. |
| `price` | `integer` (`long`) | **Yes** | `@NotNull`, `@PositiveOrZero` | Price in minor units (1/100 PLN), e.g., `1000` = 10.00 PLN. |
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

- **Service Class:** `PayToolService`
- **DTO:** `UpdatePayPricingEntryRequest` (passed under `request`)
- **Auth Scope:** Partner (`X-API-KEY`)

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `productId` | `string` | **Yes** | `@NotBlank` (UUID) | Product ID from `create-pay-product`. |
| `entryId` | `string` | **Yes** | `@NotBlank` (UUID) | Pricing entry ID from `list-pay-pricing-entries` or `add-pay-pricing-entry`. |
| `price` | `integer` (`long`) | No | `@PositiveOrZero` | New price in minor units (1/100 PLN), e.g., `1000` = 10.00 PLN. |
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

- **Service Class:** `PayToolService`
- **DTO:** `DeletePayPricingEntryRequest` (passed under `request`)
- **Auth Scope:** Partner (`X-API-KEY`)

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `productId` | `string` | **Yes** | `@NotBlank` (UUID) | Product ID from `create-pay-product`. |
| `entryId` | `string` | **Yes** | `@NotBlank` (UUID) | Pricing entry ID to delete. |

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

- **Service Class:** `GoToolService`
- **DTO:** `CreateGoProductRequest` (passed under `request`)
- **Auth Scope:** Partner (`X-API-KEY`)

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `name` | `string` | **Yes** | `@NotBlank` | Product display name (e.g., `'Zoo Wroclaw'`, `'Muzeum Narodowe'`). |
| `fullName` | `string` | **Yes** | `@NotBlank` | Full official name of the product. |
| `location` | `string` | **Yes** | `@NotBlank` | Location/city of the product (e.g., `'Wroclaw'`, `'Krakow'`). |
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

- **Service Class:** `GoToolService`
- **DTO:** `AddTicketOptionRequest` (passed under `request`)
- **Auth Scope:** Partner (`X-API-KEY`)

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `productId` | `string` | **Yes** | `@NotBlank` (UUID) | Product ID returned by `go-create-product`. |
| `title` | `string` | **Yes** | `@NotBlank` | Ticket title shown to the customer (e.g., `'Bilet normalny'`, `'Adult Ticket'`, `'VIP Pass'`). |
| `price` | `integer` (`long`) | **Yes** | `@NotNull`, `@PositiveOrZero` | Price in minor units (grosze), e.g., `1000` = 10.00 PLN, `2500` = 25.00 PLN. Pass `0` for a free ticket (`bilet bezpłatny`). |
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

- **Service Class:** `GoToolService`
- **DTO:** `UpdateTicketOptionRequest` (passed under `request`)
- **Auth Scope:** Partner (`X-API-KEY`)

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `productId` | `string` | **Yes** | `@NotBlank` (UUID) | Product ID. |
| `entryId` | `string` | **Yes** | `@NotBlank` (UUID) | Entry ID of the ticket option to update (use `go-get-product` to inspect existing `entryId`s). |
| `title` | `string` | No | Optional | New ticket title. |
| `price` | `integer` (`long`) | No | `@PositiveOrZero` | New price in minor units (grosze), e.g., `1500` = 15.00 PLN. |
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

- **Service Class:** `GoToolService`
- **DTO:** `DeleteTicketOptionRequest` (passed under `request`)
- **Auth Scope:** Partner (`X-API-KEY`)

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `productId` | `string` | **Yes** | `@NotBlank` (UUID) | Product ID. |
| `entryId` | `string` | **Yes** | `@NotBlank` (UUID) | Ticket option (`entryId`) to delete. |

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

- **Service Class:** `GoToolService`
- **DTO:** `UpdateGoProductToolRequest` (passed under `request`)
- **Auth Scope:** Partner (`X-API-KEY`)

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `productId` | `string` | **Yes** | `@NotBlank` (UUID) | Product ID to update. |
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

Fetches a `GO` product along with all its ticket options (`pricing.options`) and its public `productLink`. Public catalog discovery: no merchant `X-API-KEY` is required.

- **Service Class:** `GoToolService`
- **Auth Scope:** Public (No API Key Required)

#### Input Parameters (direct `@ToolParam`)

| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `productId` | `string` | **Yes** | — | Product ID (UUID). |
| `locale` | `string` | No | `'pl-PL'` | Locale for translations: `'pl-PL'`, `'en-US'`, `'de-DE'`, or `'uk-UA'`. |

#### Response JSON

Returns the full `GoProductDto` JSON object with `pricing.options` (including each ticket's `entryId`, `title`, `price`, `subtitle`, `detailedDescription`, `imageUrl`, `faq`, `details`) plus `"productLink": "https://go.paymove.io/{productId}"`.

---

### 15. `go-set-translations`

Sets multilingual translations for a `GO` product's ticket options in a specified locale.

- **Service Class:** `GoToolService`
- **DTO:** `SetTranslationsRequest` (passed under `request`)
- **Auth Scope:** Partner (`X-API-KEY`)

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `productId` | `string` | **Yes** | `@NotBlank` (UUID) | Product ID. |
| `locale` | `string` | **Yes** | `@NotBlank` | Target locale: `'pl-PL'`, `'en-US'`, `'de-DE'`, or `'uk-UA'`. |
| `translationsJson` | `string` | **Yes** | `@NotBlank` (JSON object string) | JSON object mapping indexed keys to translated strings (`0`-based ticket index): `title_{index}`, `subtitle_{index}`, `description_{index}`, `question_{entryIndex}_{faqIndex}`, `answer_{entryIndex}_{faqIndex}`. Example: `'{"title_0":"Adult Ticket","subtitle_0":"price","description_0":"Full access"}'`. |

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

- **Service Class:** `GoToolService`
- **DTO:** `GenerateImageToolRequest` (passed under `request`)
- **Auth Scope:** Partner (`X-API-KEY`)

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `prompt` | `string` | **Yes** | `@NotBlank` | Image description in English — concrete subject, mood, and composition; no text, logos, or prices. |
| `ticketIndex` | `integer` | **Yes** | `@NotNull`, `@Min(1)` | 1-based index of the ticket this image belongs to (`1` for the first ticket, `2` for the second, etc.). |
| `styleId` | `string` | No | Optional | Optional visual style ID (e.g., `'07'`). Use the same `styleId` across all tickets of a product for visual consistency. |

#### Response JSON (`GenerateImageToolResult`)

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

- **Service Class:** `ParkingToolService`
- **DTO:** `CreateParkingProductRequest` (passed under `request`)
- **Auth Scope:** Partner (`X-API-KEY`)

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `name` | `string` | **Yes** | `@NotBlank` | Parking display name (e.g., `'Parking Centrum'`, `'Strefa Parkowania A'`). |
| `fullName` | `string` | **Yes** | `@NotBlank` | Full official name of the parking lot. |
| `shortName` | `string` | **Yes** | `@NotBlank` | Unique URL slug (letters, numbers, hyphens only, e.g., `'parking-centrum-wroclaw'`). |
| `location` | `string` | **Yes** | `@NotBlank` | Location/city/address (e.g., `'Wroclaw, ul. Pilsudskiego 10'`). |
| `entriesJson` | `string` | **Yes** | `@NotBlank` (JSON) | Time-based tariff entries as a JSON object keyed by `"0"`, `"1"`, etc., where each entry has `order` (`int`), `cost` (in grosze, e.g. `500` = 5 PLN), `duration` (ISO-8601 duration: `PT15M`, `PT30M`, `PT1H`, `PT24H`), `repeatable` (`boolean` — usually `true` on the last entry), and `partialCost` (`boolean` — proportional charge for partial time). Example: `'{"0":{"order":0,"cost":100,"duration":"PT15M","repeatable":false,"partialCost":false},"1":{"order":1,"cost":300,"duration":"PT1H","repeatable":true,"partialCost":false}}'`. |
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

- **Service Class:** `ParkingToolService`
- **DTO:** `CreateParkingEventToolRequest` (passed under `request`)
- **Auth Scope:** Partner (`X-API-KEY`)

#### Input Parameters (`request`)

| Field | Type | Required | Constraints / Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `parkingId` | `string` | **Yes** | `@NotBlank` (UUID) | Parking UUID from `parking-create-product`. |
| `from` | `string` | **Yes** | `@NotBlank` (`yyyy-MM-ddTHH:mm:ss`) | Event start date/time in ISO-8601 local format (e.g., `'2026-11-15T16:00:00'`). |
| `to` | `string` | **Yes** | `@NotBlank` (`yyyy-MM-ddTHH:mm:ss`) | Event end date/time in ISO-8601 local format (e.g., `'2026-11-15T23:59:00'`). |
| `type` | `string` | **Yes** | `@NotBlank` | `'EVENT'` (special event pricing) or `'PRICING_CHANGE'` (temporary tariff change). |
| `name` | `string` | No | Optional | Event name (e.g., `'Concert at Stadium'`, `'Holiday Rate'`). |
| `notes` | `string` | No | Optional | Additional notes about the event. |
| `repeatEveryDay` | `boolean` | No | Default: `false` | Repeat this event daily. |
| `repeatEveryWeek` | `boolean` | No | Default: `false` | Repeat this event weekly. |
| `fixedCost` | `integer` (`long`) | No | Mutually exclusive with `entriesJson` | Flat-rate fee in grosze for the entire event (e.g., `3000` = 30.00 PLN). |
| `entriesJson` | `string` | No | Mutually exclusive with `fixedCost` | Custom time-based tariff entries JSON object for the event window. |
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

Retrieves the current pricing configuration (tariff entries, active hours, daily/weekly caps, subscriptions, free tickets, and scheduled events) for a parking lot. Public catalog discovery: no merchant `X-API-KEY` is required.

- **Service Class:** `ParkingToolService`
- **Auth Scope:** Public (No API Key Required)

#### Input Parameters (direct `@ToolParam`)

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `parkingIdOrShortName` | `string` | **Yes** | Parking UUID or URL `shortName`. |

#### Response JSON

Returns the full `ParkingGetPricingResponse` JSON object containing `entries`, `activeHours`, `maximumCostPerDay`, `maximumCostPerWeek`, `minimumCostPerDay`, `freeTimePerTicket`, `subscriptions`, `freeTickets`, and `events`.

---

## Category 4: Public Discovery & Partner Catalog (`2 tools`)

Anyone can discover purchasable Paymove products and open a checkout without a merchant API key. `search-public-products` finds tickets, services, and parking zones. Pricing for a result can be inspected with `go-get-product`, `list-pay-pricing-entries`, or `parking-get-pricing` (also public). `list-partner-products` stays partner-scoped.

### 20. `search-public-products`

Searches and lists publicly available Paymove products (`GO` tickets/events, `PAY` checkouts/services, `PARKING` zones) that anyone or any AI agent can purchase. Requires **no merchant API key**.

- **Service Class:** `GeneralToolService`
- **Auth Scope:** Public (No API Key Required)

#### Input Parameters (direct `@ToolParam`)

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `query` | `string` | No | Search phrase matched case-insensitively (`ILIKE`) against product `name`, `fullName`, `shortName`, or `location` (e.g., `"zoo"`, `"muzeum"`, `"lotnisko"`). |
| `location` | `string` | No | City or location filter (case-insensitive `ILIKE`, e.g., `"Gdańsk"`, `"Kraków"`, `"Rzeszów"`). |
| `productType` | `string` | No | Filter by product line: `'GO'`, `'PAY'`, or `'PARKING'`. Returns all active purchasable types when omitted. |

#### Response JSON

JSON array of active public products, plus `totalElements` and `totalPages`. Each product includes `productId`, `shortName`, `name`, `fullName`, `productType` (`GO` / `PAY` / `PARKING`), `location`, `timezone`, `currency`, and a direct purchase URL `productLink`:

- `GO` → `https://go.paymove.io/{shortName}`
- `PAY` → `https://pay.paymove.io/{shortName}`
- `PARKING` → `https://parking.paymove.io/{shortName}`

```json
{
  "totalElements": 1,
  "totalPages": 1,
  "products": [
    {
      "productId": "550e8400-e29b-41d4-a716-446655440000",
      "shortName": "zoo-gdansk",
      "name": "ZOO Gdańsk",
      "fullName": "Gdańskie ZOO",
      "productType": "GO",
      "location": "Gdańsk",
      "timezone": "Europe/Warsaw",
      "currency": "PLN",
      "productLink": "https://go.paymove.io/zoo-gdansk"
    }
  ]
}
```

---

### 1. `list-partner-products`

Lists existing products belonging to the authenticated partner filtered by canonical product type. Call this tool before creating sub-resources (such as a subproduct checkout under an existing `PAY` product) or when inspecting existing products.

- **Service Class:** `GeneralToolService`
- **Auth Scope:** Partner (`X-API-KEY`)

#### Input Parameters (direct `@ToolParam`)

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `productType` | `string` | **Yes** | Canonical product type for the current flow. Allowed values: `PAY`, `GO`, `PARKING` (case-insensitive). |

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

