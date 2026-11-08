# Partner offers on the Paymove MCP — use-case guide

> **Live tools: 20. Planned tools: 11, status Planned / Planowane.** Sequences below mix both. A step marked **Live** is on `tools/list` today. A step marked **Planned** is specified in [tools.md](./tools.md#planned-tools) and must not be called until that name appears in `tools/list`. Polish version: [use-cases.pl.md](./use-cases.pl.md).

A new partner product is always `PAY`, `GO`, or `PARKING`. KYC is finished by a person in [panel.paymove.io](https://panel.paymove.io). No tool in this guide submits KYC, and none of the names below are real businesses.

Amounts are integers in grosze. `8000` means 80.00 PLN. Authentication is `X-API-KEY`. Sandbox calls also send `X-SANDBOX-API-KEY` (`sk_test_...`).

## Pick a product type

| The partner wants | Product type | Create with (live) | Then |
| :--- | :--- | :--- | :--- |
| Event tickets, a workshop, timed entry with a capacity | `GO` | `go-create-product`, `go-add-ticket-option` | **Planned** `set-availability` on the ticket `entryId` when each session has a seat count. Webhook + visibility. |
| A parking zone and its tariff | `PARKING` | `parking-create-product` | **Planned** `parking-update-pricing` to edit the base tariff later. `parking-create-event` (live) for a temporary override. No slots. |
| A service with no date (a fee, a package, a one-off job) | `PAY` | `create-pay-product`, `add-pay-pricing-entry` | No availability. Tracked checkout uses live `create-subproduct`. |
| An appointment book (hairdresser, a visit, any service that occupies a person and a clock time) | `PAY` | `create-pay-product` with `price: 0`, then one `add-pay-pricing-entry` per service | **Planned** `set-availability` on that entry. **Planned** `create-reservation` holds the seat and returns the checkout URL. |

Do not add a product type. Do not call a second create tool for appointments or for services. `create-pay-product` is the create tool for both.

## What to collect first

Ask once, then stop until the partner answers:

1. Environment: sandbox (`sk_test_...`) or production (`sk_live_...`).
2. `X-API-KEY` from the panel. Never invent one.
3. `partnerId` when a product or a webhook must be created. Paymove assigns it. No API returns it.
4. Shop or venue name, city, and timezone. Propose `Europe/Warsaw`.
5. Which row of the table above matches the offer.
6. For each sellable unit: the name and the price in grosze.
7. For tickets and appointments: the sessions (`start`, `end`, `capacity`, optional `resource`).
8. A public `https` webhook URL, if the partner wants payment notifications. Propose `retries: 3` and `expectedCode: 200`.

`signingSecret` comes back from webhook registration. Store it. Verify `X-Paymove-Signature` before fulfilling. Fulfil only on `COMPLETED`. A `returnUrl` visit is not payment.

## 1. Event tickets — `GO`

**Synthetic venue:** Festiwal Światła nad Odrą, Wrocław. Two tiers. The evening session on 20 November 2026 has 120 seats on the full-price tier.

| Step | Tool | Status | What happens |
| :--- | :--- | :--- | :--- |
| 1 | `go-create-product` | Live | `name` / `fullName`: `Festiwal Światła nad Odrą`. `location`: `Wrocław`. `shortName`: `festiwal-swiatla-nad-odra`. Save `productId`. |
| 2 | `go-add-ticket-option` | Live | `title`: `Bilet normalny`, `price`: `4500` (45.00 PLN). Save `entryId`. Repeat for `Bilet ulgowy` at `3000`. |
| 3 | `set-availability` | Planned | `targetType`: `GO_TICKET`, that `entryId`, one slot `2026-11-20T18:00:00`–`2026-11-20T21:00:00`, `capacity`: `120`, `timezone`: `Europe/Warsaw`. |
| 4 | `register-webhook`, then `assign-webhook-to-product` | Planned (REST is live today) | Register, store `signingSecret`, assign to this `productId`. |
| 5 | `set-product-visibility` | Planned | `visibility`: `public` after the price list is ready. Listing still requires `ACTIVE` and KYC. |
| 6 | `search-public-products` | Live | A buyer agent finds the festival by name or `location`. |
| 7 | `list-availability` | Planned, public read | Returns `remaining` for the evening. No API key when the product is searchable. |
| 8 | `create-reservation` | Planned | `quantity`: `2`, `externalId`: `FEST-2001`, `returnUrl`: the partner's https URL. No `price`. Response `status`: `HELD`, `price`: `9000`, `redirectUrl`. |
| 9 | Customer pays on `redirectUrl` | Live checkout | The partner does not mark the order paid on `returnUrl`. |
| 10 | Webhook `COMPLETED` | Live delivery, once the webhook exists | Verify the signature. `get-reservation` then reports `confirmed: true`. Issue the tickets in that handler, idempotently. |

Payloads: [examples/planned/event-tickets.json](../examples/planned/event-tickets.json).

Two buyers taking the last seats: one `create-reservation` returns `HELD`, the other returns `409` `SLOT_FULL`. The same `externalId` sent again returns the original `reservationId` and does not take two more seats.

## 2. Parking — `PARKING`

**Synthetic zone:** Parking Bulwar Przykładowy, Toruń. Duration tariff, not a calendar of slots.

| Step | Tool | Status | What happens |
| :--- | :--- | :--- | :--- |
| 1 | `parking-create-product` | Live | `name`: `Parking Bulwar Przykładowy`. `shortName`: `parking-bulwar-przykladowy`. `location`: `Toruń, bulwar Przykładowy 1`. `timezone`: `Europe/Warsaw`. `entriesJson` in the canonical map: 30 minutes for `200` grosze, then `500` grosze per hour, last bracket `repeatable: true`. |
| 2 | `parking-get-pricing` | Live | Read the stored tariff before any edit. |
| 3 | `parking-update-pricing` | Planned | Send the full canonical map again with the new `cost` values. Shorthand arrays are rejected. Event overrides are left in place. |
| 4 | `parking-create-event` | Live | A Saturday flat rate, `fixedCost` in grosze, `type`: `EVENT`. This is a temporary override, not a base-tariff edit. |
| 5 | `set-product-visibility` | Planned | `public` when the zone should appear in search. |

Do not attach `set-availability` to a parking. A parking stay is a duration, priced by the tariff.

Payloads: [examples/planned/parking-tariff.json](../examples/planned/parking-tariff.json).

## 3. Service without a date — `PAY`

**Synthetic shop:** Biuro Przekładu Lipowa, Poznań. The customer pays for a page of translation. There is no slot and no staff member to reserve.

| Step | Tool | Status | What happens |
| :--- | :--- | :--- | :--- |
| 1 | `create-pay-product` | Live | `name`: `Biuro Przekładu Lipowa`. `price`: `0` so the container has no single price. `location`: `Poznań`. |
| 2 | `add-pay-pricing-entry` | Live | `price`: `6000` (60.00 PLN), `description`: `Tłumaczenie — jedna strona`. Save `entryId`. Add further entries for rush service if needed. |
| 3 | `create-subproduct` | Live | When the order needs an `externalId`: `amount` is the entry price times the page count, computed on the partner's server, `returnUrl` set. The customer pays on `redirectUrl`. |
| 4 | Webhook | Planned MCP, live REST | Assign a webhook. Fulfil the translation job only after a verified `COMPLETED`. |
| 5 | `set-product-visibility` | Planned | `public` if the pay link should be discoverable. `hidden` if only direct orders should exist. |

Skip `set-availability` and `create-reservation`. There is nothing to double-sell on a clock.

Payloads: [examples/planned/undated-service.json](../examples/planned/undated-service.json).

## 4. Hairdresser — `PAY` plus slots

**Synthetic salon:** Atelier Nici, Sopot. Service: strzyżenie damskie, 30 minutes, `8000` grosze. One chair label, `stylist-a`. The label is the partner's own string, not a verified identity.

| Step | Tool | Status | What happens |
| :--- | :--- | :--- | :--- |
| 1 | `list-partner-products` | Live | `productType`: `PAY`. Reuse an existing product when one already fits. |
| 2 | `create-pay-product` | Live | Only if none exists. `name`: `Atelier Nici`. `price`: `0`. `location`: `Sopot`. |
| 3 | `add-pay-pricing-entry` | Live | `description`: `Strzyżenie damskie 30 min`, `price`: `8000`. Save `entryId`. |
| 4 | `set-availability` | Planned | `targetType`: `PAY_ENTRY`. Slots `10:00–10:30` and `10:30–11:00` on `2026-11-20`, `capacity`: `1`, `resource`: `stylist-a`, `timezone`: `Europe/Warsaw`. |
| 5 | `register-webhook` + `assign-webhook-to-product` | Planned (REST live) | The salon must have this before opening the book. Confirmation is the webhook. |
| 6 | `set-product-visibility` | Planned | `public` so `search-public-products` can return the salon after KYC. |
| 7 | `list-availability` | Planned | The buyer sees `remaining: 1` on `10:00`. |
| 8 | `create-reservation` | Planned | `externalId`: `APT-1001`, `quantity`: `1`, `returnUrl` set, no price field. Response `price`: `8000`, `status`: `HELD`, `ttlSeconds`: `600`, `redirectUrl`. |
| 9 | Payment | Live checkout | Customer pays before `expiresAt`. |
| 10 | Webhook `COMPLETED` | Live delivery | Salon writes the appointment in its own calendar inside the verified handler. `get-reservation` shows `confirmed: true`. |

`cancel-reservation` while `HELD` returns the seat. It does not refund a `COMPLETED` visit. A second customer asking for `stylist-a` at `10:00` after the hold receives `409` `SLOT_FULL`. Overlapping `stylist-a` on a different service of the same product is `409` `SLOT_OVERLAP` at `set-availability` time.

Payloads: [examples/planned/hairdresser.json](../examples/planned/hairdresser.json).

## 5. Visit — `PAY` plus slots

**Synthetic practice:** Przychodnia na Lipowej, Lublin. A 20-minute visit at `12000` grosze (120.00 PLN). Resource label `room-1`. This is a booking example. It is not medical advice, and it does not create a patient record.

The tool sequence is the hairdresser sequence with different copy:

- Product name `Przychodnia na Lipowej`, `location` `Lublin`, `price` `0` on the container.
- Pricing entry `Wizyta 20 min`, `price` `12000`.
- Slots of 20 minutes, `capacity` `1`, `resource` `room-1`.
- `externalId` `VIS-3001`.
- The same hold, the same server-side price, the same rule: the visit is confirmed only after the payment webhook `COMPLETED`.

Payloads: [examples/planned/visit.json](../examples/planned/visit.json).

## Rules that apply to every booked offer

- The caller never sends the price of a reservation. The server copies it from the entry.
- `externalId` is the idempotency key. One id, one hold.
- Default hold length in this draft is 600 seconds. The seat cannot be sold twice while the hold is `HELD` or the reservation is `COMPLETED`.
- `HELD` is not a confirmation. `returnUrl` is not a confirmation. `COMPLETED` on the verified payment webhook is the confirmation.
- Register the webhook and assign it to the product or the partner's system will not hear about that confirmation. REST can do this today. The MCP tools `register-webhook` and `assign-webhook-to-product` cannot, until they are listed.
- `search-public-products` is documented, once visibility ships, to return only `ACTIVE` products with visibility `public` whose partner has finished KYC. Hidden products remain on partner tools.

## Open questions for the product owner

These are unspecified on purpose. The draft picks a proposed value so implementers have one behavior to review.

| Topic | Proposed in this draft | Question |
| :--- | :--- | :--- |
| Default TTL | `600` seconds. Caller may send `60`–`900`. | What is the default, and may the partner change it? |
| Late payment | A `COMPLETED` payment after `EXPIRED` does not confirm the seat. | Who refunds that payment, and within what grace period? |
| Cancellation | `cancel-reservation` releases a `HELD` seat only. `COMPLETED` returns `409` and does not refund. | What is the cancellation window, and does a refund put the seat back? |
| Who confirms | The server sets `COMPLETED` from the payment. The partner fulfils in the webhook handler. No manual confirm tool. | Should the partner, or the staff member, confirm as well? |
| Limits | Not set. | Max slots per call, max days ahead, max `capacity`, max holds per `externalId` prefix, rate limits. |
| Webhook `type` | Example uses `PAYMENT`, which live REST marks deprecated in favor of `TRANSACTION`. | Which type should MCP send? |
| Zero price | `PRICE_NOT_FIXED`, no hold. | How does a free ticket with a capacity work? |
| Who may reserve | `create-reservation` requires the partner key. | Should a public agent be able to hold a searchable slot? |
| New product visibility | Not changed on the live create tools. | Once the flag exists, do new products start `hidden`? |
| Resource scope | A resource label is unique per product, across entries. | Should the same label block slots across two products of one partner? |
| `retries: 0` | MCP draft requires `retries` ≥ 1. REST allows `0`. | Should MCP allow a webhook that never retries? |
