import streamlit as st
from PIL import Image
import pandas as pd
from matplotlib import pyplot as plt
import streamlit.components.v1 as components  # Import Streamlit
import time
import plotly.express as px
import sqlite3
import pymysql
from datetime import datetime
from sqlalchemy import create_engine
import os

# Text/Title
st.title("Interactive Web Application 2")

def connectdb():
    
    connection =pymysql.connect(
        user = 'root',
        password = '',
        db = 'upwork',
        #table = 'streamlith',


    )
    #cur = connection.cursor()
    return connection

def save_data(image,audio,text_area_1,text_area_2,box1,box2):
    current_time = time.localtime()
    current_time = str(time.strftime('%Y-%m-%d %H:%M:%S', current_time)).replace('-','').replace(':','').replace(' ','')
 
    if image and text_area_1 and audio and text_area_2:
        connection = connectdb()
        cur = connection.cursor()
        image = Image.open(image_file)
        file_type = 'image'
        path = os.getcwd()+'\\images\\'
        location = path+current_time+image_file.name
        location = location.replace('\\',".")
        st.write(location)
        #image.save(location)
        #st.write('Data has been saved')
        query = f"INSERT INTO streamlith(`title`,`col_a`,`col_b`,`file_location`,`file_type`) VALUES('{box1}','{text_area_1}','{text_area_2}','{location}','{file_type}')"
        #st.write('INSERT INTO streamlith VALUES({})"'.format([box1,text_area_1,text_area_2,location,file_type]))
        cur.execute(query)
        connection.commit()
   
        #st.write(audio.name)
        path = os.getcwd()+'\\audio\\'
        file_type = 'audio'
        location = path+current_time+audio.name
        location = location.replace("\\",".")
        with open(location,"wb") as f:
                f.write(audio.getbuffer())
        #st.write('INSERT INTO streamlith VALUES({})"'.format([box2,text_area_1,text_area_2,location,file_type)
        query = f"INSERT INTO streamlith(`title`,`col_a`,`col_b`,`file_location`,`file_type`) VALUES('{box2}','{text_area_1}','{text_area_2}','{location}','{file_type}')"
        cur.execute(query)
        connection.commit()
        #st.write('Data has been saved')
    else:
        st.write('needed data is not complete')
        
#menu sidebar
menu = st.sidebar.radio(
     'Select Menu:', ['Add','Show Raw','Explore ','Explore Two'],index=0)


if menu == "Add":
    col1, col2= st.columns(2)
    
    with col1:
        box1 = st.selectbox(
         'Col A',
         ['Col A '])
        
        text_area_1 = st.text_area('Enter Audio Text', value="Enter Text")
        
        image_file = st.file_uploader("Upload Image File", type=["png","jpg"])
#         if image_file:
#             image = Image.open(image_file)

#             st.image(image, caption=image_file.name)
#             #print(type(image_file))
#             path = os.getcwd()+'//images//'
#             image.save(path+image_file.name+str(datetime.now()))
        
    with col2:     
        box2 = st.selectbox(
         'Col B',
         ['Col B'])
        text_area_2 = st.text_area('Enter Video Text', value="Enter Text")

        audio_file = st.file_uploader("Upload Video File", type=["mp3"])
#         if video_file:
#             with open('test1.mp3',"wb") as f:
#                 f.write(video_file.getbuffer())
    coll1,coll2,coll3,coll4 = st.columns(4)
    with coll1:
        pass
    with coll2:
        pass
    with coll3:
        save = st.button('Add')
    with coll4:
        pass
    if save:
        save_data(image_file,audio_file,text_area_1,text_area_2,box1,box2)
        
if menu == "Show Raw":
    multi_select_a = st.multiselect('Select A', ['Pen','Apple'])
    multi_select_b = st.multiselect('Select B', ['Pen','Apple'])
    conn = connectdb()
    df = pd.read_sql('select * from streamlith',conn)
    st.write(df)
if menu == "Explore":
    st.write('3')
if menu =="Explore Two":
    st.write('4')