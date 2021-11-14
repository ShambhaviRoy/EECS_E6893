import streamlit as st
import time
import numpy as np
import get_youtube_videos


#Add title and image
st.write("""
# EECS E6893 \n
# Personalized Company Research Dashboard
## Authored by Shambhavi Roy, Saravanan Govindarajan and Rahul Lokesh
Includes a few companies in the S&P500 Index \n
""")

#Create sidebar header for user input
st.sidebar.header("User Input")
company = st.sidebar.selectbox('Select company name', 
    ('Alphabet Inc. (GOOG)', 
    'Apple Inc. (AAPL)', 
    'Amazon.com, Inc. (AMZN)', 
    'Meta Platforms, Inc. (FB)', 
    'Microsoft Corporation (MSFT)', 
    'Netflix, Inc. (NFLX)'))
st.write('You selected:', company)


if company != None:
    video_urls = get_youtube_videos.youtube_search(company)

    for url in video_urls:
        st.video(url) 

st.button("Re-run")