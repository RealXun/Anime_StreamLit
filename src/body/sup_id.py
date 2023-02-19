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
from utils import stream


def user_id():
#Add the cover image for the cover page. Used a little trick to center the image
             # To display the header text using css style
    st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
    st.title('Anime Recommendation System')
    st.title('Supervised user rating based collaborative filtering')


     # Get the user's favorite movie
    user_input_1  = st.text_input("Choose the ID of the user you would like to see recommendations?")
    try:
        users_id = int(user_input_1)
    except ValueError:
        st.error("Please enter a valid integer.")

    if isinstance(user_input_1, int):
        st.success(f"You entered the integer: {user_input_1}")

    # Get the number of the recomemendations the users wants
    user_input  = st.text_input("What is the maximum number of recommendations you would like to get?:")
    try:
        number_of_recommendations = int(user_input)
    except ValueError:
        st.error("Please enter a valid integer.")

    if isinstance(user_input, int):
        st.success(f"You entered the integer: {user_input}")

    

    # Define your filtering method (and/or)
    method = st.selectbox("Choose a filtering method", ["and", "or"])
     # Create the multiselect widgets

    if method == "or":

        # Define the options for the multiselects
        option_genre = ['Drama', 'Romance', 'School', 'Supernatural', 'Action',
        'Adventure', 'Fantasy', 'Magic', 'Military', 'Shounen', 'Comedy',
        'Historical', 'Parody', 'Samurai', 'Sci-Fi', 'Thriller', 'Sports',
        'Super Power', 'Space', 'Slice of Life', 'Mecha', 'Music',
        'Mystery', 'Seinen', 'Martial Arts', 'Vampire', 'Shoujo', 'Horror',
        'Police', 'Psychological', 'Demons', 'Ecchi', 'Josei',
        'Shounen Ai', 'Game', 'Dementia', 'Harem', 'Cars', 'Kids',
        'Shoujo Ai', 'Hentai', 'Yaoi', 'Yuri']
        option_type = ['ALL','Movie', 'TV', 'OVA', 'Special', 'Music', 'ONA']

        # Create the multiselect widgets
        selected_genre = st.multiselect('Select genre', option_genre)
        selected_type = st.multiselect('Select type', option_type)
    else:
        st.text("AND method would match any gender you input with the type.\n More Genres, more results \n Type should be one, there is no anime with two types at once")
        # Define the options for the multiselects
        option_genre = ['Drama', 'Romance', 'School', 'Supernatural', 'Action',
        'Adventure', 'Fantasy', 'Magic', 'Military', 'Shounen', 'Comedy',
        'Historical', 'Parody', 'Samurai', 'Sci-Fi', 'Thriller', 'Sports',
        'Super Power', 'Space', 'Slice of Life', 'Mecha', 'Music',
        'Mystery', 'Seinen', 'Martial Arts', 'Vampire', 'Shoujo', 'Horror',
        'Police', 'Psychological', 'Demons', 'Ecchi', 'Josei',
        'Shounen Ai', 'Game', 'Dementia', 'Harem', 'Cars', 'Kids',
        'Shoujo Ai', 'Hentai', 'Yaoi', 'Yuri']
        option_type = ['Movie', 'TV', 'OVA', 'Special', 'Music', 'ONA']

        # Create the multiselect widgets
        selected_genre = st.multiselect('Select genre', option_genre)
        selected_type = st.multiselect('Select type', option_type, max_selections=1)

    criteria_selected = user_input_1 and user_input and selected_genre and selected_type

    # Enable button if both criteria are selected
    if st.button('Get the Recommendation', disabled=not criteria_selected):
        stream.results(users_id,number_of_recommendations,selected_genre,selected_type, method)

