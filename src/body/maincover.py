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

def main_cover():

    #Add the cover image for the cover page. Used a little trick to center the image
             # To display the header text using css style

    st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">MAIN COVER</p>', unsafe_allow_html=True)
    st.write("MAIN COVER")  