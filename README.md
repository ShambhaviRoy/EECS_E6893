# EECS_E6893
Big Data Analytics Project: Personalized Company Research Dashboard (Group 46)

## Contributors- Group 46
<br> Shambhavi Roy (sr3767)</br>
<br> Saravanan Govindarajan (sg3896)</br>
<br> Rahul Lokesh (rl3164) </br>

## Abstract
<p> Stock market investors often require guidance in understanding current market conditions to make wise investment decisions. Our project addresses this concern and is aimed to provide users with centralized dashboard access to understand a company's current market condition using big data principles. For a given company name as user input, we seek to provide to its stock market information, relevant current YouTube videos, and real-time sentiment of its stock in the market. Having access to these three modalities of data with sentiment analysis would be useful for traders to conduct market research on a specific company in depth. </p>

## Data 
<p> We are utilizing data from several sources in our project. This includes financial data collected using Yahoo Finance API to display real-time stock price, video data from YouTube API to filter and display videos, and real-time tweets from Twitter API to perform sentiment analysis.
We have also used the Twitter Tweets Data for Sentiment Analysis dataset to experiment with using a BERT model for sentiment analysis. </p>

## Language: 
Python, Django

## Analytics: 
<p> For a given user input of company name, we queried the Yahoo Finance API to query the latest stock price by the minute. Next, we used the YouTube Data API to retrieve the top 10 news videos of the company searched using the tags: Company name, it's stock ticker, and 'news'. Finally, we queried the Twitter API using these tags to retrieve the latest company news on which we performed sentiment analysis using the TextBlob library. </p>
