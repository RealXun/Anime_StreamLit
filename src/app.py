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
from body import testing
from body import un_based_rate
from body import un_based_feat
from body import sup_id
from body import about
from body import about_me


with st.sidebar:
    choose = option_menu("Anime System Recommendator", ["About", "Based on ratings", "Based on Features", "Using user ID", "Testing","About the Creator"],
                         icons=['house', 'camera fill', 'kanban', 'book','person lines fill', 'book'],
                         menu_icon="app-indicator", default_index=0,
                         styles={"container": {"padding": "5!important", "background-color": "#fafafa"},
                                "icon": {"color": "orange", "font-size": "25px"}, 
                                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                                "nav-link-selected": {"background-color": "#02ab21"},
                                }
                        )

if choose == "About":
    about.it_is_about()
        
elif choose == "Based on ratings":
    un_based_rate.uns_bara()

elif choose == "Based on Features":
    un_based_feat.uns_feat()

elif choose == "Using user ID":
    sup_id.user_id()

elif choose == "Testing":
    testing.test_it()

elif choose == "About the Creator":
    me.about_me()
