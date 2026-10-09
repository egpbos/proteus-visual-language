"""proteus_plotly: PROTEUS Thermocline theme for Plotly.

Usage:
    import proteus_plotly
    proteus_plotly.use()          # light: Paper background
    proteus_plotly.use("dark")    # dark: Void background
    fig.update_layout(template="proteus_dark")   # or per figure

Importing the package registers the ``proteus`` and ``proteus_dark`` templates
in ``plotly.io.templates``. Colours are available by token name in TOKENS (the
dark-first values of tokens.css) and LIGHT (its light-theme remaps), through
``colors(theme)``; the categorical cycles as CYCLE and CYCLE_DARK, the module
domain colours as DOMAINS, the status colours as STATUS (token names), and bar markers that
keep two modules of one domain apart through ``module_markers``.
"""

import plotly.graph_objects as go
import plotly.io as pio

__version__ = "0.1.0"

# tokens.css by token name without the --pt- prefix: the :root value, and the
# [data-theme="light"] remap where there is one. check_tokens.py compares both.
TOKENS = {
    "magma": "#E23D28",
    "ocean": "#1B6FA8",
    "azure": "#4FA3D9",
    "ice": "#A8D4E8",
    "solar": "#E0A32E",
    "verdant": "#57A05C",
    "void": "#05070B",
    "basalt": "#0E131B",
    "basalt-2": "#12202E",
    "line-d": "#1A2230",
    "text-d": "#E9EEF2",
    "text-d2": "#9FB0BE",
    "text-d3": "#5A6B7A",
    "paper": "#F2F5F7",
    "ink": "#10151B",
    "ink-3": "#7A8894",
    "dom-interior": "#E23D28",
    "dom-outgassing": "#A03123",
    "dom-tidal": "#593E74",
    "dom-chem": "#1B6FA8",
    "dom-atmos": "#4FA3D9",
    "dom-stellar": "#E0A32E",
    "dom-accretion": "#A38F7A",
    "positive": "#2E8B57",
    "warning": "#C77726",
    "danger": "#C2362B",
    "info": "#1B6FA8",
    "font-body": '"Instrument Sans", "Helvetica Neue", Helvetica, Arial, sans-serif',
    "font-mono": '"Spline Sans Mono", ui-monospace, "SF Mono", Menlo, monospace',
}
LIGHT = {
    "void": "#F2F5F7",
    "basalt": "#FDFDFE",
    "basalt-2": "#E3E9EE",
    "line-d": "#D2DAE1",
    "text-d": "#10151B",
    "text-d2": "#3E4A55",
    "text-d3": "#7A8894",
    "azure": "#1B6FA8",
    "ice": "#14406B",
    "solar": "#C8860F",
    "dom-stellar": "#C8860F",
}

# domain -> token, and module -> domain (docs/module-colors.md)
DOMAINS = {
    "interior": "dom-interior",
    "outgassing": "dom-outgassing",
    "tidal": "dom-tidal",
    "chemistry": "dom-chem",
    "atmosphere": "dom-atmos",
    "stellar": "dom-stellar",
    "accretion": "dom-accretion",
}
MODULES = {
    "spider": "interior",
    "aragog": "interior",
    "zalmoxis": "interior",
    "calliope": "outgassing",
    "atmodeller": "outgassing",
    "lovepy": "tidal",
    "obliqua": "tidal",
    "vulcan": "chemistry",
    "zephyrus": "chemistry",
    "agni": "atmosphere",
    "janus": "atmosphere",
    "mors": "stellar",
    "morrigan": "accretion",
}
STATUS = ("positive", "warning", "danger", "info")  # token names

# The proteus-mpl cycles, neutral-first; two dark stops are standalone values there.
CYCLE = [
    TOKENS[name]
    for name in ("ink", "magma", "solar", "verdant", "ocean", "dom-tidal",
                 "dom-outgassing", "ink-3", "azure")
]
CYCLE_DARK = [TOKENS["paper"], TOKENS["magma"], TOKENS["solar"], "#57C08A",
              TOKENS["ice"], "#9B7BBE"]

# Second cue for the second, third, ... module of one domain
HATCHES = ("", "/", "\\", "x")


def colors(theme="light"):
    """Token name -> colour on one surface.

    Parameters
    ----------
    theme : {"light", "dark"}
        Surface; "light" applies the light-theme remaps of tokens.css.

    Returns
    -------
    dict of str to str
    """
    if theme not in ("light", "dark"):
        raise ValueError(f"theme must be 'light' or 'dark', got {theme!r}")
    return TOKENS | LIGHT if theme == "light" else dict(TOKENS)


def module_markers(modules, theme="light"):
    """Bar markers for modules drawn together.

    Every module takes its domain colour. The first module of a domain in
    ``modules`` is plain and each further one is hatched, so Aragog and
    Zalmoxis (both interior) stay apart without a second hue.

    Parameters
    ----------
    modules : iterable of str
        Module names, case-insensitive, in the order that decides which one
        stays plain.
    theme : {"light", "dark"}

    Returns
    -------
    dict of str to dict
        Module name as given -> ``marker`` for a ``go.Bar``.
    """
    palette = colors(theme)
    seen = {}
    markers = {}
    for module in modules:
        domain = MODULES[module.lower()]
        rank = seen[domain] = seen.get(domain, -1) + 1
        markers[module] = {
            "color": palette[DOMAINS[domain]],
            "line": {"color": palette["void"], "width": 1},
            "pattern": {"shape": HATCHES[rank], "fillmode": "overlay",
                        "fgcolor": TOKENS["paper"], "fgopacity": 0.7, "size": 6,
                        "solidity": 0.25},
        }
    return markers


def template(theme="light"):
    """The Plotly template for one surface: fonts, surfaces, axes and the cycle."""
    c = colors(theme)
    axis = {
        "showline": True,
        "linecolor": c["text-d"],
        "ticks": "outside",
        "tickcolor": c["text-d"],
        "tickfont": {"color": c["text-d2"]},
        "gridcolor": c["line-d"],
        "zerolinecolor": c["line-d"],
        "title": {"font": {"color": c["text-d"]}},
        "automargin": True,
    }
    return go.layout.Template(layout={
        "font": {"family": TOKENS["font-body"], "color": c["text-d"], "size": 13},
        "paper_bgcolor": c["void"],
        "plot_bgcolor": c["void"],
        "colorway": CYCLE if theme == "light" else CYCLE_DARK,
        "title": {"x": 0, "xanchor": "left", "font": {"size": 16, "weight": 600}},
        "xaxis": axis,
        "yaxis": axis,
        "legend": {"bgcolor": "rgba(0,0,0,0)"},
        "hoverlabel": {
            "bgcolor": c["basalt"],
            "bordercolor": c["line-d"],
            "font": {"family": TOKENS["font-body"], "color": c["text-d"]},
        },
    })


TEMPLATES = {"light": "proteus", "dark": "proteus_dark"}
pio.templates[TEMPLATES["light"]] = template("light")
pio.templates[TEMPLATES["dark"]] = template("dark")


def use(theme="light"):
    """Make the template of ``theme`` ("light" or "dark") the default for new figures."""
    pio.templates.default = TEMPLATES[theme]
