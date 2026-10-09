"""Stacked bars of time per module, one figure per surface.

    python examples/modules.py

Writes modules_light.html and modules_dark.html into the script's directory.
Aragog and Zalmoxis share the interior colour; Zalmoxis is hatched.
"""

from pathlib import Path

import plotly.graph_objects as go

import proteus_plotly

HERE = Path(__file__).parent
SECONDS = {  # module -> seconds per iteration
    "aragog": [3.5, 3.6, 3.4, 3.5],
    "zalmoxis": [0.0, 0.0, 140.0, 0.0],
    "agni": [780.0, 15.0, 15.2, 14.9],
    "calliope": [1.0, 1.1, 1.0, 1.0],
}


def render(theme: str, path: Path) -> None:
    markers = proteus_plotly.module_markers(SECONDS, theme)
    fig = go.Figure(
        [go.Bar(x=[1, 2, 3, 4], y=y, name=module, marker=markers[module])
         for module, y in SECONDS.items()],
        layout={"template": proteus_plotly.TEMPLATES[theme], "barmode": "stack",
                "title": f"time per iteration, {theme}",
                "xaxis_title": "iteration", "yaxis_title": "time [s]"},
    )
    fig.write_html(path, include_plotlyjs="cdn")


if __name__ == "__main__":
    for theme in ("light", "dark"):
        out = HERE / f"modules_{theme}.html"
        render(theme, out)
        print(f"wrote {out}")
