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


def uns_feat():
    #Add the cover image for the cover page. Used a little trick to center the image
             # To display the header text using css style
    st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
    st.title('Anime Recommendation System')
    st.title('Unsupervised user based collaborative filtering')


    # Get the user's favorite movie
    to_search = st.text_input("Please write the name of the anime:")
    if to_search:
        if to_search.isnumeric():
            st.write("Input contains only numbers. Please enter a string with at least one non-numeric character.")
        else:
            st.write(f"Input is valid: {to_search}")

    # Get the number of the recomemendations the users wants
    user_input  = st.text_input("Write how many recommendations you want to get:")
    st.text("Note that the results are based on the filter.\n More filters might lead to less recommendations")
    try:
        number_of_recommendations = int(user_input)
    except ValueError:
        st.error("Please enter a valid integer.")

    if isinstance(user_input, int):
        st.success(f"You entered the integer: {user_input}")

    def features_based(name,genre,type,n):
        similar_animes = recommend.create_dict(recommend.print_similar_animes(name),genre,type,n)
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
    # Check if both criteria have been selected
    criteria_selected = to_search and user_input

    # Enable button if both criteria are selected
    if st.button('Get the Recommendation', disabled=not criteria_selected):
        # dataframe = load('../models/df.pkl')
        result = result = features_based(to_search,option_gere,option_type,number_of_recommendations)

        new_dict={}
        for di in result:
            new_dict[di['name']]={}
            for k in di.keys():
                if k =='name': continue
                new_dict[di['name']][k]=di[k]
                    
        num_cols = 5
        num_rows = len(result) // num_cols + 1

        for row_idx in range(num_rows):
            cols = st.columns(num_cols)
            for col_idx, key in enumerate(list(new_dict.keys())[row_idx*num_cols:(row_idx+1)*num_cols]):
                result = new_dict[key]

                # Fetch image from URL
                response = requests.get(result['cover'])
                img = Image.open(BytesIO(response.content))

                # Display title and other details in a card
                with cols[col_idx].container():
                    cols[col_idx].image(img, use_column_width=True)
                    cols[col_idx].write(f"**{result['english_title']}**")
                    if 'japanese_title' in result:
                        cols[col_idx].write(f"**{result['japanese_title']}**")
                    cols[col_idx].write(f"**Type:** {result['type']}  **Episodes:** {int(result['episodes'])}")
                    cols[col_idx].write(f"**Duration:** {result['duration']}  **Rating:** {result['rating']}")
                    cols[col_idx].write(f"**Score:** {result['score']}/10")
    else :
        st.write("Please enter anime name and number of recommendations to get the recommendation.")