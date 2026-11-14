# Public purchase tools

These five tools are what `tools/list` returned from `https://api.paymove.io/api/mcp` without an API key on 14 November 2026. Schemas below match that response. The description an agent should follow is the one in [`mcp-agent-contract.json`](./mcp-agent-contract.json). The description currently served by the backend still asks for a BLIK code in the chat as the payment step. The process is in [`agent-payment.md`](./agent-payment.md).

Amounts are integers in grosze. `1000` = 10.00 PLN.

Partner catalog and management tools remain documented in [`tools.md`](./tools.md). They were not in this unauthenticated `tools/list`.

## `search-public-products`

Find a product. Keep `productLink` for payment outside the chat. Then load variants with the purchase tool that matches `productType`.

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `query` | string | No | Matches name, full name, short name, or location. |
| `location` | string | No | City or location, for example `Gdańsk`. |
| `productType` | string | No | `GO`, `PAY`, or `PARKING`. |
| `limit` | integer | No | 1–50. Default 20. |
| `page` | integer | No | Page starting at 0. Default 0. |

The response includes `count`, `totalElements`, `page`, `hasMore`, and `products`. A product includes `productId`, `name`, and, when set, `fullName`, `shortName`, `productType`, `location`, `currency`, and `productLink`.

`productLink` uses the short name: `https://go.paymove.io/{shortName}`, `https://pay.paymove.io/{shortName}`, or `https://park.paymove.io/{shortName}`.

## `go-purchase`

Arguments are a `request` object. `productIdOrShortName` is required.

| Field | Type | Description |
| :--- | :--- | :--- |
| `productIdOrShortName` | string | GO product id or short name from search. |
| `locale` | string | For example `pl-PL` or `en-US`. Default `pl-PL`. |
| `items` | array | Omit on the first call. Each item needs `pricingOptionId`. Optional: `quantity` (default 1), `eventId`, `termId`, `userDefinedAmount` (grosze, only when the option allows it). |
| `formData` | object | Answers keyed by the form field names the tool returned. |
| `email` | string | Buyer email. The ticket and the confirmation go there. Send it on the payment call, after the user confirmed the address. |
| `expectedTotal` | integer | The `expectedTotal` in grosze from the quote the user accepted. |
| `blikCode` | string | Six-digit BLIK code. Only on a platform that allows in-chat payment, and only in the call that starts the payment. |

First call, id only: stage `OPTIONS` with `name`, `merchant`, `options` (`pricingOptionId`, `title`, `price`, `priceFormatted`, …), `events`, `formFields`.

Second call, with `items` and without `blikCode`: stage `CONFIRM` with `merchant`, `itemsTotal`, `fee`, `expectedTotal`, `expectedTotalFormatted`, `missing`. There is no payment URL and no expiry field in that payload.

The call that starts an in-chat payment returns `orderId`, `status`, and `summaryLink`. The backend waits up to about 45 seconds for confirmation in the banking app.

## `pay-purchase`

Arguments are a `request` object. `productIdOrShortName` is required.

| Field | Type | Description |
| :--- | :--- | :--- |
| `productIdOrShortName` | string | PAY product id or short name from search. |
| `locale` | string | For example `pl-PL` or `en-US`. Default `pl-PL`. |
| `pricingOptionId` | string | Option the user picked. Omit to list options first. |
| `formData` | object | Answers keyed by the form field names the tool returned. |
| `email` | string | Buyer email. The confirmation goes there. |
| `expectedTotal` | integer | The `expectedTotal` in grosze from the quote the user accepted. |
| `blikCode` | string | Six-digit BLIK code. Only on a platform that allows in-chat payment, and only in the call that starts the payment. |

Each purchasable option carries `expectedTotal` (price plus service fee). Options with `availableInChat=false` are paid on `productLink` only.

## `parking-purchase`

Arguments are a `request` object. `productIdOrShortName` is required.

| Field | Type | Description |
| :--- | :--- | :--- |
| `productIdOrShortName` | string | PARKING product id or short name from search. |
| `plate` | string | Licence plate. The tool strips spaces and dashes. |
| `durationMinutes` | integer | Required for `STANDARD`. Ignored for `EXTERNAL_PRICING`. |
| `formData` | object | Answers keyed by the form field names the tool returned. |
| `email` | string | Buyer email. The confirmation goes there. |
| `expectedTotal` | integer | The `expectedTotal` in grosze from the quote the user accepted. |
| `blikCode` | string | Six-digit BLIK code. Only on a platform that allows in-chat payment, and only in the call that starts the payment. |

`STANDARD` is paid up front for a chosen time. `EXTERNAL_PRICING` is paid on exit and the amount depends on the plate. The quote returns `expectedTotal` including the fee, plus the ticket start and end.

## `get-payment-status`

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `productType` | string | Yes | `GO`, `PAY`, or `PARKING`. |
| `orderId` | string | Yes | `orderId` from the purchase tool. |
| `productId` | string | No | Needed for the GO and PAY summary link. |

`COMPLETED` means paid. `ERROR` or `CANCELED` means not paid. `PENDING`, `INITIALIZED`, or `WAITING_FOR_EXTERNAL_ACTION` means the user has not confirmed BLIK yet. The tool waits up to about 20 seconds. It also returns the summary link when it has one.
