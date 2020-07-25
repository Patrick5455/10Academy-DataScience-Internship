import pandas as pd
from env import api
def get_tweets(handles):
    cols = ['handle', 'tweet_text', 'tweet_date']
    data = []
    df = pd.DataFrame(columns=cols)
    for user in handles: 
        user_data = {} 
        for status in Cursor(api.user_timeline,  screen_name=user, tweet_mode="extended").items(500):
            user_data['handle'] = user
            user_data['tweet_text'] = status._json['full_text']  
            user_data['tweet_date'] = status._json['created_at']
            data.append(user_data)
            df = df.append(pd.DataFrame(data)) 
    return df