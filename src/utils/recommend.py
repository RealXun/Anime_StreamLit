# data analysis and wrangling
import pandas as pd
import numpy as np
import warnings
import os
import re
import sys
import warnings
import joblib
import pickle
from fastparquet import write
from fuzzywuzzy import fuzz
from pathlib import Path
import zipfile
import shutil

from sklearn.preprocessing import MinMaxScaler


from surprise import Dataset, Reader, NormalPredictor, KNNBasic, KNNWithMeans, SVD, accuracy
from surprise.model_selection import cross_validate
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import NearestNeighbors

pd.options.mode.chained_assignment = None  # default='warn'

#Preparing folder variables
#os.chdir(os.path.dirname(sys.path[0])) # This command makes the notebook the main path and can work in cascade.

PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
data_folder = (PROJECT_ROOT + "/" + "data")

saved_models_folder = (data_folder + "/" + "saved_models")
raw_data = (data_folder + "/" + "_raw")
processed_data = (data_folder + "/" + "processed")
content_based_supervised_data = (data_folder + "/" + "processed" + "/" + "content_based_supervised")



shutil.unpack_archive(processed_data + "/" + "features_user_based_unsupervised.zip",processed_data)
shutil.unpack_archive(processed_data + "/" + "pivot_user_based_unsupervised.zip",processed_data)

############################################################
############################################################
#                                                          #
#--------------------- For all models ---------------------#
#                                                          #
############################################################
############################################################

'''

'''
def anime():
    anime = pd.read_csv(raw_data + "/" + "anime.csv")
    return anime


'''

'''
def rating():
    rating = pd.read_csv(raw_data + "/" + "rating.csv.zip")
    return rating


'''
Function to return the anime name that mtches de index number
'''
def from_index_to_title(index,df):
    anime = df
    return anime[anime.index == index]['name'].values[0]


'''
Function to return the matched index number of the anime name
'''
def from_title_to_index(title,df):
    anime = df
    return anime[anime["name"]==title].index.values[0]


'''
Function to find the closest title, It uses Levenshtein Distance to calculate the differences between sequences
'''
def match_the_score(a,b):
   return fuzz.ratio(a,b)


'''
Function to return the most similar title to the name a user typed
'''
def finding_the_closest_title(title,df):
    anime = df
    levenshtein_scores = list(enumerate(anime['name'].apply(match_the_score, b=title))) # Create a list wuth the matchin fuzz.ratio puntuation
    sorted_levenshtein_scores = sorted(levenshtein_scores, key=lambda x: x[1], reverse=True) # Sort from higher to lower the scores
    closest_title = from_index_to_title(sorted_levenshtein_scores[0][0],anime) # Getting the closest anime name/title
    distance_score = sorted_levenshtein_scores[0][1] # Getting the score
    return closest_title, distance_score

'''
The code defines a function "filtering_or" that filters a pandas dataframe based on user-defined 
genres and types using an "OR" method. The function allows the user to select one or all possible 
genres and types and returns a filtered dataframe with the selected genres and types. 
The function also splits the genre and type columns and explodes them to account for multiple entries.
'''
def filtering_or(df, genres, types):
    
    # Make a copy of the input DataFrame
    filtered_df = df.copy()
    
    # Split the genre column into a list of genres
    filtered_df['genre'] = filtered_df['genre'].str.split(', ')
    
    # Explode the genre column to create a new row for each genre in the list
    filtered_df = filtered_df.explode('genre')
    
    # If genres are specified and 'ALL' is not one of them, filter the DataFrame to keep only rows where the genre is in the specified list
    if genres and 'ALL' not in genres:
        filtered_df = filtered_df[filtered_df['genre'].isin(genres)]
        
    # If types are specified and 'ALL' is not one of them, filter the DataFrame to keep only rows where the type is in the specified list
    if types and 'ALL' not in types:
        filtered_df = filtered_df[filtered_df['type'].apply(lambda type: type in types) if isinstance(filtered_df['type'].iloc[0], str) else False]
    
    # If both genres and types are specified
    if genres and types:
        # If 'ALL' is in the genres list, set genres to be all the unique genres in the filtered DataFrame
        if 'ALL' in genres:
            genres = filtered_df['genre'].unique()
        # If 'ALL' is in the types list, set types to be all the unique types in the filtered DataFrame
        if 'ALL' in types:
            types = filtered_df['type'].unique()

        # Filter the DataFrame to keep only rows where the genre is in the genres list AND the type is in the types list
        filtered_df = filtered_df[(filtered_df['genre'].isin(genres)) & (filtered_df['type'].isin(types))]
    
    # Return the filtered DataFrame
    return filtered_df




'''
The function filtering_and takes a DataFrame and two lists of genres and types as input. 
It then filters the DataFrame to include only rows that match all specified genres and types. 
If a list of genres or types is not specified or contains the keyword 'ALL', 
all possible values are used for filtering.
'''
def filtering_and(df, genres, types):
    
    # create a copy of the original dataframe
    filtered_df = df.copy()
    
    # split the genre column values by ', ' and create a new row for each genre
    filtered_df['genre'] = filtered_df['genre'].str.split(', ')
    filtered_df = filtered_df.explode('genre')
    
    # filter rows by genre if any genres are passed and not 'ALL'
    if genres and 'ALL' not in genres:
        filtered_df = filtered_df[filtered_df['genre'].isin(genres)]

    # filter rows by types if any types are passed
    if types:
        
        # create a new column to count the number of type matches
        filtered_df['num_matches'] = filtered_df['type'].apply(lambda x: sum(t in types for t in x.split(', ')) if isinstance(x, str) else 0)
        
        # filter rows where the number of type matches equals the number of types passed
        filtered_df = filtered_df[filtered_df['num_matches'] == len(types)]
        
        # drop the 'num_matches' column
        filtered_df = filtered_df.drop('num_matches', axis=1)
    
    # filter rows by both genre and types if both are passed
    if genres and types:
        
        # if 'ALL' is in the list of genres, select all unique genres in the filtered dataframe
        if 'ALL' in genres:
            genres = filtered_df['genre'].unique()
        
        # filter rows by genre and types using boolean indexing
        filtered_df = filtered_df[(filtered_df['genre'].isin(genres)) & (filtered_df['type'].apply(lambda x: all(t in x.split(', ') for t in types)))]
    
    return filtered_df


'''
Create dict of records with the filters selected - each row becomes a dictionary where key is column name and value is the data in the cell.
'''
def create_dict(names,gen,typ,method,n=200):
    #anime = joblib.load(processed_data  + "/" +  "_anime_to_compare_with_name.pkl")
    anime = pd.read_csv(processed_data + "/" + "_anime_to_compare_with_name.csv")# load anime df
    final_df = anime[anime['name'].isin(names)]
    final_df = final_df.drop(columns=["anime_id", "members"])
    blankIndex=[''] * len(final_df)
    final_df.index=blankIndex
    if method == 'or':
        print("or")
        final_df = filtering_or(final_df, gen, typ)
    elif method == 'and':
        print("and")
        final_df = filtering_and(final_df, gen, typ)
    else:
        raise ValueError("Invalid filter type. Expected 'or' or 'and'.")
    final_df = final_df.drop_duplicates(subset=["name"])
    final_df = final_df.head(n)
    if final_df.empty:
        sentence = print('WOW!!!! Sorry, there is no matches for the anime and options selected! \n Try again, you might have mroe luck')
        return sentence
    else:
        final_dict = final_df.to_dict('records')

        return final_dict

############################################################
############################################################
#                                                          #
#----- Unsupervised User content based recommendation -----#
#                                                          #
############################################################
############################################################

'''
A function that returns the names of the similar animes
for Unsupervised User content based recommendation system
'''
def print_similar_animes(query):
    ind = joblib.load(saved_models_folder + "/" + "model_based_content.pkl") # Load the trained model
    #anime = joblib.load(processed_data + "/" + "_anime_to_compare_with_name.pkl")
    anime = pd.read_csv(processed_data + "/" + "_anime_to_compare_with_name.csv")# load anime df
    closest_title, distance_score = finding_the_closest_title(query,anime) # find the closest title
       
    if distance_score == 100: # When a user does not make misspellings
        names = []
        errors = []
        print('These are the recommendations for similar animes to '+'\033[1m'+str(query)+'\033[0m'+'','\n')
        found_id = from_title_to_index(query,anime) # return the matched index number of the anime name
        array = ind[found_id][1:] # return the matched index number of the anime name that user did input
        indi = np.where(array==found_id) # return the position of the anime index that user did input (if it is in the list)
        array = np.delete(array, indi) # erase the anime index that matches the anime name that used did input
        #array = array[0:n] # print the number of anime recommendations that userd chosed
        for id in array:
            try :
                names.append(anime[anime.index == id]['name'].values[0])
            except IndexError :
                errors.append(id)
        return names

   # When a user makes misspellings    
    else:
        names = []
        errors = []
        print('I guess you misspelled the name\n Are you looking similitudes for the anime named '+'\033[1m'+str(closest_title)+'\033[0m'+'?','\n' + 'Here are the recommendations:')
        found_id = from_title_to_index(closest_title,anime) # return the matched index number of the anime name that user did input
        array = ind[found_id][1:] # create and array with anime indexes to recoomend according to the anime 
        indi = np.where(array==found_id) # return the position of the anime index that user did input (if it is in the list)
        array = np.delete(array, indi) # erase the anime index that matches the anime name that user did input
        #array = array[0:n] # print the number of anime recommendations that userd chosed
        for id in array:
            try :
                names.append(anime[anime.index == id]['name'].values[0])
            except IndexError :
                errors.append(id)
        return names


#############################################################
#############################################################
#                                                           #
#--------- Unsupervised User  based recommendation ---------#
#                                                           #
#############################################################
#############################################################

'''
Return a list with recommendations for the anime 
'''
def reco(name,n,df):
    model_knn = joblib.load(saved_models_folder + "/" +"model_matrix_user_based_unsupervised.pkl")
    #shutil.unpack_archive(processed_data + "/" + "pivot_user_based_unsupervised.zip",processed_data)
    #pivot_df = pd.read_csv(processed_data + "/" + "pivot_user_based_unsupervised.zip")# load anime df
    pivot_df = joblib.load(processed_data + "/" +"pivot_user_based_unsupervised.pkl")
    indl = from_title_to_index(name,df)   
    distances, indices = model_knn.kneighbors(pivot_df.iloc[indl,:].values.reshape(1, -1), n_neighbors = n+1)
    names_list = []
    for i in range(1, n+1):
        if i == 0:
            print('WOW!!!! Sorry, there is no matches for the anime and options selected!\nTry again, you might have more luck')
        else:
            names_list.append(pivot_df.index[indices.flatten()[i]])
            #print('{0}: {1}'.format(i, pivot_df.index[indices.flatten()[i]]))
    
    return names_list

        

'''
A function that returns the names of the similar animes
for Unsupervised User content based recommendation system
'''
def unsupervised_user_based_recommender(movie_user_likes,n=200):
    #df = joblib.load(processed_data + "/" + "_anime_to_compare_with_name.pkl")
    df = pd.read_csv(processed_data + "/" + "_anime_to_compare_with_name.csv")# load anime df
    lowertittle = movie_user_likes.lower() # Pasamos el titulo a minúsculas
    #pivot_df_try = joblib.load(processed_data + "/" + "_to_find_index_user_based_unsupervised.pkl")
    shutil.unpack_archive(processed_data + "/" + "pivot_user_based_unsupervised.zip",processed_data)
    pivot_df_try = pd.read_csv(processed_data + "/" + "_to_find_index_user_based_unsupervised.csv")# load anime df
    closest_title, distance_score = finding_the_closest_title(lowertittle,df)
    # When a user does not make misspellings
    if distance_score == 100:
        print('These are the recommendations for similar animes to '+'\033[1m'+str(closest_title)+'\033[0m'+'','\n')
        return reco(lowertittle,n,pivot_df_try)
    # When a user makes misspellings    
    else:
        print('I guess you misspelled the name\n\nAre you looking similitudes for the anime named '+'\033[1m'+str(closest_title)+'\033[0m'+'?','\n' + '\nHere are the recommendations:\n')
        return reco(closest_title,n,pivot_df_try)


##############################################################
##############################################################
#                                                            #
#----------- Supervised User based recommendation -----------#
#                                                            #
##############################################################
##############################################################

'''
Create dict of records with the filters selected - each row becomes a dictionary where key is column name and value is the data in the cell.
'''
def create_dict_su(final_df,gen,typ,method,n=100):
    df = final_df
    if method == 'or':
        final_df = filtering_or(df, gen, typ)
    elif method == 'and':
        final_df = filtering_and(df, gen, typ)
    else:
        raise ValueError("Invalid filter type. Expected 'or' or 'and'.")
    final_df = final_df.head(n)
    if final_df.empty:
        sentence = print('WOW!!!! Sorry, there is no matches for the anime and options selected! \n Try again, you might have mroe luck')
        return sentence
    else:
        final_dict = final_df.to_dict('records')

        return final_dict


def sort_it(id):
    algo = joblib.load(saved_models_folder + "/" + "SVD_samople_fit.pkl")
    df = pd.read_csv(processed_data + "/" + "anime_final.csv")# load anime df
    df['Estimate_Score'] = df['anime_id'].apply(lambda x: algo.predict(id, x).est)
    df = df.sort_values('Estimate_Score', ascending=False).drop(['anime_id'], axis = 1)
    blankIndex=[''] * len(df)
    df.index=blankIndex 
    return df

