import os
import xlwings as xw
import plotly.express as px
from data import *
from datetime import date
from dotenv import load_dotenv
load_dotenv()

path = os.getenv("PATH")
today = date.today()

formatted_date = today.strftime("%Y-%m-%d")
# Create workbook
wb = xw.Book()

# Add sheets for figures
wb.sheets[0].name = 'Figure 1'
wb.sheets.add(name='Figure 2')
wb.sheets.add(name='Figure 3')

# Add sheets for data
wb.sheets.add(name='Currency Amount Outstanding')
wb.sheets.add(name='Bank Amount Outstanding')
wb.sheets.add(name='Claim Amount Outstanding')

# Generate data
df1 = currency_amount_outstanding()
print('Generate data for currency amount outstanding')
df2 = bank_amount_outstanding()
print('Generate data for bank amount outstanding')
df3 = claim_amount_outstanding()
print('Generate data for claim amount outstanding')

# Generate figures
fig1 = simple_fig(df3)
fig2 = fig_amount_outstanding(df1, 'Currency')
fig3 = fig_amount_outstanding(df2, 'Counterparty sector')

# Insert figures
wb.sheets['Figure 1'].pictures.add(fig1, name='fig1', update=True)
wb.sheets['Figure 2'].pictures.add(fig2, name='fig2', update=True)
wb.sheets['Figure 3'].pictures.add(fig3, name='fig3', update=True)

df3 = df3.pivot(columns='Period', index='Reporting country', values='Value').reset_index()
df2 = df2.pivot(columns='Year', index=['Balance sheet position', 'Counterparty sector'], values='Value').reset_index()
df1 = df1.pivot(columns='Year', index=['Balance sheet position', 'Currency'], values='Value').reset_index()


# Insert DataFrames
wb.sheets['Currency Amount Outstanding']["A1"].options(index=False).value = df1
wb.sheets['Bank Amount Outstanding']["A1"].options(index=False).value = df2
wb.sheets['Claim Amount Outstanding']["A1"].options(index=False).value = df3

# Save workbook
wb.save(rf"{path}\({formatted_date}) CY data and figures.xlsx")
wb.close()