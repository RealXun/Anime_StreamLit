---
jupyter:
  kernelspec:
    display_name: stlit
    language: python
    name: python3
  language_info:
    codemirror_mode:
      name: ipython
      version: 3
    file_extension: .py
    mimetype: text/x-python
    name: python
    nbconvert_exporter: python
    pygments_lexer: ipython3
    version: 3.10.6
  nbformat: 4
  nbformat_minor: 2
  orig_nbformat: 4
  vscode:
    interpreter:
      hash: cecd28889de614796b096279bba34faf450ea72cc4d265581beb94f7bfeace2c
---

::: {.cell .markdown}
# Unsupervised content based recommendation system
:::

::: {.cell .markdown}
## Import Libraries
:::

::: {.cell .code execution_count="1"}
``` python
# Standard library imports
import os # allows access to OS-dependent functionalities
import re #  regular expression matching operations similar to those found in Perl
import sys # to manipulate different parts of the Python runtime environment
import warnings # is used to display the message Warning
import pickle # serializing and deserializing a Python object structure.

# Third party libraries
from fastparquet import write # parquet format, aiming integrate into python-based big data work-flows
from fuzzywuzzy import fuzz # used for string matching

import numpy as np # functions for working in domain of linear algebra, fourier transform, matrices and arrays
import pandas as pd # data analysis and manipulation tool
import joblib # set of tools to provide lightweight pipelining in Python

# deal with sparse data libraries
from scipy.sparse import csr_matrix # Returns a copy of column i of the matrix, as a (m x 1) CSR matrix (column vector).

# visualization
#import seaborn as sns # data visualization library based on matplotlib.
import matplotlib.pyplot as plt # collection of functions that make matplotlib work like MATLAB.

## scikit Preprocessing data libraries
from sklearn.preprocessing import MinMaxScaler # Transform features by scaling each feature to a given range.

## scikit Feature Extraction libraries
from sklearn.feature_extraction.text import TfidfVectorizer # Convert a collection of raw documents to a matrix of TF-IDF features
from sklearn.feature_extraction.text import CountVectorizer # Convert a collection of text documents to a matrix of token counts.

## scikit Pairwise metrics libraries
#implements utilities to evaluate pairwise distances or affinity of sets of samples.
from sklearn.metrics.pairwise import sigmoid_kernel
from sklearn.metrics.pairwise import cosine_similarity 
from sklearn.metrics.pairwise import linear_kernel 

## scikit Cross validation iterators libraries
from sklearn.model_selection import GridSearchCV

# Unsupervised learner for implementing neighbor searches.
from sklearn.neighbors import NearestNeighbors

# setting display options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)


# Get the current working directory
cwd = os.getcwd()

# Add the path of the utils directory to sys.path
utils_path = os.path.abspath(os.path.join(cwd, '..', 'utils'))
sys.path.append(utils_path)

# Utils libraries
from cleaning import *
from recommend import *
from testing import *
from training import *

#Preparing folder variables

main_folder = os.path.abspath(os.path.join(os.pardir))
data_folder = (main_folder + "/" +"data")
saved_models_folder = (data_folder + "/" + "saved_models")
raw_data = (data_folder + "/" + "_raw")
processed_data = (data_folder + "/" + "processed")
content_based_supervised_data = (main_folder + "/" + "processed" + "/" + "content_based_supervised")
```

::: {.output .stream .stderr}
    c:\Users\Chrisitan\miniconda3\envs\stlit\lib\site-packages\fuzzywuzzy\fuzz.py:11: UserWarning: Using slow pure-python SequenceMatcher. Install python-Levenshtein to remove this warning
      warnings.warn('Using slow pure-python SequenceMatcher. Install python-Levenshtein to remove this warning')
:::
:::

::: {.cell .markdown}
## Cleaning and preparing the data
:::

::: {.cell .code execution_count="2"}
``` python
anime = pd.read_csv(raw_data + "/" + "anime.csv")
rating = pd.read_csv(raw_data + "/" + "rating.csv.zip")
```
:::

::: {.cell .code execution_count="3"}
``` python
print(clean_anime_df.__doc__)
```

::: {.output .stream .stdout}
    The function clean_anime_df() takes an anime dataframe as input and performs several 
        cleaning and preprocessing steps, such as removing special characters from anime names, 
        converting all names to lowercase, filling missing values for "episodes" and "score" 
        columns with their median, dropping rows with null values for "genre" or "type" columns, 
        and saving the cleaned dataframe to a CSV file. The cleaned dataframe is also returned as output.
:::
:::

::: {.cell .markdown}
# Cleand data
:::

::: {.cell .markdown}
Steps:

-   Cambiamos a min??sculas todos los nombre de animes
:::

::: {.cell .code execution_count="4"}
``` python
anime_cleaned = clean_anime_df(anime)
anime_cleaned.head(1)
```

::: {.output .execute_result execution_count="4"}
```{=html}
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>anime_id</th>
      <th>name</th>
      <th>english_title</th>
      <th>japanses_title</th>
      <th>genre</th>
      <th>type</th>
      <th>source</th>
      <th>duration</th>
      <th>episodes</th>
      <th>rating</th>
      <th>score</th>
      <th>rank</th>
      <th>members</th>
      <th>synopsis</th>
      <th>cover</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>cowboy bebop</td>
      <td>Cowboy Bebop</td>
      <td>???????????????????????????</td>
      <td>Action, Adventure, Comedy, Drama, Sci-Fi, Space</td>
      <td>TV</td>
      <td>Original</td>
      <td>24 min per ep</td>
      <td>26</td>
      <td>R - 17+ (violence &amp; profanity)</td>
      <td>8.75</td>
      <td>40.0</td>
      <td>486824.0</td>
      <td>Crime is timeless. By the year 2071, humanity has expanded across the galaxy, filling the surface of other planets with settlements like those on Earth. These new societies are plagued by murder, drug use, and theft, and intergalactic outlaws are hunted by a growing number of tough bounty hunters.\r\n\r\nSpike Spiegel and Jet Black pursue criminals throughout space to make a humble living. Beneath his goofy and aloof demeanor, Spike is haunted by the weight of his violent past. Meanwhile, Jet manages his own troubled memories while taking care of Spike and the Bebop, their ship. The duo is joined by the beautiful con artist Faye Valentine, odd child Edward Wong Hau Pepelu Tivrusky IV, and Ein, a bioengineered Welsh Corgi.\r\n\r\nWhile developing bonds and working to catch a colorful cast of criminals, the Bebop crew's lives are disrupted by a menace from Spike's past. As a rival's maniacal plot continues to unravel, Spike must choose between life with his newfound family or revenge for his old wounds.\r\n\r\n[Written by MAL Rewrite]</td>
      <td>https://cdn.myanimelist.net/images/anime/4/19644l.jpg</td>
    </tr>
  </tbody>
</table>
</div>
```
:::
:::

::: {.cell .code execution_count="5"}
``` python
anime_cleaned.shape
```

::: {.output .execute_result execution_count="5"}
    (12121, 15)
:::
:::

::: {.cell .code execution_count="6"}
``` python
anime_cleaned.head(1)
```

::: {.output .execute_result execution_count="6"}
```{=html}
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>anime_id</th>
      <th>name</th>
      <th>english_title</th>
      <th>japanses_title</th>
      <th>genre</th>
      <th>type</th>
      <th>source</th>
      <th>duration</th>
      <th>episodes</th>
      <th>rating</th>
      <th>score</th>
      <th>rank</th>
      <th>members</th>
      <th>synopsis</th>
      <th>cover</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>cowboy bebop</td>
      <td>Cowboy Bebop</td>
      <td>???????????????????????????</td>
      <td>Action, Adventure, Comedy, Drama, Sci-Fi, Space</td>
      <td>TV</td>
      <td>Original</td>
      <td>24 min per ep</td>
      <td>26</td>
      <td>R - 17+ (violence &amp; profanity)</td>
      <td>8.75</td>
      <td>40.0</td>
      <td>486824.0</td>
      <td>Crime is timeless. By the year 2071, humanity has expanded across the galaxy, filling the surface of other planets with settlements like those on Earth. These new societies are plagued by murder, drug use, and theft, and intergalactic outlaws are hunted by a growing number of tough bounty hunters.\r\n\r\nSpike Spiegel and Jet Black pursue criminals throughout space to make a humble living. Beneath his goofy and aloof demeanor, Spike is haunted by the weight of his violent past. Meanwhile, Jet manages his own troubled memories while taking care of Spike and the Bebop, their ship. The duo is joined by the beautiful con artist Faye Valentine, odd child Edward Wong Hau Pepelu Tivrusky IV, and Ein, a bioengineered Welsh Corgi.\r\n\r\nWhile developing bonds and working to catch a colorful cast of criminals, the Bebop crew's lives are disrupted by a menace from Spike's past. As a rival's maniacal plot continues to unravel, Spike must choose between life with his newfound family or revenge for his old wounds.\r\n\r\n[Written by MAL Rewrite]</td>
      <td>https://cdn.myanimelist.net/images/anime/4/19644l.jpg</td>
    </tr>
  </tbody>
</table>
</div>
```
:::
:::

::: {.cell .code execution_count="7"}
``` python
anime_features = prepare_supervised_content_based(anime_cleaned)
```
:::

::: {.cell .code execution_count="8"}
``` python
anime_features.head(1)
```

::: {.output .execute_result execution_count="8"}
```{=html}
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Action</th>
      <th>Adventure</th>
      <th>Comedy</th>
      <th>Drama</th>
      <th>Dementia</th>
      <th>Mecha</th>
      <th>Historical</th>
      <th>School</th>
      <th>Hentai</th>
      <th>Horror</th>
      <th>Demons</th>
      <th>Ecchi</th>
      <th>Fantasy</th>
      <th>Shounen</th>
      <th>Game</th>
      <th>Mystery</th>
      <th>Cars</th>
      <th>Magic</th>
      <th>Romance</th>
      <th>Sci-Fi</th>
      <th>Harem</th>
      <th>Kids</th>
      <th>Shoujo</th>
      <th>Military</th>
      <th>Super Power</th>
      <th>Martial Arts</th>
      <th>Music</th>
      <th>Slice of Life</th>
      <th>Sports</th>
      <th>Supernatural</th>
      <th>Parody</th>
      <th>Vampire</th>
      <th>Psychological</th>
      <th>Samurai</th>
      <th>Yaoi</th>
      <th>Seinen</th>
      <th>Josei</th>
      <th>Thriller</th>
      <th>Space</th>
      <th>Shounen Ai</th>
      <th>Police</th>
      <th>Yuri</th>
      <th>Shoujo Ai</th>
      <th>Movie</th>
      <th>Music</th>
      <th>ONA</th>
      <th>OVA</th>
      <th>Special</th>
      <th>TV</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>
```
:::
:::

::: {.cell .code execution_count="9"}
``` python
anime_features.shape
```

::: {.output .execute_result execution_count="9"}
    (12121, 49)
:::
:::

::: {.cell .code execution_count="10"}
``` python
min_max = MinMaxScaler()
min_max_features = min_max.fit_transform(anime_features)
```
:::

::: {.cell .code execution_count="11"}
``` python
min_max_features.shape
```

::: {.output .execute_result execution_count="11"}
    (12121, 49)
:::
:::

::: {.cell .code execution_count="12"}
``` python
np.round(min_max_features,2)
```

::: {.output .execute_result execution_count="12"}
    array([[1., 1., 1., ..., 0., 0., 1.],
           [1., 0., 0., ..., 0., 0., 0.],
           [1., 0., 1., ..., 0., 0., 1.],
           ...,
           [0., 0., 0., ..., 0., 0., 1.],
           [0., 0., 1., ..., 0., 0., 1.],
           [0., 1., 0., ..., 0., 0., 0.]])
:::
:::

::: {.cell .markdown}
## Finding the best parameters for NearestNeighbors model
:::

::: {.cell .code execution_count="13"}
``` python
param_NearestNeighbors(min_max_features)
```

::: {.output .stream .stderr}
    c:\Users\Chrisitan\miniconda3\envs\stlit\lib\site-packages\sklearn\model_selection\_search.py:952: UserWarning: One or more of the test scores are non-finite: [nan nan nan ... nan nan nan]
      warnings.warn(
:::

::: {.output .execute_result execution_count="13"}
    {'algorithm': 'auto',
     'leaf_size': 30,
     'metric': 'minkowski',
     'n_neighbors': 1,
     'p': 1,
     'radius': 0.0}
:::
:::

::: {.cell .markdown}
## Building model with the best parameters
:::

::: {.cell .code execution_count="14"}
``` python
model_NearestNeighbors(min_max_features)
```

::: {.output .execute_result execution_count="14"}
    array([[    0,  1118,   376, ...,  1029,   955,  1034],
           [    1,  3154,  7607, ...,  3268,  1405,  1381],
           [ 3409, 12113,  3940, ...,  3231,   376,  3353],
           ...,
           [ 7973,  3292,   626, ...,  8364,  8387,  9359],
           [12119,  7536, 11332, ...,  1083,  7440,  2463],
           [ 7527, 12120,  9683, ...,  8052,  7518,  2190]], dtype=int64)
:::
:::

::: {.cell .markdown}
## Get recommendations
:::

::: {.cell .code execution_count="15"}
``` python
# We can get the recommendation as a dictionary
# We selec the name of the anime we want to find similitudes
# Then the genre we want (or write "All")
# Then the type we want (or write "All")
# Then the number of suggestions we have(we might get less if there not so many o none if there is no matches)

create_dict(print_similar_animes("Naruto"),["Shounen"],["TV"],"or",20)
```

::: {.output .stream .stdout}
    I guess you misspelled the name
     Are you looking similitudes for the anime named naruto? 
    Here are the recommendations:
    or
:::

::: {.output .execute_result execution_count="15"}
    [{'name': 'yakitate   japan',
      'english_title': 'Yakitate!! Japan',
      'japanses_title': '????????????!! ????????????',
      'genre': 'Shounen',
      'type': 'TV',
      'source': 'Manga',
      'duration': '24 min per ep',
      'episodes': 69.0,
      'rating': 'PG-13 - Teens 13 or older',
      'score': 7.92,
      'rank': 687.0,
      'synopsis': "While countries such as France, England, and Germany all have their own internationally celebrated bread, Japan simply does not have one that can match in reputation.\r\n\r\nThus after discovering the wonders of breadmaking at a young age, Kazuma Azuma embarks on a quest to create Japan's own unique national bread. And being blessed with unusually warm hands that allow dough to ferment faster, Azuma is able to bring his baking innovations to another level.\r\n\r\nAs he begins working at the prestigious Japanese bakery chain, Pantasia, Azuma encounters other talented bakers and experiences firsthand the competitive world of baking. Along with his newfound friends and rivals, Azuma strives to create new and unparalleled bread that will start a baking revolution. \r\n\r\n[Written by MAL Rewrite]",
      'cover': 'https://cdn.myanimelist.net/images/anime/3/76432l.jpg'},
     {'name': 'chuuka ichiban ',
      'english_title': 'Chuuka Ichiban!',
      'japanses_title': '????????????',
      'genre': 'Shounen',
      'type': 'TV',
      'source': 'Manga',
      'duration': '23 min per ep',
      'episodes': 52.0,
      'rating': 'PG-13 - Teens 13 or older',
      'score': 7.59,
      'rank': 1413.0,
      'synopsis': 'The story takes place in 19th century China during the Qing Dynasty, where the Emperor was weakened and the country was close to chaos. It is also during a fictitious era called "The Era of the Cooking Wars". It was an era in which top chefs with different cooking styles tried their best to improve their skills and to become the best chef in China. It is a country where insulting a high-grade chef or fooling around with cooking could land a person in a jail, and impersonating a top-chef is as good as usurpation of authority. Chefs compete with each other in order to gain respect and even power, but also with the risks of losing everything.\r\n\r\nThe country of China has four major regions: Beijing, Szechuan, Shanghai, and Guangdong.\r\n\r\nThe beginning of the story takes place in Szechuan, Mao\'s birthplace.\r\n\r\nAfter the death of Mao\'s mother, Pai, who was called the \'Fairy of Cuisine\', Mao becomes a Super Chef in order to take the title as Master Chef of his mother\'s restaurant. However, before he takes his mother\'s place as Master Chef, he continues to travel China in order to learn more of the many ways of cooking, in the hopes of becoming a legendary chef, just like his mother. During his journey, he meets great friends and fierce rivals who wish to challenge him in the field of cooking.\r\n\r\n(Source: Wikipedia)',
      'cover': 'https://cdn.myanimelist.net/images/anime/6/75283l.jpg'},
     {'name': 'hunter x hunter',
      'english_title': 'Hunter x Hunter',
      'japanses_title': 'HUNTER??HUNTER????????????????????????????????',
      'genre': 'Shounen',
      'type': 'TV',
      'source': 'Manga',
      'duration': '23 min per ep',
      'episodes': 62.0,
      'rating': 'PG-13 - Teens 13 or older',
      'score': 8.41,
      'rank': 166.0,
      'synopsis': 'Hunters are specialized in a wide variety of fields, ranging from treasure hunting to cooking. They have access to otherwise unavailable funds and information that allow them to pursue their dreams and interests. However, being a hunter is a special privilege, only attained by taking a deadly exam with an extremely low success rate.\r\n\r\nGon Freecss, a 12-year-old boy with the hope of finding his missing father, sets out on a quest to take the Hunter Exam. Along the way, he picks up three companions who also aim to take the dangerous test: the revenge-seeking Kurapika, aspiring doctor Leorio Paladiknight, and a mischievous child the same age as Gon, Killua Zoldyck.\r\n\r\nAs the four aspiring hunters embark on a perilous adventure, they fight for their dreams while defying the odds.\r\n\r\n[Written by MAL Rewrite]',
      'cover': 'https://cdn.myanimelist.net/images/anime/1305/132237l.jpg'},
     {'name': 'tenjou tenge',
      'english_title': 'Tenjou Tenge',
      'japanses_title': '????????????',
      'genre': 'Shounen',
      'type': 'TV',
      'source': 'Manga',
      'duration': '23 min per ep',
      'episodes': 24.0,
      'rating': 'R - 17+ (violence & profanity)',
      'score': 6.88,
      'rank': 4620.0,
      'synopsis': "For some people, high school represents the opportunity for a fresh start. You can take new classes and make new friends. For Souichiro Nagi and Bob Makihara, though, high school means something different: the chance to become the top fighters in the entire student body! Too bad Toudou Academy is the hardest possible place to realize their dreams. Their new high school is no ordinary academic institution. Rather than concentrating on classic subjects like math and science, Toudou Academy was created for the sole purpose of reviving the martial arts in Japan!\r\n\r\nAs a result, Souichiro's aspirations to become top dog are cut short when he runs afoul of Masataka Takayanagi and Maya Natsume. The two upperclassmen easily stop the freshmen duo's rampage across school, but rather than serving as a deterrent, it only stokes their competitive fire. What kind of monstrous fighters attend Toudou Academy? Are there any stronger than Masataka and Maya? And why in the world is Maya's younger sister stalking Souichiro? Learn the answers to these questions and more in Tenjou Tenge!",
      'cover': 'https://cdn.myanimelist.net/images/anime/10/8380l.jpg'},
     {'name': 'dragon ball',
      'english_title': 'Dragon Ball',
      'japanses_title': '?????????????????????',
      'genre': 'Shounen',
      'type': 'TV',
      'source': 'Manga',
      'duration': '24 min per ep',
      'episodes': 153.0,
      'rating': 'PG-13 - Teens 13 or older',
      'score': 7.96,
      'rank': 630.0,
      'synopsis': 'Gokuu Son is a young boy who lives in the woods all alone???that is, until a girl named Bulma runs into him in her search for a set of magical objects called the "Dragon Balls." Since the artifacts are said to grant one wish to whoever collects all seven, Bulma hopes to gather them and wish for a perfect boyfriend. Gokuu happens to be in possession of a dragon ball, but unfortunately for Bulma, he refuses to part ways with it, so she makes him a deal: he can tag along on her journey if he lets her borrow the dragon ball\'s power. With that, the two set off on the journey of a lifetime.\r\n\r\nThey don\'t go on the journey alone. On the way, they meet the old Muten-Roshi and wannabe disciple Kuririn, with whom Gokuu trains to become a stronger martial artist for the upcoming World Martial Arts Tournament. However, it\'s not all fun and games; the ability to make any wish come true is a powerful one, and there are others who would do much worse than just wishing for a boyfriend. To stop those who would try to abuse the legendary power, they train to become stronger fighters, using their newfound strength to help the people around them along the way.\r\n\r\n[Written by MAL Rewrite]',
      'cover': 'https://cdn.myanimelist.net/images/anime/1887/92364l.jpg'},
     {'name': 'rekka no honoo',
      'english_title': 'Rekka no Honoo',
      'japanses_title': '????????????',
      'genre': 'Shounen',
      'type': 'TV',
      'source': 'Manga',
      'duration': '23 min per ep',
      'episodes': 42.0,
      'rating': 'PG-13 - Teens 13 or older',
      'score': 7.34,
      'rank': 2349.0,
      'synopsis': 'Most people think that ninjas are a thing of the past, but Rekka Hanabishi wishes otherwise. Although he comes from a family that makes fireworks, he likes to think of himself as a self-styled, modern-day ninja. Sounds like fun, right? Maybe not. Rekka ends up in lots of fights because he once made the bold announcement that if someone can defeat him, he will become their servant.\r\n\r\nThen one day, Rekka meets Yanagi Sakoshita, a gentle girl with the ability to heal any wound or injury. Their meeting sets off a chain of events, which culminate into a shocking discovery. Rekka is the last surviving member of a legendary ninja clan that was wiped out centuries ago. Even more astonishing than being an actual ninja, he also wields the power to control fire. What does this mean for Rekka? Who are these strange people after him and Yanagi? Find out in Rekka no Honoo!',
      'cover': 'https://cdn.myanimelist.net/images/anime/1646/113504l.jpg'},
     {'name': 'bleach',
      'english_title': 'Bleach',
      'japanses_title': 'BLEACH - ???????????? -',
      'genre': 'Shounen',
      'type': 'TV',
      'source': 'Manga',
      'duration': '24 min per ep',
      'episodes': 366.0,
      'rating': 'PG-13 - Teens 13 or older',
      'score': 7.9,
      'rank': 722.0,
      'synopsis': "Ichigo Kurosaki is an ordinary high schooler???until his family is attacked by a Hollow, a corrupt spirit that seeks to devour human souls. It is then that he meets a Soul Reaper named Rukia Kuchiki, who gets injured while protecting Ichigo's family from the assailant. To save his family, Ichigo accepts Rukia's offer of taking her powers and becomes a Soul Reaper as a result.\r\n\r\nHowever, as Rukia is unable to regain her powers, Ichigo is given the daunting task of hunting down the Hollows that plague their town. However, he is not alone in his fight, as he is later joined by his friends???classmates Orihime Inoue, Yasutora Sado, and Uryuu Ishida???who each have their own unique abilities. As Ichigo and his comrades get used to their new duties and support each other on and off the battlefield, the young Soul Reaper soon learns that the Hollows are not the only real threat to the human world.\r\n\r\n[Written by MAL Rewrite]",
      'cover': 'https://cdn.myanimelist.net/images/anime/3/40451l.jpg'},
     {'name': 'viewtiful joe',
      'english_title': 'Viewtiful Joe',
      'japanses_title': '????????????????????? ?????????',
      'genre': 'Shounen',
      'type': 'TV',
      'source': 'Game',
      'duration': '20 min per ep',
      'episodes': 51.0,
      'rating': 'PG-13 - Teens 13 or older',
      'score': 6.74,
      'rank': 5265.0,
      'synopsis': 'Joe, a red-headed movie buff, and Silvia, his girlfriend, are having a bit of relationship trouble. Silvia feels that Joe is taking her for-granted and wants to do something together for once, so Joe decides to take her to see an old action movie featuring his favorite hero, Captain Blue. What started out as a cute movie date takes a turn for the worst when Silvia is pulled into the movie by the leader of the evil organization, Jado.\r\n\r\nJoe follows her into the mysterious "Movieland," and is granted a powerful device known as a V-Watch by Captain Blue himself. With it, he transforms into the action hero named "Viewtiful Joe" and goes off to rescue his girlfriend before she can be used by Jado to take over the world. It\'s a long road to go from average Joe to full-blown hero, but he\'ll give it his all to save both his girl and the world???and he\'ll do it in the most "view-ti-ful" way possible.',
      'cover': 'https://cdn.myanimelist.net/images/anime/1/278l.jpg'},
     {'name': 'grappler baki  saidai tournament hen',
      'english_title': 'Grappler Baki: Saidai Tournament-hen',
      'japanses_title': '????????????????????????(??????) ???????????????????????????',
      'genre': 'Shounen',
      'type': 'TV',
      'source': 'Manga',
      'duration': '24 min per ep',
      'episodes': 24.0,
      'rating': 'R - 17+ (violence & profanity)',
      'score': 7.49,
      'rank': 1772.0,
      'synopsis': "Mitsunari Tokugawa, the organizer of the historic Tokugawa underground fighting ring, has created a tournament featuring 38 of the world's best fighters, many of whom are grandmasters in their respective form of martial arts. With the exception of weapons, anything goes in Tokugawa's ring so that each fighter is able to showcase their true power and strongest secret moves.\r\n\r\nBaki Hanma earned a place in the tournament due to his status as the reigning champion of Tokugawa's fighting ring. Will he be able to come out on top? \r\n\r\n[Written by MAL Rewrite]",
      'cover': 'https://cdn.myanimelist.net/images/anime/1433/96723l.jpg'},
     {'name': 'sexy commando gaiden  sugoiyo   masaru san',
      'english_title': 'Sexy Commando Gaiden: Sugoi yo!! Masaru-san',
      'japanses_title': '????????????????????????????????? ????????????!! ???????????????',
      'genre': 'Shounen',
      'type': 'TV',
      'source': 'Manga',
      'duration': '8 min per ep',
      'episodes': 48.0,
      'rating': 'R - 17+ (violence & profanity)',
      'score': 7.65,
      'rank': 1273.0,
      'synopsis': 'Okometsubu Fujiyama has recently transferred over to a new school, Wakame High School. His goal is to make 100 friends--until he meets the extremely weird Masaru Hananakajima. Masaru is a martial artist whose specialty is the "Sexy Commando" form of martial art. Masaru forms a club based on this art, including Fujiyama, who he nicknames Fuumin, in the club. The club becomes full of strange, yet wacky people. Aliens, mustaches, and cute fuzzy animals are encountered as the club moves along and gets steadily more popular.\r\n\r\n(Source: ANN)',
      'cover': 'https://cdn.myanimelist.net/images/anime/13/39595l.jpg'},
     {'name': 'dragon ball z',
      'english_title': 'Dragon Ball Z',
      'japanses_title': '?????????????????????Z',
      'genre': 'Shounen',
      'type': 'TV',
      'source': 'Manga',
      'duration': '24 min per ep',
      'episodes': 291.0,
      'rating': 'PG-13 - Teens 13 or older',
      'score': 8.16,
      'rank': 389.0,
      'synopsis': "Five years after winning the World Martial Arts tournament, Gokuu is now living a peaceful life with his wife and son. This changes, however, with the arrival of a mysterious enemy named Raditz who presents himself as Gokuu's long-lost brother. He reveals that Gokuu is a warrior from the once powerful but now virtually extinct Saiyan race, whose homeworld was completely annihilated. When he was sent to Earth as a baby, Gokuu's sole purpose was to conquer and destroy the planet; but after suffering amnesia from a head injury, his violent and savage nature changed, and instead was raised as a kind and well-mannered boy, now fighting to protect others.\r\n\r\nWith his failed attempt at forcibly recruiting Gokuu as an ally, Raditz warns Gokuu's friends of a new threat that's rapidly approaching Earth???one that could plunge Earth into an intergalactic conflict and cause the heavens themselves to shake. A war will be fought over the seven mystical dragon balls, and only the strongest will survive in Dragon Ball Z.\r\n\r\n[Written by MAL Rewrite]",
      'cover': 'https://cdn.myanimelist.net/images/anime/1607/117271l.jpg'},
     {'name': 'virtua fighter',
      'english_title': 'Virtua Fighter',
      'japanses_title': '???????????????????????????',
      'genre': 'Shounen',
      'type': 'TV',
      'source': 'Game',
      'duration': '22 min per ep',
      'episodes': 35.0,
      'rating': 'PG-13 - Teens 13 or older',
      'score': 7.11,
      'rank': 3573.0,
      'synopsis': "Akira Yuki has spent years honing his Bajiquan skills under the guidance of his grandfather. He yearns to see the constellation of the eight stars of heaven, which are only revealed to those with real strength. This burning desire urges him to embark on travels, so as to learn more about how to see the stars.\r\n\r\nMeanwhile, a nefarious robotics scientist, Eva Durix, desires to create the perfect soldier. Eva's group, Judgment 6, tracks down and kidnaps Sarah Bryant, a college student and close acquaintance of Akira who is investigating a mysterious accident concerning her brother. Akira must now fight his way to Sarah to save her from the clutches of Judgement 6, a perilous path sure to be paved with countless challenges.",
      'cover': 'https://cdn.myanimelist.net/images/anime/1234/110241l.jpg'},
     {'name': 'kakutou bijin wulong  rebirth',
      'english_title': 'Kakutou Bijin Wulong: Rebirth',
      'japanses_title': '???????????? ??????[????????????] REBIRTH',
      'genre': 'Shounen',
      'type': 'TV',
      'source': 'Manga',
      'duration': '25 min per ep',
      'episodes': 25.0,
      'rating': 'R - 17+ (violence & profanity)',
      'score': 6.85,
      'rank': 4754.0,
      'synopsis': 'Mao Lan continues growing into her path in life through what she learns while fighting. Her grandfather thinks that she has grown complacent and decides to train an adversary for her next Prime Mat appearance. Training with her friends and companions Mao Lan slowly advances through life.\r\n\r\n(Source: AniDB)',
      'cover': 'https://cdn.myanimelist.net/images/anime/6/23598l.jpg'},
     {'name': 'nintama rantarou',
      'english_title': 'Nintama Rantarou',
      'japanses_title': '??????????????????',
      'genre': 'Shounen',
      'type': 'TV',
      'source': 'Manga',
      'duration': '10 min',
      'episodes': 2.0,
      'rating': 'G - All Ages',
      'score': 7.09,
      'rank': 3654.0,
      'synopsis': 'Taking place in the Sengoku Period, Rantarou, Kirimaru and Shinbei are young students at Ninjutsu Academy, a school that teaches all kinds of youth how to become ninjas. Known as "Nintamas" (a contraction of ninja + tama [egg]), the main trio, and many other students at the school, must learn all sorts of unique skills to achieve their goal. Unfortunately, things aren\'t that simple, since our protagonists constantly find themselves failing their classes. \r\n\r\nWith strict ninja teachers such as Doi-sensei and Yamada-sensei, the mischievous girls from the Kunoichi class, an entire crew of pirates and dozens more interesting characters, anything can happen in the crazy world of Nintama.\r\n\r\nThe episodes are 7 minutes and thirty seconds long each, and each season (which there\'s currently 29 of) usually has a range of 60-90 episodes.',
      'cover': 'https://cdn.myanimelist.net/images/anime/6/74028l.jpg'},
     {'name': 'kyattou ninden teyandee',
      'english_title': 'Kyattou Ninden Teyandee',
      'japanses_title': '?????????????????????????????????',
      'genre': 'Shounen',
      'type': 'TV',
      'source': 'Original',
      'duration': '24 min per ep',
      'episodes': 54.0,
      'rating': 'G - All Ages',
      'score': 7.06,
      'rank': 3797.0,
      'synopsis': "In the city of Edoropolis, hundreds of mechanical animals live in harmony alongside each other. However, when Lord Wanko discovers that the shogun's chief advisor, Lord Korn, is plotting to take over the government, he knows that something must be done to preserve the peace. In order to thwart Korn's plans, Wanko forms the Nyankees???an elite ninja team led by the fearless Yattarou, who wields the mystic sword Masamasa. With all this power, the Nyankees seem unstoppable!\r\n\r\nBut Korn's schemes are not the only thing the team has to worry about. Secretly based out of the popular Pizza Cats restaurant, the Nyankees must keep their operations hidden while delivering piping-hot plates of pizza and justice.\r\n\r\n[Written by MAL Rewrite]",
      'cover': 'https://cdn.myanimelist.net/images/anime/1380/100202l.jpg'},
     {'name': 'lupin iii',
      'english_title': 'Lupin III',
      'japanses_title': '???????????????',
      'genre': 'Shounen',
      'type': 'TV',
      'source': 'Manga',
      'duration': '25 min per ep',
      'episodes': 23.0,
      'rating': 'PG-13 - Teens 13 or older',
      'score': 7.63,
      'rank': 1313.0,
      'synopsis': "Ars??ne Lupin III is the grandson of world-famous thief Ars??ne Lupin, and he's living up to his grandfather's memory as a high-profile thief himself. Due to his infamy, Lupin III attracts the attention of the persistent Inspector Zenigata of the ICPO, as well as rival criminals. Lupin III's criminal lifestyle even seeps into his love life. The main woman in Lupin III's world is femme fatale Fujiko Mine, who Lupin III can never tell is working with or against him. Follow Lupin and his gunman partner Daisuke Jigen on their quest to own the world???or at least the valuable bits!",
      'cover': 'https://cdn.myanimelist.net/images/anime/10/15625l.jpg'},
     {'name': 'lupin iii  part ii',
      'english_title': 'Lupin III: Part II',
      'japanses_title': '?????????????????????',
      'genre': 'Shounen',
      'type': 'TV',
      'source': 'Manga',
      'duration': '25 min per ep',
      'episodes': 155.0,
      'rating': 'PG-13 - Teens 13 or older',
      'score': 7.77,
      'rank': 978.0,
      'synopsis': "Lupin III chronicles the adventures of Arsene Lupin III, the world's greatest thief, and his partners in crime: master marksman Daisuke Jigen, beautiful and scheming Fujiko Mine and stoic samurai Goemon Ishikawa XIII. Lupin and his gang travel around the globe in search of the world's greatest treasures and riches and always keeping one step ahead of the tireless Inspector Zenigata, who has vowed to bring Lupin to justice. \r\n\r\n(Source: ANN)",
      'cover': 'https://cdn.myanimelist.net/images/anime/7/34035l.jpg'},
     {'name': 'lupin iii  part iii',
      'english_title': 'Lupin III: Part III',
      'japanses_title': '??????????????? - Part III',
      'genre': 'Shounen',
      'type': 'TV',
      'source': 'Manga',
      'duration': '24 min per ep',
      'episodes': 50.0,
      'rating': 'R+ - Mild Nudity',
      'score': 7.29,
      'rank': 2579.0,
      'synopsis': "Lupin III chronicles the adventures of Arsene Lupin III, the world's greatest thief, and his partners in crime: master marksman Daisuke Jigen, beautiful and scheming Fujiko Mine and stoic samurai Goemon Ishikawa XIII. Lupin and his gang travel around the globe in search of the world's greatest treasures and riches and always keeping one step ahead of the tireless Inspector Zenigata, who has vowed to bring Lupin to justice. \r\n\r\n(Source: ANN)",
      'cover': 'https://cdn.myanimelist.net/images/anime/1441/100440l.jpg'},
     {'name': 'city hunter',
      'english_title': 'City Hunter',
      'japanses_title': '????????????????????????',
      'genre': 'Shounen',
      'type': 'TV',
      'source': 'Manga',
      'duration': '24 min per ep',
      'episodes': 51.0,
      'rating': 'PG-13 - Teens 13 or older',
      'score': 7.92,
      'rank': 700.0,
      'synopsis': '"City Hunter" is a notorious contractor group with the call sign "XYZ." No matter the job, they will take it, cleaning up the scum on the streets of Tokyo. The key member of City Hunter is Ryou Saeba; armed with his trusty Colt Python and pinpoint accuracy, he works alongside willful tomboy Kaori Makimura.\r\n\r\nTogether they solve tough cases and tackle the numerous dangers that accompany their trade head-on. However, when he\'s not out hunting crooks and villains, Ryou finds pleasure in chasing beautiful ladies with only Kaori and her one hundred-ton hammer to keep him in check. From pickpockets and arms dealers to crime syndicates, nothing can stand in the way of Ryou Saeba when he takes aim at his next mission.\r\n\r\n[Written by MAL Rewrite]',
      'cover': 'https://cdn.myanimelist.net/images/anime/8/20587l.jpg'},
     {'name': 'd gray man',
      'english_title': 'D.Gray-man',
      'japanses_title': '???????????????????????????',
      'genre': 'Shounen',
      'type': 'TV',
      'source': 'Manga',
      'duration': '23 min per ep',
      'episodes': 103.0,
      'rating': 'PG-13 - Teens 13 or older',
      'score': 8.02,
      'rank': 556.0,
      'synopsis': 'Losing a loved one is so painful that one may sometimes wish to be able to resurrect them???a weakness that the enigmatic Millennium Earl exploits. To make his mechanical weapons known as "Akuma," he uses the souls of the dead that are called back. Once a soul is placed in an Akuma, it is trapped forever, and the only way to save them is to exorcise them from their vessel using the Anti-Akuma weapon, "Innocence."\r\n \r\nAfter spending three years as the disciple of General Cross, Allen Walker is sent to the Black Order???an organization comprised of those willing to fight Akuma and the Millennium Earl???to become an official Exorcist. With an arm as his Innocence and a cursed eye that can see the suffering souls within an Akuma, it\'s up to Allen and his fellow Exorcists to stop the Millennium Earl\'s ultimate plot: one that can lead to the destruction of the world.\r\n\r\n[Written by MAL Rewrite]',
      'cover': 'https://cdn.myanimelist.net/images/anime/13/75194l.jpg'}]
:::
:::
