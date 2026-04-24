import pandas as pd
import datetime
import plotly.express as px
import pycountry

year = datetime.datetime.now().year

def currency_amount_outstanding() -> pd.DataFrame:
    urls = ["https://stats.bis.org/api/v2/data/dataflow/BIS/WS_LBS_D_PUB/1.0/.S.C+L.A.TO1.D+F.5J.A.BH+CN+CY+HK+ID+IN+JP+KR+MO+MY+PH+SA+SG+TR+TW.A.5J.N?format=csv"]
    df = pd.concat([pd.read_csv(url) for url in urls])
    col_use = ['L_POSITION','L_CURR_TYPE', 'L_REP_CTY','TIME_PERIOD','OBS_VALUE']
    df2 = df[col_use].copy()
    df2.replace({'D': 'D:Domestic currency (ie currency of bank location country)',
                'F': 'F:Foreign currency (ie currencies foreign to bank location country)',
                'L': 'L:Total liabilities',
                'C': 'C:Total claims'}, inplace=True)

    # df1 = pd.read_excel(r"C:\Users\AhmadAizudeen\The SOUTH-EAST ASIAN CENTRAL BANKS (SEACEN) RESEARCH AND TRAINING\SEACEN Faculty & Research - RSU\02_Requests\2025\2025.04.29 RM CYP presentation charts\raw data and figures\CY data\currency amount outstanding.xlsx", sheet_name='Sheet1')
    rename_col = ['Balance sheet position', 'Currency', 'Reporting country', 'Period','Value']
    df2 = df2.rename(columns={k:v for k,v in zip(df2.columns, rename_col)})

    col = df2.columns.to_list()
    # col
    df2 = df2.groupby(by = ['Balance sheet position', 'Currency', 'Period']).sum()
    df2.reset_index(inplace=True)
    df2['Reporting country'] = 'Asia'
    df2['Year'] = df2['Period'].apply(lambda x: str(x)[:4])
    df2.drop(columns=['Period', 'Reporting country'], inplace=True)
    df2 = df2.groupby(['Year', col[0], 'Currency']).sum()
    df2.reset_index(inplace=True)
    df2['Value'] = df2.apply(lambda row: row['Value'] if row['Balance sheet position'] == 'C:Total claims' else -row['Value'], axis=1)
    change_year = df['TIME_PERIOD'].sort_values().unique()[-1]
    df2.replace({change_year[:4]: change_year}, inplace=True)
    df2 = df2[df2['Year'] >= '2000']
    return df2

def bank_amount_outstanding() -> pd.DataFrame:
    urls = ["https://stats.bis.org/api/v2/data/dataflow/BIS/WS_LBS_D_PUB/1.0/.S.C+L.A.TO1.A.5J.A.BH+CN+CY+HK+ID+IN+JP+KR+MO+MY+PH+SA+SG+TR+TW.B+N.5J.N?format=csv"]
    df = pd.concat([pd.read_csv(url) for url in urls])
    col_use = ['L_POSITION','L_CP_SECTOR', 'L_REP_CTY','TIME_PERIOD','OBS_VALUE']
    df2 = df[col_use].copy()
    df2.replace({'B': 'B:Banks, total',
                'N': 'N:Non-banks, total',
                'L': 'L:Total liabilities',
                'C': 'C:Total claims'}, inplace=True)

    rename_col = ['Balance sheet position', 'Counterparty sector', 'Reporting country', 'Period','Value']
    df2 = df2.rename(columns={k:v for k,v in zip(df2.columns, rename_col)})

    col = df2.columns.to_list()
    # col
    df2 = df2.groupby(by = ['Balance sheet position', 'Counterparty sector', 'Period']).sum()
    df2.reset_index(inplace=True)
    df2['Reporting country'] = 'Asia'
    df2['Year'] = df2['Period'].apply(lambda x: str(x)[:4])
    df2.drop(columns=['Period', 'Reporting country'], inplace=True)
    df2 = df2.groupby(['Year', col[0], 'Counterparty sector']).sum()
    df2.reset_index(inplace=True)
    df2['Value'] = df2.apply(lambda row: row['Value'] if row['Balance sheet position'] == 'C:Total claims' else -row['Value'], axis=1)
    change_year = df['TIME_PERIOD'].sort_values().unique()[-1]
    df2.replace({change_year[:4]: change_year}, inplace=True)
    df2 = df2[df2['Year'] >= '2000']
    return df2

def claim_amount_outstanding():
    urls = ["https://stats.bis.org/api/v2/data/dataflow/BIS/WS_LBS_D_PUB/1.0/.S.C.A.TO1.A.5J.A.AT+AU+BE+CA+CH+DE+DK+ES+FI+FR+GB+GR+HK+IE+IT+JP+KR+LU+NL+SE+TW+US.A.AM+BD+GE+ID+IL+IN+KR+KZ+LB+LK+MY+PH+PK+TH.N?format=csv"]
    df = pd.concat([pd.read_csv(url) for url in urls]) 
    def code_to_country(code):
        country = pycountry.countries.get(alpha_2=code.upper())
        return country.name if country else None

    cty_code = df['L_REP_CTY'].unique().tolist() + df['L_CP_COUNTRY'].unique().tolist()
    cty_code_dict = {code: code_to_country(code) for code in cty_code}

    col_use = ['L_REP_CTY','TIME_PERIOD','OBS_VALUE']
    df2 = df[col_use].copy()
    df2.replace(cty_code_dict, inplace=True)

    rename_col = ['Reporting country', 'Period','Value']
    df2 = df2.rename(columns={k:v for k,v in zip(df2.columns, rename_col)})

    col = df2.columns.to_list()
    df2 = df2.groupby(by = ['Reporting country', 'Period']).sum()
    df2.reset_index(inplace=True)
    df2 = df2[df2['Period'].str[:4] >= '2005']
    df2.reset_index(drop=True,inplace=True)
    return df2

def simple_fig(df2: pd.DataFrame) -> px.bar:
    fig = px.bar(
        df2,
        x="Period",
        y="Value",
        color="Reporting country",
    )

    fig.update_layout(
        plot_bgcolor='white',
        width=800,
        height=500,
        margin=dict(b=100),   # Extra bottom space
        legend=dict(
            orientation="h",
            y=-0.3,           # Move legend further down
            x=0.5,
            xanchor="center",
            yanchor="top"
        )
    )


    fig.update_yaxes(title_text=None)

    return fig

def fig_amount_outstanding(df2: pd.DataFrame, var: str) -> px.bar:
    fig = px.bar(
        df2,
        x="Year",
        y="Value",
        color=var,
    )

    fig.update_layout(
        plot_bgcolor='white',
        width=800,
        height=500,
        margin=dict(b=100),   # Extra bottom space
        legend=dict(
            orientation="h",
            y=-0.3,           # Move legend further down
            x=0.5,
            xanchor="center",
            yanchor="top"
        )
    )

    fig.add_annotation(
        xref="paper", yref="paper",
        x=0.02, y=0.1,
        text="(-) Liabilities",
        showarrow=False,
        font=dict(size=12)
    )

    fig.add_annotation(
        xref="paper", yref="paper",
        x=0.02, y=0.9,
        text="(+) Claims",
        showarrow=False,
        font=dict(size=12)
    )

    fig.update_yaxes(title_text=None)

    return fig
