#!/usr/bin/env python3
"""Check the colours and fonts of proteus-plotly against tokens.css.

``proteus_plotly.TOKENS`` must equal the ``:root`` values of
``tokens/tokens.css`` and ``proteus_plotly.LIGHT`` the ``[data-theme="light"]``
remaps, for every name it carries; every token it carries that the light block
remaps must be in ``LIGHT``, so no surface keeps its dark value by omission.
``MODULES`` must match the table in ``docs/module-colors.md``. The cycles
and domain colours must equal proteus-mpl's, which ``check_copies.py`` holds to the
tokens. Exits non-zero on any difference. Needs plotly installed.
"""

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path[:0] = [str(REPO / "tokens"), str(HERE / "src"), str(REPO / "figures" / "proteus-mpl" / "src")]

from check_cvd import _normalise_selector, _strip_comments, _top_level_rules  # noqa: E402
from check_sync import parse_css  # noqa: E402

import proteus_mpl  # noqa: E402  (its module level needs no matplotlib)
import proteus_plotly  # noqa: E402

LIGHT_SELECTOR = '[data-theme="light"]'
# | Interior | `--pt-dom-interior` | `#E23D28` | SPIDER, Aragog, Zalmoxis |
MODULE_ROW = re.compile(r"^\|[^|]+\| `--pt-(dom-[a-z]+)` \|[^|]+\|([^|]+)\|$", re.M)


def light_remaps(css):
    """Token name -> value declared in the top-level light block."""
    for prelude, body, _ in _top_level_rules(_strip_comments(css)):
        if _normalise_selector(prelude.strip()) == LIGHT_SELECTOR:
            pairs = (decl.split(":", 1) for decl in body.split(";") if decl.strip())
            return {name.strip()[len("--pt-"):]: " ".join(value.split()) for name, value in pairs}
    raise ValueError(f"tokens.css has no top-level {LIGHT_SELECTOR} block")


def problems(css, docs):
    dark = {name[len("pt-"):]: value for name, value in parse_css(css).items()}
    light = light_remaps(css)
    found = []
    for label, ours, theirs in (("TOKENS", proteus_plotly.TOKENS, dark),
                                ("LIGHT", proteus_plotly.LIGHT, light)):
        for name, value in ours.items():
            if name not in theirs:
                found.append(f"{label}['{name}']: no such token in that block of tokens.css")
            elif value.upper() != theirs[name].upper():
                found.append(f"{label}['{name}'] is {value}, tokens.css has {theirs[name]}")
    for name in sorted(set(proteus_plotly.TOKENS) & set(light) - set(proteus_plotly.LIGHT)):
        found.append(f"LIGHT lacks '{name}', which tokens.css remaps to {light[name]}")
    for domain, token in proteus_plotly.DOMAINS.items():
        if proteus_mpl.DOMAINS[domain] != dark[token]:
            found.append(f"DOMAINS['{domain}'] names {token}, proteus-mpl differs")
    by_token = {token: domain for domain, token in proteus_plotly.DOMAINS.items()}
    documented = {
        module.strip().lower(): by_token[token]
        for token, modules in MODULE_ROW.findall(docs)
        for module in modules.split(",")
    }
    if documented != proteus_plotly.MODULES:
        found.append(f"MODULES differs from docs/module-colors.md: {documented}")
    for label in ("CYCLE", "CYCLE_DARK"):
        if [c.upper() for c in getattr(proteus_plotly, label)] != getattr(proteus_mpl, label):
            found.append(f"{label} differs from proteus_mpl.{label}")
    return found


def main():
    found = problems(
        (REPO / "tokens" / "tokens.css").read_text(encoding="utf-8"),
        (REPO / "docs" / "module-colors.md").read_text(encoding="utf-8"),
    )
    for line in found:
        print(line)
    if found:
        return 1
    print(f"proteus-plotly matches tokens.css ({len(proteus_plotly.TOKENS)} tokens, "
          f"{len(proteus_plotly.LIGHT)} light remaps) and the proteus-mpl cycles")
    return 0


if __name__ == "__main__":
    sys.exit(main())
