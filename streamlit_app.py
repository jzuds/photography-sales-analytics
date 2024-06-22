import streamlit as st
from streamlit_gsheets import GSheetsConnection

DATA_URL = st.secrets["gsheets"]["url"]

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='MammaWarrior Analytics',
    page_icon='📈',
)

conn = st.connection("gsheets", type=GSheetsConnection)
data = conn.read(spreadsheet=DATA_URL)
st.dataframe(data)