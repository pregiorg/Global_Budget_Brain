# 📊 Global Budget Brain — Country Data Analysis

A Python data analysis script that tests economic and demographic hypotheses across world countries using statistical methods.

## Hypotheses Tested

- **H1:** Countries with higher GDP per capita have significantly lower infant mortality rates
- **H2:** Western Europe has significantly higher GDP per capita and lower agricultural sector share than Sub-Saharan Africa

## Features

- Cleans and normalizes messy CSV data (EU-style decimal commas → dots)
- Pearson correlation with p-value significance testing
- Independent t-test for group comparisons (H1)
- Mann-Whitney U test for non-parametric regional comparisons (H2)
- Automatic result interpretation printed to console

## Usage

1. Clone the repo:
```bash
git clone https://github.com/pregiorg/global-budget-brain.git
cd global-budget-brain
```

2. Place `countries of the world.csv` in the project root

3. Run:
```bash
python analysis.py
```

## Requirements

- Python 3.x
- pandas
- numpy
- scipy

Install dependencies:
```bash
pip install pandas numpy scipy
```

## Dataset

Uses the [Countries of the World](https://www.kaggle.com/datasets/fernandol/countries-of-the-world) dataset from Kaggle. Place the CSV file in the same directory as the script.

## Sample Output

```
================================================================================
ΑΝΑΛΥΣΗ ΔΕΔΟΜΕΝΩΝ - GLOBAL BUDGET BRAIN (GBB)
================================================================================

ΥΠΟΘΕΣΗ 1: ...
Pearson Correlation: -0.8134
P-value: 1.23e-45
Result: ✅ ΕΠΑΛΗΘΕΥΕΤΑΙ ΠΛΗΡΩΣ
```

## Statistical Methods

| Test | Used For | Why |
|------|----------|-----|
| Pearson r | GDP vs Infant Mortality | Linear relationship check |
| Independent t-test | High vs Low GDP groups | Mean comparison |
| Mann-Whitney U | Europe vs Africa | Non-parametric; skewed GDP distributions |

## Known Limitations

- Hardcoded region strings (`'WESTERN EUROPE'`) — case/space sensitive
- `matplotlib` imported but unused
- File path assumes CWD matches script location

## What I Learned

- Cleaning real-world CSV data with inconsistent decimal formats
- Choosing between parametric (t-test) and non-parametric (Mann-Whitney) tests
- Interpreting Pearson correlation alongside p-values
- Structuring hypothesis testing with clear result summaries
- Working with `pandas`, `numpy`, and `scipy.stats` together

## License

MIT
