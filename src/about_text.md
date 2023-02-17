# Exploratory Data Analysis (EDA) on Anime Data from MyAnimeList
--------------------------------------

<p align="center">
    <img src="https://github.com/RealXun/EDA_ANIME/blob/main/src/images/Cover_images/cover.png" width="1000">
</p>

## Introduction to Anime (Japanese Animation)
--------------------------------------

<div align="justify">"Anime" is the term used by Western audiences to describe Japanese animated films and television programs (although it is used to describe any animation in Japan).
  
At first, animated pieces were known as senga eiga (線画映画, line-drawing film) or senga kigeki (線画喜劇, cartoon comedy film), which were often specified in katakana (cartoon comedy, カートン・コメディ, cartoon comedy).

Between 1907 and 1912 the first animated shorts were made, usually associated with political cartoonists, and in 1933 came the first piece of Japanese animation or spoken Japanese anime, Chikara to Onna Yo no Naka.

The following years would be, logically, marked by the war, and almost any audiovisual piece would be focused on a propaganda use. In 1948, one of the most important studios, Toei Animation, was born, and in 1958 it made the first color film, Hakujaden (白蛇伝, The Tale of the White Snake).

It was probably not until 1962 that the word anime began to be used, in a standardized way, in Japan to refer to animated productions. It seems that the film magazine Eiga Hyoron was the first.

During the 1970s some of the most popular anime in the country were born, such as Ashita no Joe (1970, Fuji TV), Arupusu no Shoujo Haiji (Heidi, 1974, Fuji TV), Lupin III (1971, YTV), Gatchaman (1972, Fuji TV), Mazinger Z (1972, Fuji TV), Uchuu Senkan Yamato (1974, YTV), Candy Candy (1976, TV Asahi) or Kidou Senshi Gundam (1979, NBN), but it was not until the 1980s when a real revolution would take place.

The first half of the 1990s saw the emergence of a new type of animation that was ready to blow the brains of viewers and burst the expectations of everything seen until then in cartoons. It was Japanese anime and there is no doubt that the two culprits of this irruption were Dragon Ball and Akira, two authentic bombshells that made us become aware of this new style of animation. These phenomena were accompanied by the arrival of private television stations, with many hours of programming to fill, which were busy with lots of Japanese anime series that were cheap to license. New publishers emerged, acquiring the rights to anime films destined to fill the shelves of video stores in response to this new demand.

Today's teenagers are getting hooked on Japanese anime again. It's happening to them as it happened in the 90s, for example, with Dragon Ball, The Knights of the Zodiac (Saint Seiya) or Chicho Earthquake (Chicho Terremoto - Dash Kappei). Not to mention the Dragon Ball phenomenon. It is true that now there are also many adults who maintain their taste for the series and movies created by the famous Japanese anime studios, and that has an influence.

Anime may be going through one of its best periods in history. The genre has audiences almost everywhere in the world. The stories are reaching diverse audiences and, technology permitting, a series of tools are available to improve manga adaptations or new proposals. A boom.</div>

## Dataset Used
--------------------------------------

The [dataset](https://github.com/RealXun/EDA_ANIME/blob/main/src/data/cleaned.csv) used was created using a [script](https://github.com/RealXun/EDA_ANIME/blob/main/src/utils/api_exctraction.py) to gather the data from [MyAnimeList](https://myanimelist.net/) uing [Jikan API](https://docs.api.jikan.moe/)

Here is the [cleaned dataset(Pickle file)](https://github.com/RealXun/EDA_ANIME/blob/main/src/data/anime.pkl)

## About the work done
--------------------------------------

Usually when we think of Data Science, Machine Learning or Artificial Intelligence, we think of the models and the wonderful applications, but the first step is usually to explore and clean the data.

The purpose of this EDA is getting insights out of data while exploring it (after doing some Data cleaning/preparation/transformation) in order to answer some previos questions and prove some hypothesis.

The parts in the project are as follows:

- Introduction
- Getting the information
- Data Preparation, Cleaning and Descriptive Analysis
- Data and Visual Analysis
- Conclusions
- References

[Click here to open the Jupyter Notebook](https://github.com/RealXun/EDA_ANIME/blob/eb2d58dcfe9fffe1b481e7d7da5557491d2300a3/src/EDA_Anime.ipynb)

[Click here to open the utils file with the definitions](https://github.com/RealXun/EDA_ANIME/blob/main/src/utils/utils.py)

[Click here if you only want the script to extract information](https://github.com/RealXun/EDA_ANIME/blob/main/src/utils/api_exctraction.py)

## Structure
--------------------------------------
- Introduction
- Getting the information
- Data Preparation, Cleaning and Descriptive Analysis
    - Importing libraries and checking the raw information
    - Next esteps explanation
    - Cleaning the columns with empty lists
    - About released, Scored_by, Score and Rank
    - Dealing with Audience and Rating columns
    - Removing unncesary columns
    - Change null values to Unknown
    - Dealing with Zero values in N_Episodes column
    - Standaricing duration column
    - Checking results after the cleaning process
    - Saving cleaned df using Pickle
    - Opening cleaned df using Pickle
- Data and visual Analysis
    - One Dimensional-Analysis
        - Numerical Columns
            - N_Episodes
            - Duration
            - Score
            - Rank
            - Released
        - Categorical Columns
            - Type
            - Source
            - Rating
            - Genre
            - Theme
            - Producers
            - Studios
    - Bi-Dimensional-Analysis
        - Score and Type
        - Score and Source
        - Score and Number of Episodes
        - Score and Duration of the episodes
        - Score and Rating
        - Score and Genre
        - Score and Theme
        - Score and Producers
        - Score and Studios
- Conclusions

## Libraries used
--------------------------------------
Script used to gather the information
```
import requests, json, os, sys, time
import pandas as pd
from datetime import datetime
```

utils file with the definitions
```
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import os
import sys
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from scipy.stats import shapiro
from scipy.stats import anderson
from scipy.stats import normaltest
from scipy.stats import spearmanr

os.chdir(os.path.dirname(sys.path[0]))
```

EDA notebook
```
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import sys
import seaborn as sns
from collections import Counter
from utils import utils
import warnings
import pickle

warnings.simplefilter(action='ignore', category=FutureWarning)
```

## Questions and Hypothesis
--------------------------------------
- Which is the most common anime source?
- Which is the most coomon anime typ?
- PG-13 - Teens 13 or older has more animes int he top 10.
- Is PG-13 - Teens 13 or older the most typical rating for animea?
- Which genre is most release? Is this gender the more voted between the audience?
- Producer and Studio with more animes
- Find out the most voted Theme and Genre for an anime. Are this the ones with more releases?
- More Number of Episodes does not mean higher score. Therefore, Is there any Correlation between Score and of number of episodes?
- Longer duration of the episodes means higher score. Therefore, Is there any Correlation between Score and Duration of the episodes?
- Best Genres and themes to use in an anime.
- which producers and studios would be better to hire.
- Best source to create an anime
- most valued Types by users
- etc...

## Thanks
--------------------------------------

I would like to say thanks to the professors and assistant professors of The Bridge Bootcamp, as well as my classmates.

Special thanks to my classmate Roger for his support, help and all the time listening to my ideas.

Thank you.

