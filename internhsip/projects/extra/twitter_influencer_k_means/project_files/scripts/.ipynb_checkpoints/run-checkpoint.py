from env import api
import pandas as pd
from user_info import get_user_tweets_info
from get_tweet import get_tweets

handles = pd.read_csv('allHandles.csv', index_col=0)
handles = handles.handles.to_list()

# run funtion get_tweets
tweet_data = get_tweets(handles) 
# save as csv
path = os.getcwd()
tweet_data.drop_duplicates().to_csv(os.path.join(path, "tweet_data.csv"))

# run function get_tweets
users_info = get_user_tweets_info(handles)
# save to file
path = os.getcwd()
users_info.drop_duplicates().to_csv(os.path.join(path, "users_info.csv"))