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

#connect to db function
def connectdb():   
    connection =pymysql.connect(
        user = 'root',
        password = '',
        db = 'upwork',
        #table = 'streamlith',


    )
    #cur = connection.cursor()
    return connection

#save data to db
def save_data(text_area_1,text_area_2,box1,box2,image='',audio=''):
    #get current time
    current_time = time.localtime()
    current_time = str(time.strftime('%Y-%m-%d %H:%M:%S', current_time)).replace('-','').replace(':','').replace(' ','')
 
    #check if text area 1 and 2 are passed and also checking if one of audio or image was passed
    if text_area_2 and text_area_1 and (audio or image):
        #connect to db
        connection = connectdb()
        cur = connection.cursor()
        #try to parse and insert the image
        try:
            #open the image using pil
            
            #streamlit reads file into RAM, there is a need to use a tool that can save the file into a specified folder, thats why it was
            #opened using PIL
            
            image = Image.open(image_file)
            file_type = 'image'
            
            #get the working path and the remaining path was added. This makes sure the image is saved inside the image folder in
            #the parent directory
            ext = image_file.name.split('.')[-1]
            path = os.getcwd()+'\\images\\'
            #use the current time as the file name, to avoid duplicates name
            location = path+current_time+'.'+ext
            
            
            
            #st.write(location)
            #save the image to the image sub folder
            image.save(location)
            st.write('Data has been saved')
            
            #replaces / with . , mysql is stripping ! before it saved, sql it messes up the path by removing /
            location = location.replace('\\',"!")
            
            #pass the variables to the query
            query = f"INSERT INTO streamlith(`title`,`col_a`,`col_b`,`file_location`,`file_type`) VALUES('{text_area_1}','{box1}','{box2}','{location}','{file_type}')"
            
            #execute the query
            cur.execute(query)
            connection.commit()
        
        except:
            pass
        try:
            #st.write(audio.name)
            path = os.getcwd()+'\\audio\\'
            file_type = 'audio'
            location = path+current_time+audio.name
            
            #write the audio file to a new file in the audio sub folder
            with open(location,"wb") as f:
                    f.write(audio.getbuffer())
                    
            location = location.replace("\\","!")
            #st.write('INSERT INTO streamlith VALUES({})"'.format([box2,text_area_1,text_area_2,location,file_type)
            query = f"INSERT INTO streamlith(`title`,`col_a`,`col_b`,`file_location`,`file_type`) VALUES('{text_area_2}','{box1}','{box2}','{location}','{file_type}')"
            cur.execute(query)
            connection.commit()
            st.write('Data has been saved')
        except:
            pass
        connection.close()
    else:
        st.write('needed data is not complete')
 
    return None

#streamlit run the code from the begining and there is a need to have a persistent state because of the next button
#this value gets incremented when the next button is pressed
#without it, the value will get reinitialized on refresh and next wouldnt work
if 'current_id' not in st.session_state:
    st.session_state['current_id'] = 0

if 'current_id2' not in st.session_state:
    st.session_state['current_id2'] = 0

 

        
#menu sidebar
menu = st.sidebar.radio(
     'Select Menu:', ['Add','Show Raw','Explore','Explore Two'],index=0)
connection = connectdb()
cur = connection.cursor()

#code for Add page
if menu == "Add":
    #two column page
    col1, col2= st.columns(2)
    
    #column one content
    with col1:
        
        #select box i.e col A
        box1 = st.selectbox(
         'Col A',
         ['Col A '])
        
        #text area
        text_area_1 = st.text_area('Enter Audio Text')
        
        #image upload
        image_file = st.file_uploader("Upload Image File", type=["png","jpg"])

        
    #column two content
    with col2:     
        box2 = st.selectbox(
         'Col B',
         ['Col B'])
        text_area_2 = st.text_area('Enter Audio Text',value=' ')

        audio_file = st.file_uploader("Upload Audio File", type=["mp3"])

    #used to center the Add button
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
        #call the save data function passing the inputs as arguments
        save_data(text_area_1,text_area_2,box1,box2,image_file,audio_file)
        
#show raw page content
if menu == "Show Raw":
    multi_select_a = st.multiselect('Select A', ['col A','Apple'])
    multi_select_b = st.multiselect('Select B', ['Col B','Apple'])
  
  
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
        st.write(df)
        
if menu == "Explore":
    
    #query to select ids of rows with image file type and sorted with the updated at column
  
    max_id = "select id from streamlith where file_type='image' ORDER BY updated_at DESC"
    
    cur.execute(max_id)
    
    last_id = cur.fetchall()

    #get the state, the current position
    try:
        position = st.session_state['current_id']
        idx = last_id[position][0]
    except:
        st.write('starting from the begining')
        st.session_state['current_id'] = 0
        position = 0
        idx = last_id[position][0]
    
    
    #select row where the id == the current id in the state
    query = f"select * from streamlith where id={idx}"
    cur.execute(query)
    details = cur.fetchall()
    
    #parse the file path to the correct format, removing ! that was sused to replace /
    path = details[0][4].split("!")
    file_path = '/'.join(path)
    #st.write(file_path) 
    #open with PIL
    image = Image.open(file_path)
    st.image(image,caption='hello world')
    
#     st.write(ext)
#     st.write(details)
#     multi_select_a = st.multiselect('Select A', ['Pen','Apple'])
#     multi_select_b = st.multiselect('Select B', ['Pen','Apple'])
    
#     explore_text_area = st.text_area('Enter File Type', value="File Type")
    
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
        st.session_state['current_id'] = position+1 
    if update:
       #st.write(idx)
        query = f'select * from streamlith where id ={idx}'
       #st.write(query)
        cur.execute(query)
        details_cur = cur.fetchone()
        query = f"UPDATE streamlith SET `title` ='temp' where id={details_cur[0]}"
        #st.write(query)
        cur.execute(query)
        query = f"UPDATE streamlith SET `title` ='{details_cur[1]}' where id={details_cur[0]}"
        #st.write(query)
        cur.execute(query)
        connection.commit()
        
if menu =="Explore Two":
    #select file type
    multi_select_type_filter = st.multiselect('Select File Type', ['image','audio'])
  
    if multi_select_type_filter:
        in_values = str(multi_select_type_filter).replace('[','(').replace(']',')')
        max_id = f"select id from streamlith where file_type in {in_values} ORDER BY id ASC"
        cur.execute(max_id)
        last_id = cur.fetchall()
        
        try:
            position = st.session_state['current_id2']
            idx = last_id[position][0]
        except:
            st.write('starting from the begining')
            st.session_state['current_id'] = 0
            position = 0
            idx = last_id[position][0]
    
        
       
        query = f"select * from streamlith where file_type in {in_values} and id={idx}"
        #t.write(query)
        df = pd.read_sql(query,connection)
        st.write(df)
        
    coll1,coll2,coll3,coll4 = st.columns(4)
    
    with coll1:
        pass
    with coll2:
        updatex = st.button('Update')
    with coll3:
        nxt = st.button('Next')
    with coll4:
        pass
    if nxt:
        st.session_state['current_id2'] = position+1 
        
    if updatex:
       
        st.write(idx)
        query = f'select * from streamlith where id ={idx}'
        st.write(query)
        cur.execute(query)
        details_cur = cur.fetchone()
        query = f"UPDATE streamlith SET `title` ='temp' where id={details_cur[0]}"
        #st.write(query)
        cur.execute(query)
        query = f"UPDATE streamlith SET `title` ='{details_cur[1]}' where id={details_cur[0]}"
        #st.write(query)
        cur.execute(query)
        connection.commit()