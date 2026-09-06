# 📊 Sales Data Analysis

An end-to-end retail sales analysis, built twice — once as an interactive **Power BI dashboard** and once as a clean, modular **Python** pipeline (pandas + matplotlib, notebook-driven). Same data, same business logic, two ways of delivering it.

## What this project answers

- Which products are the strongest and weakest performers — by sales, profit, and units sold
- How sales move over time — daily, monthly, quarterly, and year over year
- How closely profit tracks sales, and where that relationship breaks down
- How any two time periods compare on sales, profit, and quantity sold
- Which promotions carry the deepest average discounts
- Where revenue is concentrated geographically, by city
- A fully filterable order-level view — by product, date, customer, or promotion

## Dashboard preview

<p align="center">
  <img src="powerbi/screenshots/overview.jpg" width="420"/>
  <img src="powerbi/screenshots/top_bottom_products.jpg" width="420"/>
  <br/>
  <img src="powerbi/screenshots/sales_trends.jpg" width="420"/>
  <img src="powerbi/screenshots/period_comparison.jpg" width="420"/>
  <br/>
  <img src="powerbi/screenshots/top_bottom_sales_vs_profit.jpg" width="420"/>
  <img src="powerbi/screenshots/order_level_table.jpg" width="420"/>
</p>

The full interactive report — with slicers, drill-through, and tooltips — is in `powerbi/sales-data-analysis.pbix`.

## Tech stack

**Power BI** · DAX measures, interactive slicers and filters
**Python** · pandas, numpy, matplotlib, seaborn, Jupyter

## Project structure

```
sales-data-analysis/
├── data/store_data.xlsx          # source workbook (fact + 3 dimension tables)
├── powerbi/
│   ├── sales-data-analysis.pbix  # interactive dashboard
│   └── screenshots/              # dashboard preview images
├── src/                          # analysis package
│   ├── data_loader.py            # reads the raw Excel sheets
│   ├── data_cleaning.py          # whitespace / dtype cleanup
│   ├── feature_engineering.py    # derives price, discount, profit, net sales
│   ├── analysis.py               # one function per business question
│   └── visualization.py          # matching chart for each question
├── notebooks/Sales_Data_Analysis.ipynb
└── screenshots/                  # chart images exported by the notebook
```

## Quick start

```bash
git clone <repo-url>
cd sales-data-analysis
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook notebooks/Sales_Data_Analysis.ipynb
```

## Key assumptions

- Discount rate is parsed from each promotion's terms (e.g. "20% off" → 20%); "Buy 1 Get 1 Free" is modeled as an effective 50% discount.
- Profit is calculated as a flat 10% margin on net sales, matching the measure used in the Power BI model (the source data has no cost column).
- Orders with no promotion applied are labeled "No Promotion."
