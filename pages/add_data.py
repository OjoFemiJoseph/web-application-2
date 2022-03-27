import streamlit as st
import time
from PIL import Image
import os
from pages import Connect_Db

class add_data():
    #save data to db
    def save_data(self):#text_area_1,text_area_2,box1,box2,image='',audio=''):
        #get current time
        text_area_2 = self.text_area_2
        text_area_1 = self.text_area_1
        audio_file = self.audio_file
        image_file = self.image_file
        box1 = self.box1
        box2 = self.box2

        current_time = time.localtime()
        current_time = str(time.strftime('%Y-%m-%d %H:%M:%S', current_time)).replace('-','').replace(':','').replace(' ','')
    
        #check if text area 1 and 2 are passed and also checking if one of audio or image was passed
        if len(text_area_2)>1 and text_area_1 or (audio_file or image_file):
            #connect to db
            try:
                connection = Connect_Db.connectdb()
                cur = connection.cursor()
                #st.write('connected')
                #try to parse and insert the image
            
                #open the image using pil
                
                #streamlit reads file into RAM, there is a need to use a tool that can save the file into a specified folder, thats why it was
                #opened using PIL
                if image_file:
                    try:
                        #st.write('file_type')
                        image = Image.open(image_file)
                        file_type = 'image'
                        
                        #get the working path and the remaining path was added. This makes sure the image is saved inside the image folder in
                        #the parent directory
                        ext = image_file.name.split('.')[-1]
                        ext_dot = '.'+ext
                        #use the current time as the file name, to avoid duplicates name
                        location = current_time+'.'+ext
                        path = os.path.join(os.getcwd(),'images',location)
                        
                        
                        
                        
                        #st.write(path)
                        #save the image to the image sub folder
                        image.save(path)
                        st.write('Data has been saved')
                        
                        #replaces / with . , mysql is stripping ! before it saved, sql it messes up the path by removing /
                        location = path.replace('\\',"!")
                        
                        #pass the variables to the query
                        query = f"INSERT INTO streamlith(`title`,`col_a`,`col_b`,`file_location`,`file_type`) VALUES('{text_area_1}','{box1}','{box2}','{location}','{file_type}')"
#                       Needs another column for text_area_2
                        
                        #execute the query
                        cur.execute(query)
                        connection.commit()
                    except:
                        pass

                if audio_file:
                    try:
                        #st.write(audio_file.name)
                        path = os.path.join(os.getcwd(),'audio',audio_file.name)
                        file_type = 'audio'
                        #location = path+current_time+audio_file.name
                        
                        #write the audio file to a new file in the audio sub folder
                        with open(path,"wb") as f:
                                f.write(audio_file.getbuffer())
                                
                        location = path.replace("\\","!")
                        #st.write('INSERT INTO streamlith VALUES({})"'.format([box2,text_area_1,text_area_2,location,file_type)
                        query = f"INSERT INTO streamlith(`title`,`col_a`,`col_b`,`file_location`,`file_type`) VALUES('{text_area_2}','{box1}','{box2}','{location}','{file_type}')"
                        cur.execute(query)
                        connection.commit()
                        st.write('Data has been saved')
                
                    except:
                        pass    

                connection.close()
            except:
                st.write('error connecting to database or path issues')
        else:
            st.write('needed data is not complete')
    
        return None

    def app(self):
        st.write('add data')
        #two column page
        col1, col2= st.columns(2)
        
        #column one content
        with col1:
            
            #select box i.e col A
            self.box1 = st.selectbox(
            'Col A',
            ['Breakfast','Lunch','Dinner'])
            
            #text area
            self.text_area_1 = st.text_area('Enter Image Text')
            
            #image upload
            self.image_file = st.file_uploader("Upload Image File", type=["png","jpg"])

            
        #column two content
        with col2:     
            self.box2 = st.selectbox(
            'Col B',
            ['Major','Minor','Lieutanant','General','chief'])
            self.text_area_2 = st.text_area('Enter Audio Text',value=' ')

            self.audio_file = st.file_uploader("Upload Audio File", type=["mp3"])

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
            #st.write('i was clicked')
            #call the save data function passing the inputs as arguments
            self.save_data()#text_area_1,text_area_2,box1,box2,image_file,audio_file)
