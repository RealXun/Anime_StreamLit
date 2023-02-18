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
Function to apply the filters fo the df recommended with animes
'''
#def filtering(df,gen,typ):
#    
#    if (gen != "All") and (typ != "All"):
#        filtered = df[df['genre'].str.contains(gen, regex=False, case=False, na=False)]
#        filtered = filtered[filtered['type'].str.contains(typ, regex=False, case=False, na=False)]
#        return filtered
#
#    elif  (gen == "All") and (typ != "All"):
#        filtered = df[df['type'].str.contains(typ, regex=False, case=False, na=False)]
#        return filtered
#
#    elif  (typ == "All") and (gen != "All"):
#        filtered = df[df['genre'].str.contains(gen, regex=False, case=False, na=False)]
#        return filtered
#
#    elif  (typ == "All") and (gen == "All"):
#        return df


'''
Filtering function that takes a pandas DataFrame df, 
a list of genres genres, and a list of types types as input arguments.

The function first makes a copy of the input DataFrame and splits the 
genre column on commas, creating multiple rows for each anime that has multiple genres.

The function then checks if both the genres and types lists are non-empty. 
If both lists are non-empty and contain "ALL" strings, the function simply 
returns the original input DataFrame. If only the genres list contains "ALL", 
the function filters the DataFrame based on the type column, and similarly, 
if only the types list contains "ALL", the function filters the DataFrame 
based on the genre column. If neither list contains "ALL", the function 
filters the DataFrame to only include rows where the anime has a genre in 
the genres list and a type in the types list.

If either the genres or types list is empty, the function checks which list 
is empty and filters the DataFrame accordingly based on the non-empty list. 
If both lists are empty, the function simply returns the input DataFrame.

Finally, the function returns the filtered DataFrame.
'''


def filtering(df, genres, types):
    
    # Making a copy of the input DataFrame and assigning it to filtered_df.
    filtered_df = df.copy()
    
    # It splits the values in the 'genre' column of filtered_df by the separator ", " 
    # using the str.split() method of Pandas. This creates a list of genres for each row in the column.
    filtered_df['genre'] = filtered_df['genre'].str.split(', ')
    
    # Then "explodes" the DataFrame by the 'genre' column using the explode() method of Pandas. 
    # This creates a new row for each genre in each row of the original DataFrame.
    filtered_df = filtered_df.explode('genre')
    
    # If the genres argument is provided and 'ALL' is not in genres, 
    # the function filters the DataFrame by keeping only the rows where 
    # the 'genre' column matches one of the genres in the genres list
    # using the isin() method of Pandas.
    if genres and 'ALL' not in genres:
        filtered_df = filtered_df[filtered_df['genre'].isin(genres)]
        
    # If the types argument is provided, the function filters the DataFrame by keeping only the rows 
    # where at least one anime type in the 'type' column matches one of the types in the types list 
    # using the apply() method of Pandas with a lambda function that iterates over each row in the 'type' 
    # column and checks if any type matches one of the types in the types list. The any() function is 
    # used to check if at least one type matches.
    if types and 'ALL' not in types:
        filtered_df = filtered_df[filtered_df['type'].apply(lambda x: any(t in x.split(', ') for t in types) if isinstance(x, str) else False)]
    
    # If both genres and types are provided, the function checks if 'ALL' is in genres or types. 
    # If it is, the function sets genres and types to lists of unique genres and types in filtered_df 
    # using the unique() method of Pandas.
    if genres and types:
        if 'ALL' in genres:
            genres = filtered_df['genre'].unique()
        if 'ALL' in types:
            types = filtered_df['type'].str.split(', ').explode().unique()
        # filtered_df by keeping only the rows where at least one anime type in the 'type' column 
        # matches one of the types in the types list and the 'genre' column matches one of the genres 
        # in genres using the apply() method of Pandas with a lambda function that iterates over each 
        # row in the DataFrame and checks if at least one type matches and one genre matches. The any() 
        # function is used to check if at least one type and one genre match.
        filtered_df = filtered_df[filtered_df.apply(lambda x: any(t in x['type'].split(', ') for t in types) and x['genre'] in genres, axis=1)]
    
    # The function returns filtered_df.
    return filtered_df





'''
The function filters the DataFrame based on the specified genres in the same way as before. 
Then, it checks if types is non-empty and filters the DataFrame based on whether the number 
of matches between the input type list and the types in each row is equal to the length of 
the input type list. It does this using a lambda function that counts the number of types 
in each row that match the input type list, and then filters on this count. Finally, 
it removes the 'num_matches' column that was added.

To filter based on the AND operator between genres and types, the code now checks if genres 
and types are both non-empty and filters the DataFrame based on whether each row's genre 
is in the input genre list and whether all the types in the input type list are present 
in each row. It does this using a lambda function that checks if all the types in the 
input type list are present in each row.
'''

#The function takes three arguments: a Pandas DataFrame df, a list of genres genres, and a list of anime types types.
def filtering_and(df, genres, types):
    
    # Making a copy of the input DataFrame and assigning it to filtered_df.
    filtered_df = df.copy()
    
    # It splits the values in the 'genre' column of filtered_df by the separator ", " 
    # using the str.split() method of Pandas. This creates a list of genres for each row in the column.
    filtered_df['genre'] = filtered_df['genre'].str.split(', ')
    
    # Then "explodes" the DataFrame by the 'genre' column using the explode() method of Pandas. 
    # This creates a new row for each genre in each row of the original DataFrame.
    filtered_df = filtered_df.explode('genre')
    
    # If the genres argument is provided and 'ALL' is not in genres, 
    # the function filters the DataFrame by keeping only the rows where 
    # the 'genre' column matches one of the genres in the genres list
    # using the isin() method of Pandas.
    if genres and 'ALL' not in genres:
        filtered_df = filtered_df[filtered_df['genre'].isin(genres)]

    if types:
        # If the types argument is provided, the function creates a new column in filtered_df 
        # called 'num_matches' that counts the number of anime types in each row that match 
        # the input types list. The function uses a lambda function with the apply() method 
        # of Pandas to iterate over each row of the 'type' column and count the number of matches. 
        # The sum() function is used to count the number of matches, and the split() method is 
        # used to split the types string into a list. If the 'type' column is not a string, 
        # the function sets the count to 0.
        filtered_df['num_matches'] = filtered_df['type'].apply(lambda x: sum(t in types for t in x.split(', ')) if isinstance(x, str) else 0)
        # Keep only the rows where the count of matches equals the length of the input type list
        filtered_df = filtered_df[filtered_df['num_matches'] == len(types)]
        # Remove the 'num_matches' column
        filtered_df = filtered_df.drop('num_matches', axis=1)
    
    # If both genres and types are provided, the function checks if 'ALL' is in genres. 
    # If it is, the function sets genres to a list of unique genres in filtered_df 
    # using the unique() method of Pandas.
    if genres and types:
        # The 'all' is used to check if all anime types in the 'type' column match the input types list
        if 'ALL' in genres:
            genres = filtered_df['genre'].unique()
        # filtered_df by keeping only the rows where the 'genre' column matches one of the genres in genres 
        # and all anime types in the 'type' column match the input types list using a lambda function with 
        # the apply() method of Pandas. The all() function is used to check if all anime types in the 'type' 
        # column match the input types list. The split() method is used to split the types string into a list.
        filtered_df = filtered_df[(filtered_df['genre'].isin(genres)) & (filtered_df['type'].apply(lambda x: all(t in x.split(', ') for t in types)))]
    
    # The function returns filtered_df.
    return filtered_df


'''
Create a df of the anime matches with the filters selected
'''
def create_df(names,gen,typ,n=100):
    #anime = joblib.load(processed_data + "/" + "_anime_to_compare_with_name.pkl")
    anime = pd.read_csv(processed_data + "/" + "_anime_to_compare_with_name.csv")# load anime df
    final_df = anime[anime['name'].isin(names)]
    final_df = final_df.drop(columns=["anime_id", "members"])
    blankIndex=[''] * len(final_df)
    final_df.index=blankIndex
    final_df = filtering(final_df,gen,typ)
    to_return = final_df.head(n)
    if final_df.empty:
        sentence = print('WOW!!!! Sorry, there is no matches for the anime and options selected! \n Try again, you might have mroe luck')
        return sentence
    else:
        return to_return


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
        final_df = filtering(final_df, gen, typ)
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


#def dict_recommendation(id,n,gen,typ):
#    final_df = reco_by_user(id,n,gen,typ)
#    to_return = final_df
#    blankIndex=[''] * len(final_df)
#    final_df.index=blankIndex
#    final_df = final_df.head(n)
#    if final_df.empty:
#        sentence = print('WOW!!!! Sorry, there is no matches for the anime and options selected! \n Try again, you might have mroe luck')
#        return sentence
#    else:
#        final_dict = final_df.to_dict('records')
#        return final_dict

#def reco_by_user(id,n,gen,typ):
#    chosen_user = pd.read_csv(processed_data + "/" + "anime_final.csv")# load anime df
#    df = pd.read_csv(processed_data + "/" + "anime_final.csv")# load anime df
#    df['genre'] = df['genre'].str.split(', ')
#    df = df.explode('genre')   
#
#    if gen and typ:
#
#        # If both lists are empty, the original DataFrame is returned without any filtering.
#        filtered = df[df['genre'].isin(gen)]
#        filtered = filtered[filtered['type'].isin([t for t in typ])]
#        return sort_it(id,filtered,n)
#
#        # If only the genres list has values, the function filters the DataFrame 
#        # to include only rows where the genre column matches one of the genres in the list.
#    elif gen:
#        filtered = df[df['genre'].isin(gen)]
#        return sort_it(id,filtered,n)
#        # If only the types list has values, the function filters the DataFrame 
#        # to include only rows where the type column matches one of the types in the list.
#    elif gen:
#        filtered = df[df['type'].isin([t for t in typ])]
#        return sort_it(id,filtered,n)
#    else:
#        return chosen_user

#def sort_it(id):
#    algo = joblib.load(saved_models_folder + "/" + "SVD_samople_fit.pkl")
#    df = pd.read_csv(processed_data + "/" + "anime_final.csv")# load anime df
#    df['Estimate_Score'] = df['anime_id'].apply(lambda x: algo.predict(id, x).est)
#    df = df.sort_values('Estimate_Score', ascending=False).drop(['anime_id'], axis = 1)
#    blankIndex=[''] * len(df)
#    df.index=blankIndex 
#    return df

'''
Create dict of records with the filters selected - each row becomes a dictionary where key is column name and value is the data in the cell.
'''
def create_dict_su(final_df,gen,typ,method,n=100):
    df = final_df
    if method == 'or':
        final_df = filtering(df, gen, typ)
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

