#!/usr/bin/env python3
"""Check the agent payment contract and the docs that point at it.

This repository has no application build. The check is the test gate.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs" / "mcp-agent-contract.json"
PURCHASE_TOOLS = (
    "search-public-products",
    "go-purchase",
    "pay-purchase",
    "parking-purchase",
    "get-payment-status",
)

REQUIRED_INSTRUCTIONS = (
    "expectedTotal",
    "productLink",
    "ChatGPT",
    "get-payment-status",
    "same address",
    "BLIK",
    "pending",
    "grosze",
    "summaryLink",
)

REQUIRED_FILES = {
    "README.md": ("docs/agent-payment.md", "expectedTotal", "ChatGPT", "productLink"),
    "README.pl.md": ("docs/agent-payment.pl.md", "expectedTotal", "ChatGPT", "productLink", "Wysłać na ten sam adres?"),
    "SKILL.md": ("docs/agent-payment.md", "expectedTotal", "ChatGPT", "get-payment-status"),
    "AGENTS.md": ("docs/agent-payment.md", "expectedTotal", "ChatGPT", "get-payment-status", "same address"),
    "docs/agent-payment.md": ("mcp-agent-contract.json", "expectedTotal", "ChatGPT", "productLink", "same address"),
    "docs/agent-payment.pl.md": ("mcp-agent-contract.json", "expectedTotal", "ChatGPT", "productLink", "Wysłać na ten sam adres?"),
    "docs/purchase-tools.md": ("mcp-agent-contract.json", "expectedTotal", "blikCode", "get-payment-status"),
    "docs/tools.md": ("agent-payment.md", "purchase-tools.md", "expectedTotal"),
    "docs/catalog.md": ("agent-payment.md", "expectedTotal", "productLink"),
}


def fail(message: str) -> None:
    print(f"FAIL {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if not CONTRACT.is_file():
        fail(f"missing {CONTRACT}")
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    instructions = contract.get("initialize", {}).get("instructions", "")
    if not isinstance(instructions, str) or len(instructions) < 400:
        fail("initialize.instructions is missing or too short")
    for phrase in REQUIRED_INSTRUCTIONS:
        if phrase not in instructions:
            fail(f"initialize.instructions missing {phrase!r}")

    tools = contract.get("tools")
    if not isinstance(tools, dict):
        fail("tools must be an object")
    if tuple(tools) != PURCHASE_TOOLS:
        fail(f"tool keys are {tuple(tools)}, expected {PURCHASE_TOOLS}")
    for name, spec in tools.items():
        description = spec.get("description", "") if isinstance(spec, dict) else ""
        if not isinstance(description, str) or len(description) < 200:
            fail(f"{name} description is missing or too short")
        if name == "search-public-products":
            for phrase in ("productLink", "ChatGPT"):
                if phrase not in description:
                    fail(f"{name} description missing {phrase!r}")
        elif name == "get-payment-status":
            for phrase in ("COMPLETED", "PENDING", "summaryLink"):
                if phrase not in description:
                    fail(f"{name} description missing {phrase!r}")
        else:
            for phrase in ("expectedTotal", "productLink", "ChatGPT", "blikCode", "get-payment-status"):
                if phrase not in description:
                    fail(f"{name} description missing {phrase!r}")
            if "same address" not in description:
                fail(f"{name} description missing email reuse")

    for relative, phrases in REQUIRED_FILES.items():
        path = ROOT / relative
        if not path.is_file():
            fail(f"missing {relative}")
        text = path.read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                fail(f"{relative} missing {phrase!r}")

    server = json.loads((ROOT / "server.json").read_text(encoding="utf-8"))
    remote = server["remotes"][0]
    if remote.get("url") != "https://api.paymove.io/api/mcp":
        fail("server.json remote URL changed")
    if "instructions" in server:
        fail("server.json has no initialize instructions field in the registry schema")

    # Flag a real credential, not the public prefix names used in the integration guide.
    secret_pattern = re.compile(r"(?:sk_live_|sk_test_|whsec_)[A-Za-z0-9]{8,}")
    scanned = [CONTRACT, *[(ROOT / relative) for relative in REQUIRED_FILES]]
    for path in scanned:
        text = path.read_text(encoding="utf-8")
        match = secret_pattern.search(text)
        if match:
            fail(f"{path.relative_to(ROOT)} contains a credential-shaped value")

    print("ok: agent payment contract, docs, and server.json remote")
    print("build: no compile step; this repository is documentation and a registry manifest")


if __name__ == "__main__":
    main()
