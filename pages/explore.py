import streamlit as st
from PIL import Image
import pandas as pd
from matplotlib import pyplot as plt
import streamlit.components.v1 as components  # Import Streamlit
import datetime
import plotly.express as px
import pymysql
from sqlalchemy import create_engine
from pages import Connect_Db
import time


def app():
    if 'current_id' not in st.session_state:
        st.session_state['current_id'] = 0

    if 'current_id2' not in st.session_state:
        st.session_state['current_id2'] = 0
    image_filter_a = st.multiselect('Select A', ['Breakfast','Lunch','Dinner'])
    image_filter_b = st.multiselect('Select B', ['Major','Minor','Lieutanant','General','chief'])
    #query to select ids of rows with image file type and sorted with the updated at column
    try:
        connection = Connect_Db.connectdb()
        cur = connection.cursor()
        st.write('connected')

        if image_filter_a and not image_filter_b:
            #add to format it because of sql, IN works with tuple shape. that is , the values has to be passed like this (a,b,c)
            in_values = str(image_filter_a).replace('[','(').replace(']',')')
        
            query = f"select * from streamlith where col_a in {in_values}"
            
            df = pd.read_sql(query,connection)
            #st.write(df)
            row_number = df.id.to_list()
        elif image_filter_b and not image_filter_a:
            in_values = str(image_filter_b).replace('[','(').replace(']',')')
            query = f"select * from streamlith where col_b in {in_values}"
            df = pd.read_sql(query,connection)
            #st.write(df)
            row_number = df.id.to_list()
        elif image_filter_b and image_filter_a:
            in_values_a = str(image_filter_a).replace('[','(').replace(']',')')
            in_values_b = str(image_filter_b).replace('[','(').replace(']',')')
            query = f"select * from streamlith where col_b in {in_values_b} and col_a in {in_values_a}"
            df = pd.read_sql(query,connection)
            #st.write(df)
            row_number = df.id.to_list()

        if image_filter_a or image_filter_b:
            temp = st.session_state['current_id']
            #st.write(df.shape[0])
            #st.write(temp)
            if temp+1 == df.shape[0] or temp > df.shape[0]:
                st.session_state['current_id'] = -1
        
            if temp < df.shape[0]:
                one_row = df[temp:temp+1]
                one_row = one_row[one_row.columns[:-1]]
            else:
                one_row = df[temp:]
                one_row = one_row[one_row.columns[:-1]]
            if one_row.shape[0]>0:
                st.write(one_row)
                idx = one_row.id.to_list()[0]

                path = one_row['file_location'].to_list()[0].replace('!','/')
                #st.write(path) 
                #open with PIL
                try:
                    if 'image' in path:
                        image = Image.open(path)
                        st.image(image.resize((300, 300)))
                    else:
                        audio_file = open(path, 'rb')
                        audio_bytes = audio_file.read()

                        st.audio(audio_bytes)
                except:
                    st.write('issue loading the media')
    except:
        st.write('error connecting to database')
    coll1,coll2,coll3,coll4 = st.columns(4)
    with coll1:
        pass
    with coll2:
        update = st.button('Update')
    with coll3:
        nxt = st.button('Next')
    with coll4:
        pass


    if nxt:
        #st.write(st.session_state['current_id'])
        st.session_state['current_id'] += 1 
    if update:
        current_time = time.localtime()
        current_time = str(time.strftime('%Y-%m-%d %H:%M:%S', current_time)).replace('-','').replace(':','').replace(' ','')
        try:
            idx = row_number[st.session_state['current_id']-1]
            #st.write(idx)
            query = f"UPDATE streamlith SET `update_column` ='{current_time}' where id={idx}"
            #st.write(query)
            cur.execute(query)
            connection.commit()
            query = f"UPDATE streamlith SET `update_column` ='{one_row['title'].to_list()[0]}' where id={idx}"
            #st.write(query)
            cur.execute(query)
            connection.commit()
            st.session_state['current_id'] += 1 
        except:
            pass
    try:
        connection.close()
    except:
        pass