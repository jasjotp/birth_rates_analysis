# Birth Rates Analysis — Canada vs the World

This project analyzes historical birth rate and population data for Canada and 260+ other countries from 1960 to 2023. The goal is to explore trends in global and Canadian birth rates, track population changes over time, and compute the chance of being born in Canada in any given year based on available data.

---

## 📊 Key Findings

### Chance of Being Born in Canada (1960–2023)

| Year | Canada Births | Global Births | Chance (%) |
|------|----------------|------------------|--------------|
| 1960 | 478,180        | 1.35B            | **0.035%**   |
| 2023 | 352,735        | 2.01B            | **0.018%**   |

- In 1960, about **0.035%** of global births occurred in Canada.
- By 2023, this chance **dropped to 0.018%** — nearly half.
- This decline reflects Canada’s relatively stable or declining birth rate while the global population nearly **doubled**.

---

## Highlights

- **Years Covered**: 1960 to 2023  
- **Number of Countries**: 262  
- **Average Global Birth Rate**: 27.91 births per 1,000 people  
- **Database**: `birth_stats.db` (SQLite)

---

## Visuals Included (Some visuals get an out of memory error - still needs to be fixed)

All plots are saved in the project directory:

- `global_average_birth_rate.png`: Average birth rate per country
- `canada_birth_rate.png`: Yearly birth rate trend in Canada
- `canada_population.png`: Year-over-year population of Canada
- `other_population.png`: Population trends for all other countries
- `chance_of_birth_in_canada.png`: Canada's share of global births over time

---

## Interpretation of Trends

- **Canada's declining share** of global births suggests either a relatively slower population growth or lower fertility rates compared to global averages.
- Despite Canada’s population increasing, **its global significance in birth contribution has declined**.
- **Global births rose steadily** from ~1.35B in 1960 to over 2B in 2023.
- The slight decline in birth counts in Canada over time (from ~478K to ~352K) also supports concerns around **aging populations** and **slowing growth**.

---

## Tech Stack

- **Python** (pandas, matplotlib, seaborn, sqlite3)
- **SQLite** for querying and joining datasets
- **Jupyter Notebooks** for exploration
- **Git & GitHub** for version control

---

##  How to Run

1. Clone the repository and run the file
   ```bash
   git clone https://github.com/jasjotp/birth_rates_analysis.git
   cd birth_rates_analysis
   python preprocessing-eda-01.py

---

## File Structure 
birth_rates_analysis/
├── birth_stats.db                   # SQLite database with merged birth + population data
├── preprocessing-eda-01.py         # Script to clean, join, analyze, and plot data
├── canada_birth_rate.png
├── canada_population.png
├── global_average_birth_rate.png
├── chance_of_birth_in_canada.png
├── README.md                        # This file
└── .ipynb_checkpoints/             # Jupyter notebook backups

--- 
