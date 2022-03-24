import streamlit as st
from pages import Connect_Db
import pandas as pd
from PIL import Image
import time

def app():
    if 'current_id' not in st.session_state:
       st.session_state['current_id'] = 0

    if 'current_id2' not in st.session_state:
        st.session_state['current_id2'] = 0
    try:
        connection = Connect_Db.connectdb()
        cur = connection.cursor()
        st.write('connected')

        st.write('explore two')
        #select file type
        multi_select_type_filter = st.multiselect('Select File Type', ['image','audio'])
    
        if multi_select_type_filter:
            in_values = str(multi_select_type_filter).replace('[','(').replace(']',')')
            query = f"select * from streamlith where file_type in {in_values} ORDER BY id ASC"
            # cur.execute(max_id)
            # last_id = cur.fetchall()
            df = pd.read_sql(query,connection)
    
            row_number = df.id.to_list()
            #st.write(df)

            temp = st.session_state['current_id2']
            #st.write(df.shape[0])
            #st.write(temp)
            if temp+1 == df.shape[0] or temp > df.shape[0]:
                st.session_state['current_id2'] = -1
        
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
                    st.write('issue loading the media from path')
    except:
        st.write('error connecting to database')    
        
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
        #st.write(st.session_state['current_id2'])
        st.session_state['current_id2'] += 1 
        
    if updatex:
       
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