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

def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()

def it_is_about():
    #Add the cover image for the cover page. Used a little trick to center the image
             # To display the header text using css style

    st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">About the work</p>', unsafe_allow_html=True)
    st.write("The goal of this project is that according to the user's anime viewing history we can recommend a list of anime that suits their tastes.\nIn order to do this we are going to create 3 types or recommendation system")
    intro_markdown = read_markdown_file("about_text.md")
    st.markdown(intro_markdown, unsafe_allow_html=True)

    with open(body_folder + "about_text.md",'r') as f:
        st.markdown(f.read(), unsafe_allow_html=True)