import streamlit as st
import os
import sys
from utils import recommend
from PIL import Image
import pickle
import requests
from pathlib import Path
from PIL import Image
import requests
from io import BytesIO
import glob

PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
data_folder = (PROJECT_ROOT + "/" + "data")
body_folder = (PROJECT_ROOT + "/" + "body")

saved_models_folder = (data_folder + "/" + "saved_models")
raw_data = (data_folder + "/" + "_raw")
processed_data = (data_folder + "/" + "processed")
content_based_supervised_data = (data_folder + "/" + "processed" + "/" + "content_based_supervised")
images = (PROJECT_ROOT + "/" + "images")
cover_images = (images + "/" + "Cover_images")



def it_is_about():
    #Add the cover image for the cover page. Used a little trick to center the image
             # To display the header text using css style

    st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">About the work</p>', unsafe_allow_html=True)
    st.write("The goal of this project is that according to the user's anime viewing history we can recommend a list of anime that suits their tastes.\nIn order to do this we are going to create 3 types or recommendation system")

    with open(body_folder + "about_text.md",'r') as f:
        readme_line = f.readlines()
        readme_buffer = []
        resource_files = [os.path.basename(x) for x in glob.glob(f'images/*')]
        # resource_files
    for line in readme_line :
        readme_buffer.append(line) 
        for image in resource_files:
            if image in line:
                st.markdown(''.join(readme_buffer[:-1])) 
                st.image(f'Resources/{image}')
                readme_buffer.clear()
                
    st.markdown(''.join(readme_buffer))