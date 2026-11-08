# Planned MCP examples

> **Status: Planned / Planowane.** These files are sample arguments for tools that are **not** on the server. Do not send them to `https://api.paymove.io/api/mcp` until each tool name appears in `tools/list`.

Names (`Atelier Nici`, `Festiwal Światła nad Odrą`, `Parking Bulwar Przykładowy`, `Biuro Przekładu Lipowa`, `Przychodnia na Lipowej`) are synthetic. UUIDs are documentation placeholders. `whsec_example_not_a_real_secret` is not a secret. Amounts are illustrative grosze.

The contract is [docs/tools.md](../../docs/tools.md#planned-tools). Sequences are in [docs/use-cases.md](../../docs/use-cases.md) and [docs/use-cases.pl.md](../../docs/use-cases.pl.md).

| File | Offer | Product type |
| :--- | :--- | :--- |
| `event-tickets.json` | Timed tickets with a seat count | `GO` |
| `parking-tariff.json` | Base-tariff edit | `PARKING` |
| `undated-service.json` | A fee with no clock time | `PAY` |
| `hairdresser.json` | Appointment slots | `PAY` |
| `visit.json` | Appointment slots | `PAY` |
| `webhooks.json` | Register, assign, list | any |
| `visibility.json` | Public or hidden | any |
