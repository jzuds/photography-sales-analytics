import numpy as np
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

DATA_URL = st.secrets["gsheets"]["url"]

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='MammaWarrior Analytics',
    page_icon='📈',
)

def fetch_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=DATA_URL)

    FINANCIAL_COLS = [
    "Gross Sales ($)",
    "PhotoDay Fee ($)",
    "Processing Fee ($)",
    "Product Costs ($)",
    "Lab Shipping Costs ($)",
    "Sales Tax Total ($)",
    "Taxable Amount ($)",
    "Studio Payouts ($)",
    ]

    NUMERIC_COLS = df.select_dtypes(include=np.number).columns.tolist()

    COLUMNS_TO_CAST_TO_NUM = [col for col in FINANCIAL_COLS if col not in NUMERIC_COLS]


    # convert FINANCIAL_COLS to numeric if not already
    for fin_col in COLUMNS_TO_CAST_TO_NUM:
        df[fin_col] = df[fin_col].str.replace(',', '')

        # Convert to numeric, coercing errors to NaN
        df[fin_col] = pd.to_numeric(df[fin_col], errors='coerce')

    return df

data = fetch_data()

st.dataframe(data)
st.bar_chart(data, x="MonthYear", y="Gross Sales ($)")
