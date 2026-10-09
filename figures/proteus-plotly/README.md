# proteus-plotly

PROTEUS Thermocline Plotly theme. Interactive figures whose colors, fonts, and
surfaces match the website, the docs, and the matplotlib figures of
[proteus-mpl](../proteus-mpl/).

## Install

From a checkout of the repository: `pip install figures/proteus-plotly` (or cd
into the folder and `pip install .`).

## Use

```python
import plotly.graph_objects as go
import proteus_plotly

proteus_plotly.use()              # light: Paper background
# proteus_plotly.use("dark")      # dark: Void background
fig = go.Figure(go.Scatter(y=[3, 1, 2]))
fig.update_layout(template="proteus_dark")   # or choose per figure
```

## What you get

- **Templates** `proteus` and `proteus_dark`, registered in
  `plotly.io.templates` on import: Instrument Sans text, the page surface as
  background (Paper or Void), hairline grid, left-aligned titles, and hover
  labels on the card surface.
- **Colors by token name**: `proteus_plotly.colors("light")["danger"]`. `TOKENS`
  holds the dark-first values of `tokens.css`, `LIGHT` its light-theme remaps,
  so a name such as `text-d2` (secondary text) or `void` (page) gives the right
  value on either surface, as in the CSS.
- **Cycles** `CYCLE` (light, 9 colours) and `CYCLE_DARK` (6), the same as
  proteus-mpl's, set as each template's `colorway`.
- **Module domain colors**: `DOMAINS` maps a domain to its token, `MODULES` a
  module to its domain. Use them whenever a trace *is* a module.
- **Status colors**: `STATUS` names the tokens `positive`, `warning`,
  `danger` and `info`.
- **A second cue within a domain**: `module_markers(["aragog", "zalmoxis"])`
  gives bar markers in the interior colour, Aragog plain and Zalmoxis hatched
  (`marker.pattern`), so two modules of one domain stay apart without a new
  hue.

## Example

`python examples/modules.py` writes `modules_light.html` and
`modules_dark.html` next to the script: time per module as stacked bars.

## Check

`python3 figures/proteus-plotly/check_tokens.py` compares every colour and
font here with `tokens/tokens.css`, in both themes, and the cycles with
proteus-mpl's. CI runs it with the other token checks.
