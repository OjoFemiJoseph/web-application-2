import streamlit as st

from pages import add_data
from pages import show_raw
from pages import explore
from pages import explore_two


st.set_page_config(page_title="page", layout="wide")


menu = st.sidebar.radio(
     'Select Menu:', ['Add','Show Raw','Explore','Explore Two'],index=0)


if menu == "Add":
    data = add_data.add_data()
    data.app()
    

if menu == "Show Raw":
    show_raw.app()
    
if menu == "Explore":
    explore.app()
    

if menu == "Explore Two":
    explore_two.app()
    
