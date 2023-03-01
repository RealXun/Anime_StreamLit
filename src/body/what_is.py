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
import pandas as pd

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



def what_is():
    #Add the cover image for the cover page. Used a little trick to center the image
             # To display the header text using css style
    user_input_1  = st.text_input("Write the user ID    ") # create a text input for the user to enter the ID of the user they want recommendations for
    try:
        users_id = int(user_input_1) # convert the input to an integer
    except ValueError:
        st.error("Please enter a valid integer.") # show an error message if the input is not a valid integer

    if isinstance(user_input_1, int): # check if the input is an integer
        st.success(f"You entered the integer: {user_input_1}") # show a success message with the input value


    # get the name of the selected anime
    selected_name = st.selectbox("Choose the anime name",sorted(recommend.names_unique()))

    anime = pd.read_csv(raw_data + "/" + "anime.csv")

    # find the anime_id of the selected anime
    selected_anime_id = anime.loc[anime['name'] == selected_name, 'anime_id'].values[0]

    user_rating  = st.text_input("Write the rating") # create a text input for the user to enter the ID of the user they want recommendations for
    try:
        users_id = int(user_rating) # convert the input to an integer
    except ValueError:
        st.error("Please enter a valid integer.") # show an error message if the input is not a valid integer

    if isinstance(user_rating, int): # check if the input is an integer
        st.success(f"You entered the integer: {user_rating}") # show a success message with the input value

    with open(body_folder + "/" + "what_is.md",'r', encoding='utf-8') as f:
        st.markdown(f.read(), unsafe_allow_html=True)

