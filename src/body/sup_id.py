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


def user_id():
#Add the cover image for the cover page. Used a little trick to center the image
             # To display the header text using css style
    st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
    st.title('Anime Recommendation System')
    st.title('Supervised user rating based collaborative filtering')


     # Get the user's favorite movie
    user_input  = st.text_input("Choose the ID of the user you would like to see recommendations?")
    try:
        users_id = int(user_input)
    except ValueError:
        st.error("Please enter a valid integer.")

    if isinstance(user_input, int):
        st.success(f"You entered the integer: {user_input}")

    def super_ratings_based(id,n,genre,type):
        similar_animes =recommend.df_recommendation(id,n,genre,type)
        return similar_animes

    # Get the number of the recomemendations the users wants
    user_input  = st.text_input("Write how many recommendations you want to get:")
    st.text("Note that the results are based on the filter. More filters might lead to less recommendations")
    try:
        number_of_recommendations = int(user_input)
    except ValueError:
        st.error("Please enter a valid integer.")

    if isinstance(user_input, int):
        st.success(f"You entered the integer: {user_input}")

    def super_ratings_based(id,n,genre,type):
        similar_animes =recommend.df_recommendation(id,n,genre,type)
        return similar_animes


    ## Drop down menu to select the genre
    option_gere = st.selectbox('What kind of genre would you like to search (you can choose all)',
        ('All','Drama', 'Romance', 'School', 'Supernatural', 'Action',
       'Adventure', 'Fantasy', 'Magic', 'Military', 'Shounen', 'Comedy',
       'Historical', 'Parody', 'Samurai', 'Sci-Fi', 'Thriller', 'Sports',
       'Super Power', 'Space', 'Slice of Life', 'Mecha', 'Music',
       'Mystery', 'Seinen', 'Martial Arts', 'Vampire', 'Shoujo', 'Horror',
       'Police', 'Psychological', 'Demons', 'Ecchi', 'Josei',
       'Shounen Ai', 'Game', 'Dementia', 'Harem', 'Cars', 'Kids',
       'Shoujo Ai', 'Hentai', 'Yaoi', 'Yuri'))
    st.write('You selected:', option_gere)

    ## Drop down menu to select the type
    option_type = st.selectbox('What type of anime would you like to search (you can choose all)',
    ('All','Movie', 'TV', 'OVA', 'Special', 'Music', 'ONA'))
    st.write('You selected:', option_type)
    if (st.button('Get the Recommendation')):
        # dataframe = load('../models/df.pkl')
        result = super_ratings_based(users_id,number_of_recommendations,option_gere,option_type)
        st.dataframe(result)
        st.balloons()