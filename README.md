# Tarmeez Capital – Demand & Supply Planning Dashboard

## Project Overview
This project delivers a live, executive-level financial dashboard focused on Demand & Supply Planning KPIs.  
The solution is designed to help business stakeholders monitor forecast performance, identify inventory risks, evaluate service reliability, and quantify the financial impact of planning decisions.
The dashboard answers key business questions:

- How accurate is the forecast compared to actual demand?
- What is the financial impact of forecast error?
- Where are stockout risks occurring?
- How healthy is the inventory?
- How reliable are suppliers?

## Data Source
Dataset: Demand Supply Planning Dataset  
Source: Public dataset for analytical purposes.

The dataset includes monthly demand planning metrics such as forecast units, actual demand, inventory value, fill rate, stockout flags, and lead time attributes.

## Steps & Methodology

### Data Preparation
- Loaded the dataset using Pandas
- Applied robust numeric parsing
- Standardized categorical flags
- Created derived financial metrics

### Analytics & KPIs
The dashboard includes:

- Forecast Accuracy (W-MAPE, MAPE, Bias, MAE)
- Service Level (Fill Rate, Stockout Rate)
- Inventory Health (DOI, Turnover, SLOB)
- Financial Impact (Forecast variance cost)
- Supplier Reliability (Lead Time variability)

### Tools Used
- Python
- Streamlit  
- Plotly  
- Pandas  
- NumPy  

## Key Insights

- Forecast error is concentrated in specific SKUs, suggesting the need for SKU-level model tuning.
- Under-forecast risk contributes directly to potential lost revenue.
- Inventory health varies across product groups, indicating optimization opportunities.
- Lead time variability suggests supplier reliability risks.

## Live Dashboard Link

👉 **(PASTE YOUR STREAMLIT LINK HERE AFTER DEPLOYMENT)**

## Assumptions & Limitations

- COGS is estimated using Unit Cost × Actual Demand.
- Revenue at Risk is approximated using stockout-flagged rows.
- Some KPIs depend on available fields in the dataset.