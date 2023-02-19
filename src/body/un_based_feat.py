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


def uns_feat():
    #Add the cover image for the cover page. Used a little trick to center the image
             # To display the header text using css style
    st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
    st.title('Anime Recommendation System')
    st.title('Unsupervised user based collaborative filtering')


 # The code prompts the user to enter the name of an anime using a text input field.
 # It checks if the input is valid by verifying that it is not an empty string and does 
 # not contain only numbers. If the input is valid, the code displays a message to 
 # confirm that the input is valid. If the input is not valid, the code displays an 
 # error message asking the user to enter a string with at least one non-numeric character.
    
    to_search = st.text_input("Please write the name of the anime:")   # a text input field for user to input name of the anime to search for
    if to_search:   # checks if user has entered any value
        if to_search.isnumeric():   # checks if the value entered by the user is a number
            st.write("Input contains only numbers. Please enter a string with at least one non-numeric character.")   # displays error message if the input contains only numbers
        else:
            st.write(f"Input is valid: {to_search}")   # displays success message if the input is valid



# This code prompts the user to enter the maximum number of recommendations 
# they would like to receive, then it attempts to convert the user input into 
# an integer using a try-except block. If the user input can be converted to 
# an integer, it is stored in the variable number_of_recommendations. If the 
# conversion fails, an error message is displayed. If the user input is an 
# integer, a success message is displayed.

    # Prompts the user to enter a maximum number of recommendations 
    # they want to get and stores the input in the 'user_input' variable.
    user_input  = st.text_input("What is the maximum number of recommendations you would like to get?:") 

    # The input is then converted into an integer type and stored in the 
    # 'number_of_recommendations' variable using the 'int' function. 
    try:
        number_of_recommendations = int(user_input)
    except ValueError:
        st.error("Please enter a valid integer.")

    # If the input is successfully converted to an integer, a success message 
    # is displayed with the integer value using the 'st.success' function.
    if isinstance(user_input, int):
        st.success(f"You entered the integer: {user_input}")

    if isinstance(user_input, int):
        st.success(f"You entered the integer: {user_input}")

    def features_based(name,genre,type,method,n):
        similar_animes = recommend.create_dict(recommend.print_similar_animes(name),genre,type,method,n)
        return similar_animes



# The code presents a dropdown menu to select between two filtering methods ("and" and "or"). 
# Depending on the method chosen, the user can select one or more genres and one or more types 
# of anime using checkboxes. If the "and" method is chosen, the user can only select one type 
# of anime, while the "or" method allows the user to select multiple types. The selected genres 
# and types are stored in the selected_genre and selected_type variables.

    method = st.selectbox("Choose a filtering method", ["and", "or"]) # prompts user to choose filtering method either 'and' or 'or'

    if method == "or": # if filtering method is 'or'

        option_genre = ['Drama', 'Romance', 'School', 'Supernatural', 'Action', # list of anime genres
        'Adventure', 'Fantasy', 'Magic', 'Military', 'Shounen', 'Comedy',
        'Historical', 'Parody', 'Samurai', 'Sci-Fi', 'Thriller', 'Sports',
        'Super Power', 'Space', 'Slice of Life', 'Mecha', 'Music',
        'Mystery', 'Seinen', 'Martial Arts', 'Vampire', 'Shoujo', 'Horror',
        'Police', 'Psychological', 'Demons', 'Ecchi', 'Josei',
        'Shounen Ai', 'Game', 'Dementia', 'Harem', 'Cars', 'Kids',
        'Shoujo Ai', 'Hentai', 'Yaoi', 'Yuri']
        option_type = ['ALL','Movie', 'TV', 'OVA', 'Special', 'Music', 'ONA'] # list of anime types

        selected_genre = st.multiselect('Select genre', option_genre) # prompts user to select genres
        selected_type = st.multiselect('Select type', option_type) # prompts user to select anime types

    else: # if filtering method is 'and'
        st.text("AND method would match any gender you input with the type.\n More Genres, more results \n Type should be one, there is no anime with two types at once")

        option_genre = ['Drama', 'Romance', 'School', 'Supernatural', 'Action', # list of anime genres
        'Adventure', 'Fantasy', 'Magic', 'Military', 'Shounen', 'Comedy',
        'Historical', 'Parody', 'Samurai', 'Sci-Fi', 'Thriller', 'Sports',
        'Super Power', 'Space', 'Slice of Life', 'Mecha', 'Music',
        'Mystery', 'Seinen', 'Martial Arts', 'Vampire', 'Shoujo', 'Horror',
        'Police', 'Psychological', 'Demons', 'Ecchi', 'Josei',
        'Shounen Ai', 'Game', 'Dementia', 'Harem', 'Cars', 'Kids',
        'Shoujo Ai', 'Hentai', 'Yaoi', 'Yuri']
        option_type = ['Movie', 'TV', 'OVA', 'Special', 'Music', 'ONA'] # list of anime types

        selected_genre = st.multiselect('Select genre', option_genre) # prompts user to select genres
        selected_type = st.multiselect('Select type', option_type, max_selections=1) # prompts user to select anime types, allowing only one selection



    criteria_selected = to_search and user_input and selected_genre and selected_type



    # Enable button if both criteria are selected
    if st.button('Get the Recommendation', disabled=not criteria_selected):
        
        # dataframe = load('../models/df.pkl')
        stream.features_based(to_search, selected_genre, selected_type,method,number_of_recommendations,"features_based")
    