# End-to-End Book Sales Analytics: YAML, Parquet, CSV to Streamlit Dashboard

A multi-source data cleaning, reconciliation, and analytics project built with <b>Pandas</b>, <b>Jupyter Notebook</b>, and <b>Streamlit</b>.

This project processes three separate datasets — <b>DATA1</b>, <b>DATA2</b>, and <b>DATA3</b> — each containing information about books, orders, and users in different file formats. The raw data was cleaned and analyzed in <b>Jupyter Notebook</b>, and the final results were manually transferred into a <b>Streamlit dashboard</b> for neat online presentation.

## Project Overview

Each dataset folder contains three files:

- books.yaml — book metadata, including titles, authors, genres, publishers, and publication years
- orders.parquet — order records, including purchased books, buyers, quantities, prices, and timestamps
- users.csv — customer information, including names, addresses, emails, and phone numbers

The main goal of the project was to turn raw, inconsistent data into a clean analytical layer and present the final business insights in a <b>professional BI-style dashboard accessible via browser</b>.

## Datasets

The project works with three separate folders:

- DATA1
- DATA2
- DATA3

Each folder represents an independent dataset with the same structure but different content.

## Business Questions Solved

For each dataset, the following metrics were computed:

1. Top 5 days by revenue in YYYY-MM-dd format
2. Number of unique users
3. Number of unique sets of authors
4. Most popular author or author set by sold book count
5. Best buyer, including all linked alias IDs
6. Daily revenue chart

## Data Processing Workflow

The analytical work was done in <b>Jupyter Notebook</b>, where the raw files were loaded, cleaned, normalized, and analyzed. After the final metrics were computed, the results were manually transferred into ```dashboard_data.py```, which powers the Streamlit dashboard pages.

This workflow was chosen to keep the data exploration and transformation steps transparent and notebook-friendly, while still delivering a clean browser-based dashboard as the final product.

## Data Cleaning and Normalization

Several real-world data quality issues had to be handled during preprocessing.

### 1. Books data (books.yaml)

- Loaded YAML content into Pandas through Python parsing
- Cleaned column names
- Converted year from messy string/object values into nullable integer format
- Replaced invalid year markers such as empty strings, tabs, NULL, and -
- Converted genre and publisher into more appropriate categorical types where applicable
- Cleaned publisher values by removing blank and broken entries

### 2. Orders data (orders.parquet)

- Parsed timestamps stored in multiple inconsistent formats
- Extracted a normalized date field from raw timestamp values
- Cleaned and standardized unit_price values
- Split price information into:
  - numeric value
  - currency type
- Normalized mixed currency formats such as:
  - 27.00$
  - USD 45.99
  - €50¢50
  - 22$75¢
- Converted EUR prices into USD using a fixed exchange rate
- Calculated paid_price
- Aggregated daily revenue for time-series analysis

### 3. Users data (users.csv)

- Cleaned phone numbers into a consistent presentation format
- Standardized string values for names, phones, and addresses
- Reconciled duplicate real-world users under the assumption that only one field may change
- Accounted for:
  - aliases instead of real names
  - changed addresses
  - changed phone numbers
 
## User Reconciliation Logic

One of the most important parts of the project was identifying <b>real unique users</b>.

Since the same person could appear multiple times with one changed field, exact duplicate removal was not enough. Instead, records were reconciled using the assumption that <b>only one user attribute may differ</b>, while the other identifying fields still match.

This allowed the project to:

- estimate the real number of unique users
- identify the top customer by total spending
- collect all related user IDs representing the same buyer

## Author Set Logic

Books were analyzed not only by individual author names, but also by <b>author sets</b>.

For example, if:

- John writes alone
- Paul writes alone
- John and Paul write together

then those count as <b>three different author sets</b>.

To solve this correctly, author combinations were normalized as unordered sets, so that:

- John, Paul
- Paul, John

would be treated as the same collaboration set.

## Dashboard

The final results are displayed in a <b>Streamlit dashboard</b>.

The dashboard was designed to resemble a compact BI report rather than plain text output. Each page presents the key metrics for one dataset and includes:

- KPI cards
- Top 5 revenue days table
- Most popular author(s)
- Best buyer aliases
- Daily revenue line chart
- Methodology notes

The final dashboard was deployed online using <b>Streamlit</b>.

## Tech Stack

- Python
- Pandas
- Jupyter Notebook
- PyYAML
- FastParquet
- Matplotlib
- Streamlit

## Project Structure

```
.
├── DATA1/
│   ├── books.yaml
│   ├── orders.parquet
│   └── users.csv
├── DATA2/
│   ├── books.yaml
│   ├── orders.parquet
│   └── users.csv
├── DATA3/
│   ├── books.yaml
│   ├── orders.parquet
│   └── users.csv
├── notebooks/
│   ├── task_Data_1.ipynb
│   ├── task_Data_2.ipynb
│   └── task_Data_3.ipynb
├── reports/
│   ├── daily_revenue_data_1.csv
│   ├── daily_revenue_data_2.csv
│   └── daily_revenue_data_3.csv
├── app.py
├── dashboard_utils.py
├── dashboard_data.py
├── pages/
│   ├── 1_Page_One.py
│   ├── 2_Page_Two.py
│   └── 3_Page_Three.py
└── requirements.txt
```

## Running the Dashboard Locally

Clone the repository and install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit app:

```bash
streamlit run app.py
```

## Live Demo

```
https://itransition-etybw67ltpkdvpvs6l5fpm.streamlit.app/
```

## Notes
- Data cleaning and feature engineering were performed in <b>Jupyter Notebook</b>
- Final dashboard values were manually transferred into ```dashboard_data.py```
- The dashboard is presentation-focused and intended to showcase the final analytical results clearly and professionally

## Why This Project Matters

This project demonstrates practical skills in:

- loading heterogeneous data formats
- cleaning messy real-world data
- type normalization
- handling inconsistent timestamps and prices
- reconciling duplicate entities
- aggregating business metrics
- building and deploying a browser-based analytical dashboard

It is a compact end-to-end example of turning raw multi-format data into a polished analytical product.
