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
    user_input  = st.text_input("What is the maximum number of recommendations you would like to get?:")
    try:
        number_of_recommendations = int(user_input)
    except ValueError:
        st.error("Please enter a valid integer.")

    if isinstance(user_input, int):
        st.success(f"You entered the integer: {user_input}")

    def features_based(name,genre,type,method,n):
        similar_animes = recommend.create_dict(recommend.print_similar_animes(name),genre,type,method,n)
        return similar_animes

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
        option_type = ['Movie', 'TV', 'OVA', 'Special', 'Music', 'ONA']

        # Create the multiselect widgets
        selected_genre = st.multiselect('Select genre', option_genre)
        selected_type = st.multiselect('Select type', option_type)
    else:
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
        selected_type = st.multiselect('Select type', option_type)

    criteria_selected = to_search and user_input and selected_genre and selected_type

    # Enable button if both criteria are selected
    if st.button('Get the Recommendation', disabled=not criteria_selected):
        # dataframe = load('../models/df.pkl')
        result = features_based(to_search, selected_genre, selected_type,method,number_of_recommendations)
        if result is not None: # result coming from the dictionary that get the rsults from filtering
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
                            cols[col_idx].write(f"**{result['japanese_title']}")
                        if 'type' in result:
                            cols[col_idx].write(f"**Type:** {result['type']}")
                        if 'episodes' in result:
                            cols[col_idx].write(f"**Episodes:** {int(result['episodes'])}")
                        if 'duration' in result:
                            cols[col_idx].write(f"**Duration:** {result['duration']}")
                        if 'rating' in result:
                            cols[col_idx].write(f"**Rating:** {result['rating']}")
                        if 'score' in result:
                            cols[col_idx].write(f"**Score:** {result['score']}/10")
        else:
            st.write("Sorry, there is no matches for this, try again with different filters.")
    else :
        st.write("Please enter anime name and number of recommendations to get the recommendation.")