import streamlit as st
from pages import Connect_Db
import pandas as pd

def app():
    st.write('show raw')
    multi_select_a = st.multiselect('Select A', ['Breakfast','Lunch','Dinner'])
    multi_select_b = st.multiselect('Select B', ['Major','Minor','Lieutanant','General','chief'])
    try:
        connection = Connect_Db.connectdb()
        cur = connection.cursor()

    
        if multi_select_a and not multi_select_b:
            #add to format it because of sql, IN works with tuple shape. that is , the values has to be passed like this (a,b,c)
            in_values = str(multi_select_a).replace('[','(').replace(']',')')
        
            query = f"select * from streamlith where col_a in {in_values}"
        
            df = pd.read_sql(query,connection)
        elif multi_select_b and not multi_select_a:
            in_values = str(multi_select_b).replace('[','(').replace(']',')')
            query = f"select * from streamlith where col_b in {in_values}"
            df = pd.read_sql(query,connection)
        elif multi_select_b and multi_select_a:
            in_values_a = str(multi_select_a).replace('[','(').replace(']',')')
            in_values_b = str(multi_select_b).replace('[','(').replace(']',')')
            query = f"select * from streamlith where col_b in {in_values_b} and col_a in {in_values_a}"
            df = pd.read_sql(query,connection)
        connection.close()
        if multi_select_a or multi_select_b:
            st.write(df[df.columns[:-1]])
    except:
        st.write('error connecting to database')    