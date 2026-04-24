# 📊 BIS Data Processing

This folder contains scripts for processing and visualizing data from the Bank for International Settlements (BIS) Locational Banking Statistics (LBS) database. 🚀

## 📁 Files

### 🐍 data.py
This Python script contains functions to fetch and process BIS data:

- `currency_amount_outstanding()`: 💰 Fetches and processes currency amount outstanding data for Asian countries.
- `bank_amount_outstanding()`: 🏦 Fetches and processes bank amount outstanding data categorized by counterparty sector.
- `claim_amount_outstanding()`: 🌍 Fetches and processes claim amount outstanding data by reporting country.
- `simple_fig()`: 📊 Creates a simple bar chart using Plotly Express.
- `fig_amount_outstanding()`: 📈 Creates a bar chart for amount outstanding data with annotations.

The script uses the BIS API to retrieve CSV data, processes it with pandas, and generates visualizations with Plotly. 🔄

### 📊 to_excel.py
This script automates the creation of an Excel workbook containing BIS data and figures:

- 📝 Creates a new Excel workbook using xlwings.
- 🔄 Generates data using functions from `data.py`.
- 📊 Creates three figures: a simple figure and two amount outstanding figures.
- 📥 Inserts figures and pivoted data into separate sheets.
- 💾 Saves the workbook with a date-stamped filename.

## 📦 Dependencies

- pandas 🐼
- plotly 📊
- xlwings 📈
- pycountry 🌍
- python-dotenv 🔐

Install dependencies using:
```bash
pip install pandas plotly xlwings pycountry python-dotenv
```

## ⚙️ Environment Setup

Create a `.env` file in the same directory with the following variable:
```
PATH=/path/to/your/output/directory
```

## 🚀 Usage

1. ✅ Ensure all dependencies are installed.
2. 🔧 Set up the `.env` file with the desired output path.
3. ▶️ Run `to_excel.py` to generate the Excel report with data and figures.

## 🌐 Data Sources

Data is fetched from the BIS Statistics API:
- 🔗 https://stats.bis.org/api/v2/data/dataflow/BIS/WS_LBS_D_PUB/1.0/

## 📤 Output

The script generates an Excel file named `(YYYY-MM-DD) data and figures.xlsx` containing:
- 📊 Figure 1: Simple bar chart
- 💰 Figure 2: Currency amount outstanding
- 🏦 Figure 3: Bank amount outstanding
- 📋 Currency Amount Outstanding: Pivoted data table
- 📋 Bank Amount Outstanding: Pivoted data table
- 📋 Claim Amount Outstanding: Pivoted data table