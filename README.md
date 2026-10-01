# 📊 Week 5 — Data Visualization & Communication

## 📌 Project Overview

A Python data visualization project using the **Gapminder country-year dataset** to explore changes in **health, wealth, and population from 1952 to 2007**.

The project includes static charts using **Matplotlib and Seaborn**, an interactive **Plotly** visualization, and a report explaining the key findings.

## 🎯 Objectives

* Analyze historical trends and patterns.
* Choose suitable charts for different analytical questions.
* Present insights clearly through annotations and visual storytelling.
* Communicate correlation without assuming causation.

## 🌍 Dataset

**Gapminder Dataset — Plotly Express**

* **1,704** records
* **142** countries
* **5** continents
* **1952–2007**
* Key fields: country, continent, year, life expectancy, population, and GDP per capita.

## 📈 Visualizations

1. **Life Expectancy Trend** — changes in health over time.
2. **GDP per Capita Trend** — wealth trends using a logarithmic scale.
3. **Population Growth** — demographic changes by continent.
4. **Wealth vs Life Expectancy** — relationship between GDP and health in 2007.
5. **Life Expectancy Gains** — countries with the largest improvements.
6. **GDP Distribution** — variation in GDP per capita across continents in 2007.

## 🔎 Key Findings

| Metric                             | Result                   |
| ---------------------------------- | ------------------------ |
| Life expectancy                    | **48.94 → 68.92 years**  |
| Largest 2007 population            | **Asia — ~3.81 billion** |
| GDP vs Life Expectancy correlation | **r ≈ 0.81**             |
| Largest life expectancy gain       | **Oman — +38.1 years**   |

These results are calculated from the dataset used in the project.

## 🛠️ Technologies

**Python · Pandas · NumPy · Matplotlib · Seaborn · Plotly Express · python-docx**

## 📂 Project Files

```text
README.md
requirements.txt
week5_visualization_project.py
create_report.py
gapminder_clean.csv
summary_statistics.csv
interactive_gdp_life_expectancy.html
Week5_Data_Visualization_Communication_Report.pdf
Week5_Data_Visualization_Communication_Report.docx
figures/
```

## 🚀 Run the Project

```bash
git clone https://github.com/YOUR-USERNAME/week5-data-visualization-communication.git
cd week5-data-visualization-communication

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt
python week5_visualization_project.py
```

The script generates the visualizations, processed datasets, summary statistics, and interactive Plotly chart.

## ⚠️ Limitations

The dataset ends in **2007**, so it does not represent current global conditions. GDP and life expectancy correlation also does not prove causation, and continental averages may hide country-level differences.

## 👤 Author

**Kartik Koli**
BCA Student | Data Analytics & AI/ML Learner

This project was developed as part of a **Week 5 Data Visualization and Communication** assignment.

## ⭐ Data Source

**Gapminder / Plotly Express Gapminder Dataset**

