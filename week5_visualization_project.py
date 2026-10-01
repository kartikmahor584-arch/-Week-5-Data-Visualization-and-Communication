"""Week 5 - Data Visualization and Communication
Portfolio project based on Plotly Express' Gapminder dataset.

Dataset source:
- Plotly Express built-in Gapminder data: https://plotly.com/python-api-reference/generated/plotly.express.data.html
- Original data source / attribution: https://www.gapminder.org/data/

Outputs:
- figures/01_life_expectancy_trend.png
- figures/02_gdp_per_capita_trend.png
- figures/03_population_growth.png
- figures/04_wealth_vs_life_expectancy_2007.png
- figures/05_life_expectancy_gain.png
- figures/06_gdp_distribution_2007.png
- interactive_gdp_life_expectancy.html
- gapminder_clean.csv
- summary_statistics.csv
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# -----------------------------
# Paths and global styling
# -----------------------------
ROOT = Path(__file__).resolve().parent
FIG_DIR = ROOT / "figures"
FIG_DIR.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", context="talk")
plt.rcParams.update({
    "figure.dpi": 150,
    "savefig.dpi": 180,
    "axes.titleweight": "bold",
    "axes.titlesize": 18,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 9,
})

# -----------------------------
# Load dataset
# -----------------------------
df = px.data.gapminder().copy()
df = df.sort_values(["country", "year"]).reset_index(drop=True)

df.to_csv(ROOT / "gapminder_clean.csv", index=False)

# -----------------------------
# Prepare summaries
# -----------------------------
def weighted_average(group: pd.DataFrame, value: str, weight: str) -> float:
    return float(np.average(group[value], weights=group[weight]))

continent_summary = (
    df.groupby(["year", "continent"])
    .apply(
        lambda g: pd.Series({
            "weighted_life_exp": weighted_average(g, "lifeExp", "pop"),
            "median_gdp_per_capita": g["gdpPercap"].median(),
            "population": g["pop"].sum(),
        }),
        include_groups=False,
    )
    .reset_index()
)
continent_summary.to_csv(ROOT / "summary_statistics.csv", index=False)

# -----------------------------
# Figure 1: Life expectancy trend
# -----------------------------
fig, ax = plt.subplots(figsize=(12, 7))
sns.lineplot(
    data=continent_summary,
    x="year",
    y="weighted_life_exp",
    hue="continent",
    marker="o",
    linewidth=2.4,
    ax=ax,
)
ax.set_title("Life Expectancy Rose Across Every Continent, 1952-2007")
ax.set_xlabel("Year")
ax.set_ylabel("Population-weighted life expectancy (years)")
ax.legend(title="Continent", frameon=True, ncol=3)
ax.text(
    0.01,
    -0.16,
    "Weighted by population within each continent; country-year observations come from the Gapminder dataset.",
    transform=ax.transAxes,
    fontsize=9,
)
fig.tight_layout()
fig.savefig(FIG_DIR / "01_life_expectancy_trend.png", bbox_inches="tight")
plt.close(fig)

# -----------------------------
# Figure 2: GDP per capita trend
# -----------------------------
fig, ax = plt.subplots(figsize=(12, 7))
sns.lineplot(
    data=continent_summary,
    x="year",
    y="median_gdp_per_capita",
    hue="continent",
    marker="o",
    linewidth=2.4,
    ax=ax,
)
ax.set_yscale("log")
ax.set_title("Median GDP per Capita Increased, but the Gap Remained Large")
ax.set_xlabel("Year")
ax.set_ylabel("Median GDP per capita (US$; log scale)")
ax.legend(title="Continent", frameon=True, ncol=3)
ax.text(
    0.01,
    -0.16,
    "Median is used to reduce the effect of very large or very small country values; log scale makes long-term gaps easier to compare.",
    transform=ax.transAxes,
    fontsize=9,
)
fig.tight_layout()
fig.savefig(FIG_DIR / "02_gdp_per_capita_trend.png", bbox_inches="tight")
plt.close(fig)

# -----------------------------
# Figure 3: Population growth
# -----------------------------
fig, ax = plt.subplots(figsize=(12, 7))
pop_plot = continent_summary.copy()
pop_plot["population_millions"] = pop_plot["population"] / 1_000_000
sns.lineplot(
    data=pop_plot,
    x="year",
    y="population_millions",
    hue="continent",
    marker="o",
    linewidth=2.4,
    ax=ax,
)
ax.set_title("Population Growth Was Strongest in Asia")
ax.set_xlabel("Year")
ax.set_ylabel("Population (millions)")
ax.legend(title="Continent", frameon=True, ncol=3)
fig.tight_layout()
fig.savefig(FIG_DIR / "03_population_growth.png", bbox_inches="tight")
plt.close(fig)

# -----------------------------
# Figure 4: Wealth vs life expectancy (2007)
# -----------------------------
latest = df[df["year"] == 2007].copy()
fig, ax = plt.subplots(figsize=(13, 8))
for continent in sorted(latest["continent"].unique()):
    sub = latest[latest["continent"] == continent]
    ax.scatter(
        np.log10(sub["gdpPercap"]),
        sub["lifeExp"],
        s=np.sqrt(sub["pop"]) / 18,
        alpha=0.72,
        label=continent,
        edgecolors="white",
        linewidths=0.6,
    )

# Annotate selected reference countries so the story is easier to read.
for country in ["China", "India", "United States", "Japan", "Zimbabwe"]:
    row = latest[latest["country"] == country]
    if not row.empty:
        x = float(np.log10(row["gdpPercap"].iloc[0]))
        y = float(row["lifeExp"].iloc[0])
        ax.annotate(country, (x, y), xytext=(7, 7), textcoords="offset points", fontsize=9)

corr = latest[["gdpPercap", "lifeExp"]].assign(log_gdp=np.log(latest["gdpPercap"]))[["log_gdp", "lifeExp"]].corr().iloc[0, 1]
ax.set_title("In 2007, Wealth and Life Expectancy Moved Together")
ax.set_xlabel("GDP per capita (US$; log10 scale)")
ax.set_ylabel("Life expectancy (years)")
ax.set_xticks(np.arange(2.5, 5.1, 0.5), labels=[f"10^{x:.1f}" for x in np.arange(2.5, 5.1, 0.5)])
ax.legend(title="Continent", frameon=True, ncol=3)
ax.text(
    0.02,
    0.03,
    f"Pearson correlation with log GDP per capita: r = {corr:.2f}  |  Bubble size represents population",
    transform=ax.transAxes,
    fontsize=10,
    bbox=dict(boxstyle="round,pad=0.4", facecolor="white", alpha=0.85),
)
fig.tight_layout()
fig.savefig(FIG_DIR / "04_wealth_vs_life_expectancy_2007.png", bbox_inches="tight")
plt.close(fig)

# -----------------------------
# Figure 5: Life expectancy gains by country
# -----------------------------
first = df[df["year"] == df["year"].min()].set_index("country")
last = df[df["year"] == df["year"].max()].set_index("country")
gains = (last["lifeExp"] - first["lifeExp"]).sort_values(ascending=False)
top10 = gains.head(10).sort_values()
fig, ax = plt.subplots(figsize=(12, 7))
ax.barh(top10.index, top10.values)
ax.set_title("Largest Life Expectancy Gains in the Dataset")
ax.set_xlabel("Increase from 1952 to 2007 (years)")
ax.set_ylabel("")
for i, value in enumerate(top10.values):
    ax.text(value + 0.5, i, f"+{value:.1f}", va="center", fontsize=9)
ax.set_xlim(0, max(top10.values) + 6)
fig.tight_layout()
fig.savefig(FIG_DIR / "05_life_expectancy_gain.png", bbox_inches="tight")
plt.close(fig)

# -----------------------------
# Figure 6: GDP distribution by continent (2007)
# -----------------------------
fig, ax = plt.subplots(figsize=(12, 7))
sns.boxplot(
    data=latest,
    x="continent",
    y="gdpPercap",
    ax=ax,
)
ax.set_yscale("log")
ax.set_title("GDP per Capita Varied Widely Within Continents in 2007")
ax.set_xlabel("Continent")
ax.set_ylabel("GDP per capita (US$; log scale)")
ax.tick_params(axis="x", rotation=0)
ax.text(
    0.01,
    -0.14,
    "Each box summarizes the distribution of country GDP-per-capita values within a continent.",
    transform=ax.transAxes,
    fontsize=9,
)
fig.tight_layout()
fig.savefig(FIG_DIR / "06_gdp_distribution_2007.png", bbox_inches="tight")
plt.close(fig)

# -----------------------------
# Interactive figure
# -----------------------------
interactive = px.scatter(
    df,
    x="gdpPercap",
    y="lifeExp",
    size="pop",
    color="continent",
    hover_name="country",
    animation_frame="year",
    log_x=True,
    size_max=55,
    title="Interactive: GDP per Capita vs Life Expectancy, 1952-2007",
    labels={
        "gdpPercap": "GDP per capita (US$)",
        "lifeExp": "Life expectancy (years)",
        "pop": "Population",
        "continent": "Continent",
    },
)
interactive.update_layout(template="plotly_white", legend_title_text="Continent")
interactive.write_html(ROOT / "interactive_gdp_life_expectancy.html", include_plotlyjs=True)

# -----------------------------
# Print key findings for reproducibility
# -----------------------------
world_1952 = weighted_average(df[df["year"] == 1952], "lifeExp", "pop")
world_2007 = weighted_average(df[df["year"] == 2007], "lifeExp", "pop")
print("Dataset shape:", df.shape)
print(f"Population-weighted world life expectancy: {world_1952:.2f} years (1952) -> {world_2007:.2f} years (2007)")
print(f"2007 correlation, log GDP per capita vs life expectancy: r = {corr:.2f}")
print("Largest life-expectancy gains:")
print(gains.head(10).round(1).to_string())
print("\nCreated files in:", ROOT)
