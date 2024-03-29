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
import pandas as pd
import xlsxwriter
import base64
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
data_folder = (PROJECT_ROOT + "/" + "data")

saved_models_folder = (data_folder + "/" + "saved_models")
raw_data = (data_folder + "/" + "_raw")
processed_data = (data_folder + "/" + "processed")
content_based_supervised_data = (data_folder + "/" + "processed" + "/" + "content_based_supervised")
output = BytesIO()
output = BytesIO()


def to_excel(df):
    # Create a BytesIO object to store the Excel file as bytes
    output = BytesIO()
    
    # Create a Pandas ExcelWriter object with the XlsxWriter engine
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    
    # Write the DataFrame to the Excel file, specifying the sheet name and that the index should not be included
    df.to_excel(writer, index=False, sheet_name='Recommendations')
    
    # Get a reference to the XlsxWriter workbook and worksheet objects
    workbook = writer.book
    worksheet = writer.sheets['Recommendations']
    
    # Create a format for numbers with two decimal places
    format1 = workbook.add_format({'num_format': '0.00'}) 
    
    # Apply the number format to the first column of the worksheet
    worksheet.set_column('A:A', None, format1)  
    
    # Save the Excel file and get its contents as bytes
    writer.close()
    processed_data = output.getvalue()
    
    # Return the Excel file contents as bytes
    return processed_data



def uns_feat():
    #Add the cover image for the cover page. Used a little trick to center the image
             # To display the header text using css style
    st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font"> Unsupervised content based recommendation system</p>', unsafe_allow_html=True)



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
            anime = pd.read_csv(processed_data + "/" + "_anime_to_compare_with_name.csv")
            # Find the closest title in the anime dataset to the user's query
            closest_title, distance_score = recommend.finding_the_closest_title(to_search,anime)
            if distance_score == 100:
                st.write(f"Input is valid: {to_search}")   # displays success message if the input is valid
            else:
                st.write(f"I guess you misspelled the name\n and you looking similitudes for the anime named:   {closest_title}")



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



# The code presents a dropdown menu to select between two filtering methods ("and" and "or"). 
# Depending on the method chosen, the user can select one or more genres and one or more types 
# of anime using checkboxes. If the "and" method is chosen, the user can only select one type 
# of anime, while the "or" method allows the user to select multiple types. The selected genres 
# and types are stored in the selected_genre and selected_type variables.

    method = st.selectbox("Choose a filtering method", ["and", "or"]) # prompts user to choose filtering method either 'and' or 'or'

    if method == "or": # if filtering method is 'or'

        option_genre = ['ALL','Drama', 'Romance', 'School', 'Supernatural', 'Action', # list of anime genres
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



    def features_based(name,genre,type,method,n):
        similar_animes = recommend.create_dict(recommend.print_similar_animes(name),genre,type,method,n)
        return similar_animes



    criteria_selected = to_search and user_input and selected_genre and selected_type



    # Create a visual indicator to show if both criteria are selected
    if criteria_selected:
        st.success('All criteria are selected. You can click now.')
    else:
        st.warning('Please select All criteria to get recommendations')



# Displays anime recommendations based on selected criteria. It uses the Streamlit library 
# to create a user interface with input fields for selecting anime genre, type, and method 
# for recommendation. When the user clicks the "Get the Recommendation" button, the script 
# retrieves anime recommendations based on the selected criteria using a pre-trained model. 
# It then displays the recommendations in a grid of images and text information such as 
# English and Japanese titles, type, episodes, duration, rating, and score. If there are 
# no recommendations to display or the user has not entered enough information, the script 
# prompts the user accordingly.

    # Enable button if both criteria are selected
    if st.button('Get the Recommendation', disabled=not criteria_selected):
        with st.spinner('Generating recommendations...'):
            result = features_based(to_search, selected_genre, selected_type,method,number_of_recommendations)
            if result is not None: 

                # Define a dataframe from the result list
                df = pd.DataFrame(result)

                # Call the function to create a excel file
                df_xlsx = to_excel(df)

                # Button to download the excel file
                st.download_button(label='📥 Download Recommendations',
                                                data=df_xlsx ,
                                                file_name= 'Recommendations.xlsx')

                # If the recommendation results are not empty, create a new dictionary to store them
                new_dict={}
                for di in result:
                    # For each recommendation, add a new entry to the dictionary using the anime name as the key
                    new_dict[di['name']]={}
                    # Copy all other properties of the recommendation into the dictionary entry for that anime
                    for k in di.keys():
                        if k =='name': continue
                        new_dict[di['name']][k]=di[k]


                # Determine how many rows and columns are needed to display the recommendations
                num_cols = 5
                num_rows = len(result) // num_cols + 1

                # Loop through each row of recommendations
                for row_idx in range(num_rows):
                    # Create a new set of columns to display each recommendation
                    cols = st.columns(num_cols)
                    # Loop through each column and get the key (anime name) for that column's recommendation
                    for col_idx, key in enumerate(list(new_dict.keys())[row_idx*num_cols:(row_idx+1)*num_cols]):
                        # Get the recommendation for the current anime
                        result = new_dict[key]

                        # Get the cover image for the anime from the recommendation data
                        response = requests.get(result['cover'])
                        img = Image.open(BytesIO(response.content))

                        # Display the anime information in a container within the current column
                        with cols[col_idx].container():
                            cols[col_idx].image(img, use_column_width=True)
                            cols[col_idx].write(f"**{result['english_title']}**")
                            if 'japanese_title' in result:
                                cols[col_idx].write(f"**{result['japanese_title']}")
                            if 'type' in result:
                                cols[col_idx].write(f"**Type:** {result['type']}")
                            if 'episodes' in result:
                                cols[col_idx].write(f"**Episodes:** {result['episodes']}")
                            if 'duration' in result:
                                cols[col_idx].write(f"**Duration:** {result['duration']}")
                            if 'rating' in result:
                                cols[col_idx].write(f"**Rating:** {result['rating']}")
                            if 'score' in result:
                                cols[col_idx].write(f"**Score:** {result['score']}/10")
                            # Display the estimated score for the recommendation
                            if 'Estimate_Score' in result:
                                cols[col_idx].write(f"**{float(result['Estimate_Score'])}**")

            else:
                # If there are no recommendations to display, inform the user
                st.write("Sorry, there is no matches for this, try again with different filters.")
                
            # If the user has not entered enough information to get recommendations, prompt them to do so
    else :
        st.write("")