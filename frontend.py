import streamlit as st
import time
import numpy as np
import get_youtube_videos

company = st.selectbox('Select company name', ('Apple (AAPL)', 'Facebook (FB)', 'Microsoft (MSFT)'))
st.write('You selected:', company)
# selected = True

video_urls = get_youtube_videos.youtube_search(company)

for url in video_urls:
    st.video(url) 

# if selected:
    # video_urls = ['https://www.youtube.com/watch?v=TSii5NIgbYQ', 
    # 'https://www.youtube.com/watch?v=7Y_RZf5i_LE', 
    # 'https://www.youtube.com/watch?v=Qw6UCwCt4bE',
    # 'https://www.youtube.com/watch?v=6W9s4JjiSH0',
    # 'https://www.youtube.com/watch?v=k1VUZEVuDJ8',
    # 'https://www.youtube.com/watch?v=uwutHtN-ks0',
    # 'https://www.youtube.com/watch?v=nImSo1tbnzQ',
    # 'https://www.youtube.com/watch?v=Uh9643c2P6k', 
    # 'https://www.youtube.com/watch?v=S-nHYzK-BVg']

    

# st.video('https://www.youtube.com/watch?v=BSzSn-PRdtI')

# progress_bar = st.sidebar.progress(0)
# status_text = st.sidebar.empty()
# last_rows = np.random.randn(1, 1)
# chart = st.line_chart(last_rows)

# for i in range(1, 101):
#     new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
#     status_text.text("%i%% Complete" % i)
#     chart.add_rows(new_rows)
#     progress_bar.progress(i)
#     last_rows = new_rows
#     time.sleep(0.05)

# progress_bar.empty()

# # Streamlit widgets automatically run the script from top to bottom. Since
# # this button is not connected to any other logic, it just causes a plain
# # rerun.
st.button("Re-run")