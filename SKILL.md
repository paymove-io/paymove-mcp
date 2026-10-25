---
name: paymove-integration
description: A complete, step-by-step procedure for an AI agent implementing paymove checkout, Pay&Go, Parking, and MCP tools.
---

# paymove integration skill

You are implementing payments with **paymove**, a Polish payment gateway. Follow this procedure exactly. Everything here is verified against the live API.

## When to use this

Use this document whenever the task is to accept payments, add a checkout, integrate a payment gateway, or handle BLIK / Google Pay / Apple Pay in a project that uses paymove.

Not covered here: if the merchant has **no cart and no backend** and only wants to sell a product **already configured in paymove** (a service, a fundraiser, tickets, parking) on their website, they do not need this procedure, an API key or a webhook. Use the payment button (widget) instead - a single `<script src="…/v1/sdk.js" data-product-id="…">` tag: https://docs.paymove.io/en/app-widget.md

## How paymove works

1. Your **server** calls the paymove API to create a payment. You get back a `redirectUrl`.
2. You redirect the **customer** to that URL. paymove hosts the checkout page.
3. When the payment completes, paymove sends a **signed webhook** to your server.
4. You **verify the signature**, respond `200`, and only then fulfil the order.

The customer's return to your `returnUrl` is *not* proof of payment. The webhook is.

Before any of that can happen, the merchant's account needs a **product** (their store in paymove) and a **webhook assigned to it**. Steps 1 and 2 make you do that setup *for* the user: ask for the few values only they know, propose defaults for the rest, run the calls, and hand back the resulting IDs. Do not tell the user to "create a product in the panel" and stop.

## Facts you must not get wrong

1. **Amounts are integers in grosze** (minor units). `1000` = 10.00 PLN.
2. **A float `price` is silently truncated.** `12.99` becomes `12` grosze and the API still returns `200`. Always `Math.round(pln * 100)`.
3. **PLN only.** There is no currency field in the REST API. (The Node SDK requires a `currency` argument but the API ignores it - pass `"PLN"`.)
4. **Auth header is `X-API-KEY`.** Never `Authorization: Bearer`. Sandbox keys start `sk_test_`, production `sk_live_`.
5. **Server-side only.** A `fetch` from the merchant's page is rejected. Never put the key in frontend code.
6. **Unknown fields are silently ignored and still return `200`.** A wrong body shape looks like success. Match the documented shape exactly.
7. **A missing `externalId` returns `500 Something went wrong`**, not `400`. A missing `price` or `details.returnUrl` returns **`200`** and a usable `redirectUrl` - no error at all. Validate the body yourself before sending it.
8. **Errors are `{"status": <int>, "message": "<text>"}`.** Branch on the HTTP status only. Never parse `message` - it is unstable and leaks internal class names.
9. **No rate limiting, no `429`, no `422`, no `Idempotency-Key`, no API versioning.** Do not write code for them.
10. **Re-POSTing an existing `externalId` returns `200` with the ORIGINAL `redirectUrl`** and silently discards **every** field you send - price, description and details alike. Use a unique `externalId` per order.
11. **Webhooks fire only on `COMPLETED` by default.** `retries` and `expectedCode` are required when registering one - omitting either returns `500`, and `retries: 0` means no retry at all. Delivery succeeds when your HTTP status equals `expectedCode`; the response body is never inspected.
12. **Never fulfil an order in the `returnUrl` handler.** The checkout does not redirect there by itself - the customer has to click "back to shop", and it may never happen. Only fulfil after a verified webhook, idempotently.
13. **Do not pin a version of `@paymove-io/sdk`.**
14. **PayPo appears on the checkout only from `1000` grosze (10.00 PLN).** Below that the method is not shown at all - `details.triggerPayment: "PAYPO"` has nothing to preselect, and a widget `methods` list with `PAYPO` would advertise a method the customer cannot pick. Do not promise PayPo on smaller orders.
15. **Sandbox BLIK test code: any 6 digits starting with `777`** (`777123`, `777000`, …). The three leading sevens are what matters; the other three digits are arbitrary. Sandbox only - production needs a real code from the customer's banking app.

## Step 0 - Credentials and environment

Nothing below works without these. Ask the user and **stop until you have them**. Do not invent values, do not leave placeholders in committed code, do not guess a product ID or a `partnerId`.

Ask, in one message:

1. **Which environment** you are integrating against - sandbox or production. A key, a product and a webhook all belong to one environment: a `sk_test_…` key goes with the sandbox base URL, a `sk_live_…` key with the production one. A sandbox product ID does not exist in production.
2. **The API key.** The merchant generates it in the paymove panel - https://panel.paymove.io, section "API keys".
3. **Whether the merchant already has a product** - a `productId` (UUID) - and, if so, **whether a webhook is already registered and assigned to it**. The answers decide how much of Steps 1-2 you do. When in doubt, the user can check both in the panel.
4. **`partnerId`** - only if you are going to create the product or register the webhook. It is the UUID of the merchant's partner account, **assigned by paymove when the account was opened. It cannot be generated, and no API call returns it.** If the user does not have it: integration@paymove.io.

| Value | What it is | Where it comes from |
|---|---|---|
| `PAYMOVE_API_KEY` | The key sent in the `X-API-KEY` header. `sk_test_…` in sandbox, `sk_live_…` in production | The panel, section "API keys" |
| `PAYMOVE_PRODUCT_ID` | UUID of the merchant's store ("product") in paymove - it goes in the URL of every create-payment call | The panel if the product already exists; otherwise the `id` in the response of Step 1, which you run for the user |
| `PAYMOVE_WEBHOOK_SECRET` | The `whsec_…` secret used to verify `X-Paymove-Signature` | Field `signingSecret` in the response of Step 2, which you run for the user |
| `partnerId` | UUID of the merchant's partner account. Needed only for Steps 1-2, never for creating a payment | Handed over by paymove; not available through the API |

The first three go in environment variables. Never commit them and never expose them to the browser.

### Base URLs

| Environment | URL |
|---|---|
| Sandbox | `https://gateway-api.sandbox.paymove.io` |
| Production | `https://api.paymove.io` |

`{baseUrl}` below means the one that matches the key.

## Step 1 - Create the product (you do this for the user)

The product is the merchant's store in paymove. Every payment is created inside it, and its `id` is `PAYMOVE_PRODUCT_ID`. One product per environment, created once. Full reference: https://docs.paymove.io/en/webhooks.md

**Skip this step** if the user gave you an existing `productId` in Step 0. Never create a second product for a merchant who already has one, and never send this call twice: if you are not sure whether it went through, ask the user to look in the panel before retrying.

### 1a. Interview the user

Ask for everything in **one message**, as a numbered list with your proposed defaults already filled in, so the user can answer "ok" or correct a value. Do not ask about the optional fields one at a time, and do not invent a shop name or a domain.

Required - no call without them:

1. **`name`** - the shop name. The checkout shows it to the customer as the merchant they are paying (a single payment can override it with `details.recipient`). Use the trade name customers know, not a technical identifier. No default - the user has to tell you.
2. **`location`** - free text: a city or a country code (`Warszawa`, `PL`). Not shown to the customer. Propose the merchant's city, or `PL`.
3. **`timezone`** - an IANA name. Propose `Europe/Warsaw`; change it only if the user asks.

Optional - list them once, ask which (if any) the user wants, and leave the rest out of the body:

- **`shortName`** - a short display name (`SHOP1`).
- **`fullName`** - the full legal name of the company (`Merchant Shop Sp. z o.o.`). Included in the default webhook payload.
- **`metadata.locale`** - the default language of the checkout, an IETF tag such as `pl-PL` or `en-US`; the checkout is available in Polish, English, German and French. `pl-PL` when omitted, so ask only if the shop is not Polish.
- **`metadata.logoUrl`** - public HTTPS URL of the shop logo. The checkout shows it next to the shop name as a 34×34 px square (cropped to a square, so ask for a square image) and falls back to a generic icon if the image cannot be loaded. Worth offering explicitly: it is the one optional field customers actually see.
- **`metadata.merchantDomain`** - the shop's bare domain (`shop.example.com` - no scheme, port or path). Needed **only** for Apple Pay inside a widget modal on the merchant's site (the checkout widget or the [payment button widget](https://docs.paymove.io/en/app-widget/apple-pay.md)), and the domain must additionally be registered with Apple through integration@paymove.io. Skip it unless the user plans exactly that. Anything other than a bare domain is rejected with `400`.
- **`id`** - a UUID you choose instead of one generated by paymove. Only if the user wants a specific UUID; an `id` that already exists returns `400`.
- **`bankAccountDetails`** - the payout account for this product's payments: `{ "iban": "PL…", "holderName": "…", "nip": "…" }`. Only `iban` is required - `PL` followed by 26 digits, upper case, no spaces; the checksum is verified. The account is looked up by IBAN on the partner account and created if missing. It can only be set when the product is created (`PATCH` does not change it). It is **not** the account the customer pays into. Never invent or reuse an example IBAN - take it from the user or leave the field out.

Fixed, never asked: `partnerId` (from Step 0) and `productType: "PAY"`.

### 1b. Confirm and call

Show the user the exact JSON body you are about to send and wait for their go-ahead. Then run the call yourself if you can execute commands and the key is available in the environment; otherwise hand the user the complete command and ask them to paste the response back. Never write the key into the command as a literal.

```bash
curl --request POST \
  --url https://gateway-api.sandbox.paymove.io/api/product/pay \
  --header 'Content-Type: application/json' \
  --header "X-API-KEY: $PAYMOVE_API_KEY" \
  --data '{
    "partnerId": "78562c79-2f5c-4415-8af4-c871eea92ef2",
    "productType": "PAY",
    "name": "Sklep Testowy",
    "location": "Warszawa",
    "timezone": "Europe/Warsaw",
    "metadata": { "locale": "pl-PL" }
  }'
```

The response is `200` with the full product object. The only field you need is `id`:

```json
{
  "id": "891412c8-8717-4449-9543-e34112bec470",
  "name": "Sklep Testowy",
  "location": "Warszawa",
  "timezone": "Europe/Warsaw",
  "productType": "PAY",
  "status": "ACTIVE"
}
```

(abridged - the real response also carries `partner`, `shortName`, `fee` and timestamps)

### 1c. Save the result

- `id` → `PAYMOVE_PRODUCT_ID` in the environment (`.env`, not committed). Also tell the user the value in plain text - they will want it in the panel and when they go to production.
- Remember that the product now exists, so you do not create it again later in the conversation.

If the call fails, fix the cause. Do not retry blindly and do not guess other values:

| Response | Cause | What to do |
|---|---|---|
| `400` `merchantDomain must be a bare domain, e.g. shop.example.com` | `metadata.merchantDomain` contains a scheme, port or path | Send the bare host, or drop the field |
| `400` `Invalid IBAN` | `bankAccountDetails.iban` fails the checksum, has spaces or is too short | Ask the user to re-check the IBAN - full form, no spaces - or drop the field |
| `400` `Product with id <uuid> already exists` | The `id` you chose is taken | Drop `id` and let paymove generate one - or, if the user meant "this is my existing product", use that UUID as `PAYMOVE_PRODUCT_ID` and skip the call |
| `401` `Invalid API key` | Wrong key, or a key from the other environment | Match `sk_test_` with the sandbox URL and `sk_live_` with production |
| `401` `Missing access levels: […]` | The key has no write permission | Ask the user to generate a key with write access in the panel |
| `403` `Access denied` | `partnerId` in the body is not the partner the key belongs to | Ask the user to re-check `partnerId`. Never try other values |

## Step 2 - Register the webhook and assign it to the product (you do this for the user)

**Skip this step** only if the user confirmed in Step 0 that a webhook is registered **and assigned to this product**. Then ask for its `signingSecret`. A lost one can be re-read with `GET {baseUrl}/api/pay/plugin/webhook/{webhookId}` (field `signingSecret`) or replaced with `POST {baseUrl}/api/pay/plugin/webhook/{webhookId}/rotate-secret` - rotating invalidates the old secret.

Otherwise ask, in one message, for:

1. **The public URL of the webhook endpoint.** It must be reachable from the internet - locally that means a tunnel such as `ngrok`. Agree with the user on the route you will implement in Step 5 (for example `/api/payments/webhook`) and use that full URL here.
2. **`retries`** - propose `3`. `0` means a single delivery attempt and no retry at all.

Everything else has a fixed value - do not ask: `name: "OrderPaymentHook"`, `method: "POST"`, `expectedCode: 200`, `type: "PAYMENT"`, `headers: {"Content-Type": ["application/json"]}`. Leave `requestTemplate` out: without it paymove sends the full default payload (`externalId`, `orderId`, `status`, `price`, `paymentMethod`, …), which the handler in Step 5 expects.

Confirm the body with the user, then run the calls the same way as in Step 1.

**2a. Register** - `POST {baseUrl}/api/pay/plugin/webhook`

```json
{
  "name": "OrderPaymentHook",
  "endpoint": "https://your-shop.example/api/payments/webhook",
  "method": "POST",
  "expectedCode": 200,
  "retries": 3,
  "partnerId": "78562c79-2f5c-4415-8af4-c871eea92ef2",
  "type": "PAYMENT",
  "headers": { "Content-Type": ["application/json"] }
}
```

`expectedCode` and `retries` are **required - omitting either returns `500`**. The response carries `id` (the `webhookId`) and `signingSecret` (`whsec_…`) → `PAYMOVE_WEBHOOK_SECRET`. Save it to the environment now and tell the user where it went.

**2b. Assign** - `POST {baseUrl}/api/pay/plugin/webhook/{webhookId}/products/{productId}`, with the `X-API-KEY` header and no body. **Do not skip this.** Without it payments still work and no notification is ever delivered - the classic silent failure.

One more fact worth telling the user:

- Sandbox and production are separate. Going live means repeating Steps 1-2 with a `sk_live_…` key against `https://api.paymove.io`.

## There is an official SDK - use it on Node.js

paymove publishes an official JavaScript/TypeScript SDK on npm:

```bash
npm install @paymove-io/sdk
```

`@paymove-io/sdk` is MIT-licensed, has **zero runtime dependencies**, requires Node 18+, and ships both ESM and CommonJS builds with TypeScript types. On a Node or TypeScript project, prefer it over hand-written HTTP calls - it assembles the nested request body for you and surfaces typed errors.

On any other stack (Python, PHP, Go, Ruby, …) there is no official SDK yet - call the REST API directly, as shown in Step 3, Option B.

**What the SDK does not do:** it contains no webhook signature verification helper, and it does not create products or register webhooks. Steps 1, 2 and 5 are hand-written regardless of which option you pick.

## Step 3 - Create a payment

### Option A - the official Node SDK (preferred on Node/TypeScript)

```javascript
import { PaymoveClient, PaymoveApiError, PaymoveValidationError } from "@paymove-io/sdk";

const client = new PaymoveClient({
  apiKey: process.env.PAYMOVE_API_KEY,       // sk_test_… / sk_live_…
  productId: process.env.PAYMOVE_PRODUCT_ID,
  environment: "sandbox",                    // or "production"
});

try {
  const { redirectUrl } = await client.createPayment({
    amount: Math.round(amountPln * 100),     // integer grosze - never a float
    currency: "PLN",                         // required by the SDK, ignored by the API
    externalId: orderId,                     // unique per order
    returnUrl: "https://your-shop.example/payment/return",
    productName: "Sports T-shirt",
    email: customerEmail,                    // optional
  });
  return redirectUrl;
} catch (err) {
  if (err instanceof PaymoveValidationError) {
    // rejected locally before any request was sent; err.field names the parameter
  } else if (err instanceof PaymoveApiError) {
    // non-2xx from the API; err.statusCode and err.responseBody hold the original response
  }
  throw err;
}
```

SDK specifics that matter:

- Parameters are **flat**. The SDK builds the nested `{price, externalId, details:{…}}` body itself: `amount` → `price`, `returnUrl` → `details.redirectUrl`, `externalId` goes **both** top-level and into `details.orderId`, `description`, `bankAccount` and `nip` stay **top-level**, and every remaining key spreads into `details`.
- `currency` is **required by the SDK** even though the API ignores it. Always pass `"PLN"`.
- The SDK validates `amount` only as "a number greater than zero" - it does **not** check that it is an integer. `49.99` passes the SDK and is then truncated to 49 grosze by the API. Keep using `Math.round(pln * 100)`.
- Errors: `PaymoveValidationError` (local, has `.field`), `PaymoveApiError` (has `.statusCode`, `.responseBody`), `PaymoveNetworkError` (has `.cause`), all extending `PaymoveError`.
- The client takes no `baseUrl` override, no timeout and no retry options; `environment` selects the host.
- `merchantId` is a deprecated alias for `productId` - use `productId`.

### Option B - plain HTTP (any language)

`POST {baseUrl}/api/pay/product/{productId}/subproduct/pricing`

```javascript
async function createPayment({ orderId, amountPln, productName }) {
  const response = await fetch(
    `https://gateway-api.sandbox.paymove.io/api/pay/product/${process.env.PAYMOVE_PRODUCT_ID}/subproduct/pricing`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-API-KEY": process.env.PAYMOVE_API_KEY,
      },
      body: JSON.stringify({
        price: Math.round(amountPln * 100), // integer grosze - never a float
        externalId: orderId,               // unique per order
        details: {
          returnUrl: "https://your-shop.example/payment/return",
          productName,
        },
      }),
    }
  );

  if (!response.ok) {
    const error = await response.json(); // { status, message }
    throw new Error(`paymove ${response.status}: ${error.message}`);
  }

  return response.json(); // { redirectUrl }
}
```

Response is HTTP `200` (not `201`) with one field:

```json
{ "redirectUrl": "https://checkout.sandbox.paymove.io/{productId}?externalId=ec6RtwTZKb" }
```

**Important:** the `externalId` query parameter inside that URL (`ec6RtwTZKb`) is a 10-character hash generated by paymove - *not* the `externalId` you sent. Store it if you want to poll the payment status later.

Fields in `details` that the checkout actually reads: `returnUrl`, `redirectUrl`, `productName`, `email`, `locale`, `orderId`, `recipient`, `triggerPayment`, `qrStepEnabled`, `autoclose`. Anything else is stored but never displayed.

The amount must be computed **server-side**. Never accept a price from the browser.

Optional top-level `bankAccountDetails` (`{ iban, holderName, nip }`, only `iban` required) sends the payout of this one payment to a different account than the product's. The SDK equivalent is `bankAccount` - the IBAN alone as a string. If both are sent, `bankAccountDetails` wins; an invalid IBAN returns `400` and no payment is created; on a repeated `externalId` it is ignored. Add it only when the merchant asks for per-payment payout accounts - never with a made-up IBAN.

## Step 4 - Redirect the customer

```javascript
res.redirect(303, redirectUrl);
```

**The customer is not sent back automatically.** After a successful payment the checkout shows a confirmation screen with a "back to shop" button, and only a click on that button navigates to `details.returnUrl` - no query parameters are appended. A customer who closes the tab never reaches your `returnUrl` at all.

On the `returnUrl` page, show only a neutral "we are processing your payment" message. Do not mark the order paid there.

## Step 5 - Verify and acknowledge the webhook

paymove signs every webhook with HMAC-SHA256 and sends it in a single header:

```
X-Paymove-Signature: t=1708790400,v1=<base64>
```

The signature covers the string `"{timestamp}.{raw_body}"`. The HMAC key is the **full secret including the `whsec_` prefix**, as UTF-8 bytes - do not strip the prefix, do not base64-decode it. The output is standard base64 with padding, not hex.

```javascript
const express = require("express");
const crypto = require("crypto");

const app = express();

function verifyWebhook(secret, signatureHeader, rawBody) {
  if (!signatureHeader) return false;

  const [tPart, signature] = signatureHeader.split(",", 2);
  if (!tPart?.startsWith("t=") || !signature?.startsWith("v1=")) return false;

  const timestamp = tPart.slice(2);

  // Replay protection: reject anything older than 5 minutes
  const age = Math.abs(Math.floor(Date.now() / 1000) - Number(timestamp));
  if (!Number.isFinite(age) || age > 300) return false;

  const expected =
    "v1=" +
    crypto
      .createHmac("sha256", secret)
      .update(`${timestamp}.${rawBody}`, "utf8")
      .digest("base64");

  // timingSafeEqual throws when lengths differ - guard first
  if (expected.length !== signature.length) return false;
  return crypto.timingSafeEqual(Buffer.from(expected), Buffer.from(signature));
}

app.post(
  "/api/payments/webhook",
  express.raw({ type: "application/json" }), // MUST be the raw body
  async (req, res) => {
    const rawBody = req.body.toString("utf8");

    if (!verifyWebhook(process.env.PAYMOVE_WEBHOOK_SECRET, req.get("X-Paymove-Signature"), rawBody)) {
      return res.status(401).json({ error: "invalid signature" });
    }

    const event = JSON.parse(rawBody);

    // Acknowledge immediately - paymove applies no timeout to this call
    res.status(200).json({ status: "ok" });

    // Then fulfil, asynchronously and idempotently
    try {
      await fulfillOrderOnce(event.externalId ?? event.orderId);
    } catch (err) {
      console.error("fulfilment failed", err);
    }
  }
);
```

**The raw body matters.** If a JSON body parser runs first and the object is re-serialized, the signature will not match. Use `express.raw(...)` on this route, or `await request.text()` in Next.js route handlers.

The acknowledgement must have a status **exactly equal** to the webhook's `expectedCode` (`200` by default). The response body is never inspected - `expectedResponse` is stored on the webhook but not compared against what you return, so any body will do.

A `201` or `204` counts as a failure **and is not retried**: only 4xx, 5xx and network errors trigger the retry schedule, so a wrong 2xx loses the notification for good.

## Step 6 - Fulfil idempotently

```javascript
async function fulfillOrderOnce(orderId) {
  const order = await db.orders.findByExternalId(orderId);
  if (!order || order.status === "paid") return; // already handled - do nothing
  await db.orders.markPaid(orderId);
  // ship goods, send confirmation email, etc.
}
```

paymove may redeliver the same notification. Fulfilment must be safe to run twice.

## Step 7 - Test in sandbox

Run one payment end to end before you report the integration as done - or, if you cannot open a browser, hand the user these exact steps:

1. Create a payment with a `sk_test_…` key and open the `redirectUrl`.
2. On the checkout pick **BLIK** and enter any 6-digit code starting with `777`, e.g. `777123`. The three leading sevens are what matters; the remaining three digits can be anything.
3. Confirm that the webhook arrives, the signature verifies, and the order is fulfilled exactly once.

The test code works in sandbox only. To test PayPo, use a `price` of at least `1000` - below 10.00 PLN the method is not on the checkout.

## Optional - poll the status

Useful when the customer is back on `returnUrl` but the webhook has not arrived yet. Use the 10-character hash from `redirectUrl`:

```
GET https://pay-api.sandbox.paymove.io/api/payment/product/{productId}/subproduct/{paymentHash}/status
```

**This endpoint is on a different host** - `pay-api.sandbox.paymove.io` in sandbox, `pay-api.paymove.io` in production. It is *not* routed through the `gateway-api` / `api.paymove.io` host used for creating payments: that host answers with `404` and a plain-text `No route found for: GET …`, which is not even the usual `{status, message}` error shape.

Returns `{"status": "COMPLETED", "orderId": "..."}`. It needs no API key. Treat it as a supplement to the webhook, never a replacement.

Statuses: `INITIALIZED`, `PENDING`, `COMPLETED`, `CANCELED` (one L), `ERROR`, `REFUNDED`, `WAITING_FOR_EXTERNAL_ACTION`.

## Verification checklist

Before you report the integration as done, check each of these against the code you wrote:

- [ ] The API key came from the user. `PAYMOVE_PRODUCT_ID` came from the user or from `id` in the Step 1 response; `PAYMOVE_WEBHOOK_SECRET` from the user or from `signingSecret` in the Step 2 response. Nothing is a placeholder or a guessed value.
- [ ] The product was created at most once, and only because the user had none. Its `name` is the one the user gave, not one you made up.
- [ ] The webhook is registered **and assigned to the product** (`POST /api/pay/plugin/webhook/{webhookId}/products/{productId}`).
- [ ] The API key comes from an environment variable, not a literal, and appears nowhere in frontend code.
- [ ] Requests use the `X-API-KEY` header, not `Authorization: Bearer`.
- [ ] Every amount reaching `price` is an integer, produced by `Math.round(x * 100)` or already in grosze.
- [ ] No decimal literal is ever assigned to `price`.
- [ ] There is no `currency` field in the REST request body.
- [ ] `externalId` is unique per order.
- [ ] The webhook route captures the raw body before any JSON parsing.
- [ ] The signature is verified with HMAC-SHA256, `"{timestamp}.{body}"`, base64 output, full `whsec_` secret as the key.
- [ ] Signature comparison guards against differing lengths before `timingSafeEqual`.
- [ ] A timestamp older than 300 seconds is rejected.
- [ ] The handler responds with the status equal to the webhook's `expectedCode` (`200` by default) before doing slow work.
- [ ] Fulfilment happens in the webhook handler, not in the `returnUrl` handler.
- [ ] Fulfilment is idempotent.
- [ ] There is no code handling `429`, `422`, rate limits or `Idempotency-Key`.
- [ ] On a Node/TypeScript project, `@paymove-io/sdk` is used rather than hand-rolled HTTP calls.
- [ ] No `@paymove-io/sdk` version is pinned.
- [ ] A sandbox payment was run end to end with a BLIK code starting with `777`, or the user was given the steps from Step 7.

## Do not

- Do not invent or placeholder an API key, `productId` or `partnerId` - ask the user and wait.
- Do not send the user to the panel to create the product or the webhook - do it for them (Steps 1-2), asking only for the values they alone know.
- Do not create a product for a merchant who already has one, and do not send the create-product call twice.
- Do not use `Authorization: Bearer`.
- Do not call the API from the browser.
- Do not send `currency` in the REST body, or `amount` instead of `price`.
- Do not send a float as `price`.
- Do not fulfil an order on the `returnUrl` redirect.
- Do not trust an unverified webhook.
- Do not write retry logic for `429` - the API has no rate limiting.
- Do not send an `Idempotency-Key` header - it does not exist.
- Do not branch on the `message` text of an error.
- Do not reuse an `externalId` to change a price; call `PATCH /api/pay/product/{productId}/subproduct/{externalId}` with `{"price": <int>}` instead.

## Deeper reading

- Setup - product, webhook, assignment: https://docs.paymove.io/en/webhooks.md
- Quickstart: https://docs.paymove.io/en/quickstart.md
- REST API: https://docs.paymove.io/en/rest-api.md
- Webhook signature: https://docs.paymove.io/en/webhook-signature.md
- Payment statuses: https://docs.paymove.io/en/payment-status.md
- Errors: https://docs.paymove.io/en/errors.md
- Payment methods, PayPo minimum, sandbox BLIK code: https://docs.paymove.io/en/payment-methods.md
- Node SDK: https://docs.paymove.io/en/sdk/javascript.md
- Full index: https://docs.paymove.io/llms.txt

If something does not work as documented, tell the user to write to integration@paymove.io with the prompt used - paymove treats that as a documentation bug.
