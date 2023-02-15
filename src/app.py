import streamlit as st
import os
import sys
from utils import recommend
from PIL import Image
import pickle
import requests
from pathlib import Path
from streamlit_option_menu import option_menu
from PIL import Image
import requests
from io import BytesIO



with st.sidebar:
    choose = option_menu("Anime System Recommendator", ["About", "Based on ratings", "Based on Features", "Using user ID", "Other", "Testing"],
                         icons=['house', 'camera fill', 'kanban', 'book','person lines fill', 'book'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#02ab21"},
    }
    )

if choose == "About":
    #Add the cover image for the cover page. Used a little trick to center the image
             # To display the header text using css style
    st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">About the Creator</p>', unsafe_allow_html=True)
    st.write("Aquí pondría mi introducción o lo que sea")    

    st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">About the work</p>', unsafe_allow_html=True)
    st.write("Explicar el trabajo")  
        
elif choose == "Based on ratings":
    #Add the cover image for the cover page. Used a little trick to center the image
             # To display the header text using css style
    st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
    st.title('Anime Recommendation System')
    st.title('Unsupervised user based collaborative filtering')

    # Get the user's favorite movie
    to_search = st.text_input('What anime would you like to search for recommendations?')

    # Get the number of the recomemendations the users wants
    number_of_recommendations = st.text_input("Enter an integer:")
    try:
        user_input = int(number_of_recommendations)
    except ValueError:
        st.error("Please enter a valid integer.")

    if isinstance(user_input, int):
        st.success(f"You entered the integer: {user_input}")

    def unsupervised_user_explicit_rating_based(name,n,genre,type):
        similar_animes = recommend.create_dict(recommend.unsupervised_user_based_recommender(name,n),genre,type)
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
        result = unsupervised_user_explicit_rating_based(to_search,number_of_recommendations,option_gere,option_type)

        new_dict={}
        for di in result:
            new_dict[di['name']]={}
            for k in di.keys():
                if k =='name': continue
                new_dict[di['name']][k]=di[k]
                
        num_cols = 3
        num_rows = len(result) // num_cols + 1

        for row_idx in range(num_rows):
            cols = st.columns(num_cols)
            for col_idx, key in enumerate(list(new_dict.keys())[row_idx*num_cols:(row_idx+1)*num_cols]):
                result = new_dict[key]

                # Fetch image from URL
                response = requests.get(result['cover'])
                img = Image.open(BytesIO(response.content))
                # Display image, title, and rating
                cols[col_idx].image(img, use_column_width=True)

                cols[col_idx].write(f"{result['english_title']}")
                cols[col_idx].write(f"{result['japanses_title']}")

                cols[col_idx].write(f"{result['type']}, Episodes: {int(result['episodes'])}")
                cols[col_idx].write(f"{result['duration']}")
                cols[col_idx].write(f"{result['rating']}")
                cols[col_idx].write(f"Score: {result['score']}/10")

elif choose == "Based on Features":
    #Add the cover image for the cover page. Used a little trick to center the image
             # To display the header text using css style
    st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
    st.title('Anime Recommendation System')
    st.title('Unsupervised user based collaborative filtering')


    # Get the user's favorite movie
    to_search = st.text_input('What anime would you like to search for recommendations?')

    # Get the number of the recomemendations the users wants
    number_of_recommendations = st.text_input("Enter an integer:")
    try:
        user_input = int(number_of_recommendations)
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
    if (st.button('Get the Recommendation')):
        # dataframe = load('../models/df.pkl')
        result = features_based(to_search,option_gere,option_type,number_of_recommendations)

        new_dict={}
        for di in result:
            new_dict[di['name']]={}
            for k in di.keys():
                if k =='name': continue
                new_dict[di['name']][k]=di[k]
                
        num_cols = 3
        num_rows = len(result) // num_cols + 1

        for row_idx in range(num_rows):
            cols = st.columns(num_cols)
            for col_idx, key in enumerate(list(new_dict.keys())[row_idx*num_cols:(row_idx+1)*num_cols]):
                result = new_dict[key]

                # Fetch image from URL
                response = requests.get(result['cover'])
                img = Image.open(BytesIO(response.content))
                
                # Display image, title, and rating
                cols[col_idx].image(img, use_column_width=True)

                cols[col_idx].write(f"{result['english_title']}")
                cols[col_idx].write(f"{result['japanses_title']}")

                cols[col_idx].write(f"{result['type']}, Episodes: {int(result['episodes'])}")
                cols[col_idx].write(f"{result['duration']}")
                cols[col_idx].write(f"{result['rating']}")
                cols[col_idx].write(f"Score: {result['score']}/10")

elif choose == "Using user ID":
    #Add the cover image for the cover page. Used a little trick to center the image
             # To display the header text using css style
    st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
    st.title('Anime Recommendation System')
    st.title('Supervised user rating based collaborative filtering')


     # Get the user's favorite movie
    users_id = st.slider('Choose the ID of the user you would like to see recommendations?', min_value=1, max_value=25000, value=5, step=1)
    st.write('The current number is ', users_id)

    # Get the number of the recomemendations the users wants
    number_of_recommendations = st.text_input("Enter an integer:")
    try:
        user_input = int(number_of_recommendations)
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

elif choose == "Other":
    #Add the cover image for the cover page. Used a little trick to center the image
             # To display the header text using css style
    import streamlit as st

    # Example data
    data = [{"name": "The Shawshank Redemption", "genre": "Drama", "type": "Movie"},        {"name": "The Godfather", "genre": "Crime", "type": "Movie"},        {"name": "The Godfather: Part II", "genre": "Crime", "type": "Movie"},        {"name": "The Dark Knight", "genre": "Action", "type": "Movie"},        {"name": "12 Angry Men", "genre": "Drama", "type": "Movie"},        {"name": "Schindler's List", "genre": "Biography", "type": "Movie"},        {"name": "The Lord of the Rings: The Return of the King", "genre": "Adventure", "type": "Movie"},        {"name": "Pulp Fiction", "genre": "Crime", "type": "Movie"},        {"name": "The Good, the Bad and the Ugly", "genre": "Western", "type": "Movie"}]

    # Number of results
    n = len(data)

    # Columns
    col1 = data[:n//3]
    col2 = data[n//3:2*n//3]
    col3 = data[2*n//3:]

    # Display the columns
    st.write("Column 1")
    for item in col1:
        st.write("-", item["name"], item["genre"], item["type"])

    st.write("Column 2")
    for item in col2:
        st.write("-", item["name"], item["genre"], item["type"])

    st.write("Column 3")
    for item in col3:
        st.write("-", item["name"], item["genre"], item["type"])



elif choose == "Testing":
    #Add the cover image for the cover page. Used a little trick to center the image
             # To display the header text using css style
    st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
    st.title('Anime Recommendation System')
    st.title('Unsupervised user based collaborative filtering')


    # Get the user's favorite movie
    to_search = st.text_input('What anime would you like to search for recommendations?')

    # Get the user's favorite movie
    number_of_recommendations = st.slider('How many recommendations would you like to get?', min_value=1, max_value=100, value=5, step=1)
    st.write('The current number is ', number_of_recommendations)

    def testing(name,genre,type,n):
        similar_animes = recommend.create_dict(recommend.unsupervised_user_based_recommender(name),genre,type,n)
        return similar_animes

    ## Drop down menu to select the genre
    option_gere = st.selectbox('What kind of genre would you like to search (you can choose all)',('All','Email', 'Home phone', 'Mobile phone'))
    st.write('You selected:', option_gere)

    ## Drop down menu to select the type
    option_type = st.selectbox('What type of anime would you like to search (you can choose all)',('All','TV', 'OVA', 'ONA'))
    st.write('You selected:', option_type)
    if (st.button('Get the Recommendation')):
        # dataframe = load('../models/df.pkl')
        result = testing(to_search,option_gere,option_type,number_of_recommendations)

        new_dict={}
        for di in result:
            new_dict[di['name']]={}
            for k in di.keys():
                if k =='name': continue
                new_dict[di['name']][k]=di[k]
                
        num_cols = 3
        num_rows = len(result) // num_cols + 1

        for row_idx in range(num_rows):
            cols = st.columns(num_cols)
            for col_idx, key in enumerate(list(new_dict.keys())[row_idx*num_cols:(row_idx+1)*num_cols]):
                result = new_dict[key]
                #cols[col_idx].image(result['cover_image'], width=200)
                cols[col_idx].write(f"{result['english_title']}")
                cols[col_idx].write(f"{result['japanses_title']}")
                #url = cols[col_idx].write(f"{result['img']}")
                #cols[col_idx].write(f"{result['cover']}")
                # Fetch image from URL
                response = requests.get(result['cover'])
                img = Image.open(BytesIO(response.content))
                
                # Display image, title, and rating
                cols[col_idx].image(img, use_column_width=True)

                cols[col_idx].write(f"{result['type']}, Episodes: {int(result['episodes'])}")
                cols[col_idx].write(f"{result['duration']}")
                cols[col_idx].write(f"{result['rating']}")
                cols[col_idx].write(f"Score: {result['score']}/10")

