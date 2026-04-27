import streamlit as st
import pandas as pd

df = pd.read_csv("dataset_teknik_sipil_indonesia.csv")

st.dataframe(df)
