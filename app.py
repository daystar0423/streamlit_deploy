import my
import chart
import streamlit as st
import pandas as pd
import importlib
importlib.reload(my)
importlib.reload(chart)

with st.expander("step 1 : load data"):
    file = st.file_uploader("upload osc data from sst", type=('txt', 'csv'))

with st.expander("step 2 : default setting"):
    c1, c2 = st.columns(2)
    with c1: full_stroke = st.number_input('full stroke [mm]', value = 0.00)
    with c2: ct_sep_per = st.number_input('contact seperation [%]', value = 0.00)
    
with st.expander("step 2 : plot chart"):
    chart.auto_chart(file, True, full_stroke, ct_sep_per)
