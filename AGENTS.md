> ## Documentation Index
> Fetch the complete documentation index at: https://docs.paymove.io/llms.txt
> Use this file to discover all available pages before exploring further.

> ## Agent Instructions
> ## paymove integration rules for AI agents
>
> These rules are verified against the live API. Follow them exactly.
>
> 1. Amounts are INTEGERS in grosze (minor units). `1000` means 10.00 PLN. PLN is the only supported currency and there is no currency field in the API.
> 2. `price` must always be an integer in grosze. Never send a float. Compute it with `Math.round(pln * 100)`.
> 3. Authenticate with the `X-API-KEY` header. Never `Authorization: Bearer`. Sandbox keys start with `sk_test_`, production keys with `sk_live_`.
> 4. Server-side only. A call from a merchant page is rejected. Never put the key in frontend code.
> 5. Send only the documented request fields. Match the documented shape exactly.
> 6. When creating a payment, `externalId`, `price`, and `details.returnUrl` are required. Validate the body before sending it.
> 7. Always verify the `X-Paymove-Signature` header on incoming webhooks before trusting them: https://docs.paymove.io/en/webhook-signature.md
> 8. Errors are `{"status": <int>, "message": "<text>"}`. Branch on the HTTP status code rather than parsing `message` strings.
> 9. Do not send an `Idempotency-Key` header.
> 10. `externalId` must be unique per order. Updating an existing subproduct price requires `PATCH /api/pay/product/{productId}/subproduct/{externalId}` with `{"price": <int>}`.
> 11. Webhooks fire only on `COMPLETED` by default. Registering a webhook requires both `retries` and `expectedCode`. Use a positive `retries` value such as `3`. Delivery counts as successful when the HTTP status equals `expectedCode`.
> 12. Never fulfil an order on the `returnUrl` redirect. The checkout does not redirect there by itself: the customer has to click "back to shop", and inside the widget modal that redirect never happens. Fulfil only in the webhook handler, after verifying the signature.
> 13. Do not pin a version of `@paymove-io/sdk` - install the latest.
> 14. If the merchant has no `productId` yet, do not stop at a placeholder: ask for the API key, the `partnerId` and the shop name, propose defaults for `location` and `timezone` (`Europe/Warsaw`), offer the optional fields once, then create the product for them with `POST /api/product/pay` and take `productId` from `id` in the response. Do the same for the webhook: register it, then assign it to the product. Guided procedure: https://docs.paymove.io/skill.md (Steps 1-2).
> 15. Full documentation index: https://docs.paymove.io/llms.txt · Copy-paste quickstart: https://docs.paymove.io/en/quickstart.md · Agent skill: https://docs.paymove.io/skill.md
> 16. Paymove MCP (Streamable HTTP) primary endpoint: https://api.paymove.io/api/mcp (also https://mcp-api.paymove.io/mcp). Public catalog discovery (`search-public-products`) does not require `X-API-KEY`. Partner tools (including `go-get-product`, `parking-get-pricing`, `list-pay-pricing-entries`, and `list-partner-products`) require `X-API-KEY`.

# Integracja z agentami AI

> Jak skierować Cursor, Claude Code, Windsurf czy Lovable na dokumentację Paymove, żeby wdrożyły integrację samodzielnie.

Dokumentacja Paymove jest przygotowana tak, by mógł z niej korzystać nie tylko człowiek, ale i agent AI piszący kod. Poniżej znajdziesz gotowe sposoby, żeby z tego skorzystać.

Serwer MCP (Streamable HTTP) działa pod głównym adresem `https://api.paymove.io/api/mcp` (także `https://mcp-api.paymove.io/mcp`). Publiczne odkrywanie katalogu (`search-public-products`) nie wymaga klucza `X-API-KEY`. Narzędzia partnerskie (w tym `go-get-product`, `parking-get-pricing`, `list-pay-pricing-entries` i `list-partner-products`) wymagają `X-API-KEY`.

## Zanim odpalisz agenta

Agent napisze kod, ale nie utworzy konta ani nie wymyśli kluczy - te dane muszą być po Twojej stronie:

| Dana | Skąd ją masz |
| - | - |
| Klucz API (`sk_test_…` / `sk_live_…`) | [Panel Paymove](https://panel.paymove.io) |
| `productId` | UUID Twojego produktu (sklepu) - z Panelu. Nie masz jeszcze produktu? Agent utworzy go za Ciebie - zapyta tylko o nazwę sklepu i pola, które chcesz ustawić |
| `signingSecret` (`whsec_…`) | Odpowiedź na rejestrację webhooka - służy do weryfikacji `X-Paymove-Signature`. Agent zarejestruje webhook za Ciebie, jeśli podasz publiczny adres endpointu |
| `partnerId` | Nadaje Paymove. Potrzebny wyłącznie do utworzenia produktu i rejestracji webhooka, nigdy do tworzenia płatności. Nie masz go? Napisz na [integration@paymove.io](mailto:integration@paymove.io) |

Do tego jednorazowa konfiguracja - produkt, webhook i **przypisanie webhooka do produktu** - opisana w [Konfiguracji](https://docs.paymove.io/webhooks.md). Agent wykona ją za Ciebie: potrzebuje do tego klucza API i `partnerId`, o resztę zapyta. Pominięcie ostatniego kroku to najczęstsza wpadka: płatności działają, a powiadomienia nie przychodzą.

> [!NOTE]
>
> Agent, który dostał `skill.md`, sam poprosi o klucz API i zatrzyma się, dopóki go nie podasz - zamiast wstawiać zmyślone wartości do kodu. Jeśli nie masz jeszcze produktu albo webhooka, poprowadzi Cię przez ich utworzenie: w jednej wiadomości zapyta o nazwę sklepu i pozostałe wymagane pola, zaproponuje wartości domyślne, wymieni pola opcjonalne, pokaże żądanie do zatwierdzenia i sam je wyśle. `productId` i `signingSecret` odczyta z odpowiedzi API i zapisze w zmiennych środowiskowych.

## Najszybsza droga

Wklej swojemu agentowi ten adres:

```
https://docs.paymove.io/skill.md
```

To wszystko - bez żadnego zdania wyjaśniającego. Pod tym adresem leży kompletna procedura wdrożenia: jakie dane zebrać od Ciebie, jak utworzyć płatność, jak zweryfikować webhook i czego nie robić. Agent pobierze plik i wykona integrację.

> [!NOTE]
>
> Działa w Cursorze, Claude Code, Windsurfie, Lovable i wszędzie tam, gdzie agent potrafi pobrać adres URL.

## Trwała konfiguracja w projekcie

Jeśli chcesz, żeby agent pamiętał reguły Paymove przy każdym zadaniu, dodaj je raz do swojego repozytorium. Skopiuj zawartość:

```
https://docs.paymove.io/agents.md
```

i wklej do pliku `AGENTS.md`, `CLAUDE.md` albo `.cursor/rules/paymove.md` w swoim projekcie. Od tego momentu wystarczy polecenie w stylu „dodaj płatności" - agent sam sięgnie po właściwe reguły.

## Każda strona jako Markdown

Do dowolnego adresu w tej dokumentacji możesz dopisać `.md` i otrzymasz czysty Markdown, bez elementów interfejsu:

```
https://docs.paymove.io/rest-api.md
https://docs.paymove.io/en/webhook-signature.md
```

Ten sam efekt daje menu kontekstowe w prawym górnym rogu każdej strony - znajdziesz tam kopiowanie treści oraz otwarcie strony bezpośrednio w Claude, ChatGPT, Cursorze czy VS Code.

## Mapa dokumentacji dla modeli

| Adres | Zawartość |
| - | - |
| [`/llms.txt`](https://docs.paymove.io/llms.txt) | Spis wszystkich stron z opisami oraz zestaw reguł integracji. Dobry punkt startu, gdy agent ma sam zdecydować, co przeczytać |
| [`/llms-full.txt`](https://docs.paymove.io/llms-full.txt) | Cała dokumentacja w jednym pliku |
| [`/openapi.yaml`](https://docs.paymove.io/openapi.yaml) | Specyfikacja OpenAPI bramki płatniczej |
| [`/skill.md`](https://docs.paymove.io/skill.md) | Gotowa procedura wdrożenia krok po kroku |
| [`/agents.md`](https://docs.paymove.io/agents.md) | Krótki zestaw reguł do wklejenia w repozytorium |

## Reguły, na które agenci najczęściej się przewracają

Jeśli piszesz integrację samodzielnie albo sprawdzasz kod wygenerowany przez agenta, zwróć uwagę na te punkty:

1. **Kwoty to liczby całkowite w groszach.** `price` zawsze jest liczbą całkowitą. Nie wysyłaj float. Przeliczaj przez `Math.round(kwota * 100)`.
2. **Autoryzacja nagłówkiem `X-API-KEY`**, nie `Authorization: Bearer`.
3. **Tylko po stronie serwera.** Klucz nie może trafić do frontendu, a przeglądarka i tak nie przejdzie CORS.
4. **Zawsze weryfikuj `X-Paymove-Signature`** przed realizacją zamówienia.
5. **Nigdy nie realizuj zamówienia na `returnUrl`** - to tylko przekierowanie przeglądarki.
6. **Wysyłaj wyłącznie pola opisane w dokumentacji.** Przy tworzeniu płatności wymagane są `externalId`, `price` i `details.returnUrl`.
7. **`externalId` jest unikalne dla zamówienia.** Zmianę ceny istniejącego subproduktu wykonuje `PATCH`. Nie wysyłaj nagłówka `Idempotency-Key`. Przy rejestracji webhooka wymagane są `retries` i `expectedCode`.

Pełne uzasadnienie każdej z nich znajdziesz w [Kodach błędów](https://docs.paymove.io/errors.md) i [Weryfikacji podpisu](https://docs.paymove.io/webhook-signature.md).

## Zgłoś problem

Jeśli Twój agent wygenerował niedziałającą integrację mimo skorzystania z powyższych materiałów, napisz na [integration@paymove.io](mailto:integration@paymove.io) i dołącz użyty prompt. Traktujemy to jako błąd dokumentacji.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.