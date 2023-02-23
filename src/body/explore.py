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
import joblib
import plotly.express as px


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




def explore_data():
    import streamlit as st
    import pandas as pd

    #Opening cleaned df using Pickle
    fichero = open(raw_data + "/" +"anime.pkl","rb")
    df = pickle.load(fichero)
    fichero.close()


    #Add the cover image for the cover page. Used a little trick to center the image
             # To display the header text using css style

    st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)

    st.markdown('<p class="font">Hi there!!👋 Take a look at my repositories and let\'s get in touch!</p>', unsafe_allow_html=True)

    # Opening cleaned df using Pickle
    anime_df = joblib.load(raw_data + "/" + "anime_eda.pkl")
    st.dataframe(anime_df)

    # Create a sample dataframe with the given column types and values

    # Create a pie chart using Plotly Express
    fig = px.pie(df, values='Count', names='Type', title='Distribution of Anime Types')

    # Display the pie chart in Streamlit
    st.plotly_chart(fig)