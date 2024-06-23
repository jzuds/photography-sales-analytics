import duckdb
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

DATA_URL = st.secrets["gsheets"]["url"]

if "duck_conn" not in st.session_state:
    st.session_state["duck_conn"] = duckdb.connect(":memory:")

conn = st.session_state["duck_conn"]

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='MammaWarrior Analytics',
    page_icon='📈',
)

def fetch_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=DATA_URL)

    FINANCIAL_COLS = [
    "Amount",
    "Used Credits",
    ]

    NUMERIC_COLS = df.select_dtypes(include=np.number).columns.tolist()

    COLUMNS_TO_CAST_TO_NUM = [col for col in FINANCIAL_COLS if col not in NUMERIC_COLS]


    # convert FINANCIAL_COLS to numeric if not already
    for fin_col in COLUMNS_TO_CAST_TO_NUM:
        df[fin_col] = df[fin_col].str.replace(',', '')

        # Convert to numeric, coercing errors to NaN
        df[fin_col] = pd.to_numeric(df[fin_col], errors='coerce')

    return df


def load_data():
    df = fetch_data()
    return conn.execute("CREATE TABLE IF NOT EXISTS transactions AS SELECT * FROM df")


def main():
    load_data()

    transactions_monthly_agg = conn.execute('''
        SELECT 
            "Purchase Date", 
            SUM("Amount") as "Amount",
            SUM("Used Credits") as "Used Credits"
        FROM transactions
        GROUP BY 
            "Purchase Date"
        ORDER BY 
            "Purchase Date" DESC
    ''').fetchdf()

    month_dropdown_select = conn.execute('''
        SELECT DISTINCT 
            "Purchase Date" 
        FROM transactions 
        ORDER BY 
            "Purchase Date"
    ''').fetchdf()

    st.header('MammaWarrior Analytics 📈')

    st.write("Monthly Gross Sales")
    st.line_chart(
        data=transactions_monthly_agg,
        x="Purchase Date", 
        y="Amount",
        color=[75, 83, 32],
    )

    st.write("Daily PhotoDay Breakdown")
    st.dataframe(transactions_monthly_agg)

    


if __name__ == "__main__":
    main()