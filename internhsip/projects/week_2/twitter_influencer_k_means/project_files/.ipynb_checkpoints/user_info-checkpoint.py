def get_user_tweets_info(handles):
    
    cols = ['id', 'name', 'screen_name', 'description', 
            'statuses_count', 'friends_count', 'followers_count',
            'account_age_days', 'avg_daily_tweets', 'hashtags',
            'user_mentions','favorite_count', 'retweet_count',]
    
    # dataframe that would be returned at the end
    df = pd.DataFrame(columns=cols)
    #print(df)
    handle_data = []
    off_users = []
            
    if len(handles) > 0:  
        for handle in handles:
            value_list = []
            print("Getting data for " + handle)
            # this helps avoid Tweepy errors like suspended users or user not ound errors
            try:
                item = api.get_user(handle)
            except tweepy.TweepError as e:
                continue
            value_list+= item.id_str, item.name, item.screen_name,\
            item.description, item.statuses_count, item.friends_count, item.followers_count
            
            #get average daily tweets
            
            no_tweets = item.statuses_count
            #value_list.append(no_tweets)
            account_created_date = item.created_at
            delta = datetime.utcnow() - account_created_date
            account_age_days = delta.days
            value_list.append(str(account_age_days))
            #print(str(account_age_days))
            if account_age_days > 0:
                   value_list.append(int(float(no_tweets)/float(account_age_days)))
                    
            hashtags = []
            mentions = []
            favorite_count =[]
            retweet_count=[] 
            tweets = [] 
            tweet_count = 0
            end_date = datetime.utcnow() - timedelta(days=30)
            

            for status in Cursor(api.user_timeline, id=handle,
                              #  trim_user=True, exclude_replies=True
                        ).items(500):
#                 tweets.append(status._json['text'])
#                 print(tweets)
#                 break
                
                #tweets.append(status['text'])
                tweet_count+= 1
                if hasattr(status, "entities"):
                    entities = status.entities

                # get hashtags
                if "hashtags" in entities:
                    for ent in entities["hashtags"]:
                        if ent is not None:
                            if "text" in ent:
                                hashtag = ent["text"]
                                if hashtag is not None:
                                    hashtags.append(hashtag)
                # get usermentions
                if "user_mentions" in entities:
                    for ent in entities["user_mentions"]:
                        if ent is not None:
                            if "screen_name" in ent:
                                name = ent["screen_name"]
                                if name is not None:
                                    mentions.append(name)

                # get retweets    
                if hasattr(status, "retweet_count"):
                    retweets = status.retweet_count
                    if retweets is not None:
                        retweet_count.append(retweets)
                        
                # favorite count     
                if hasattr(status, "favorite_count"):
                    likes = status.favorite_count 
                    if likes is not None:
                        favorite_count.append(likes)
                if status.created_at < end_date:
                    break
                    
            
            value_list.append(len(hashtags))
            value_list.append(len(mentions))
            value_list.append(sum(favorite_count))
            value_list.append(sum(retweet_count))
            handle_data.append(value_list)
            
            tweet_series = pd.Series(tweets) 
            df = df.append(pd.DataFrame([value_list], columns=cols))
            df=pd.concat([df, pd.DataFrame(tweet_series)], axis=1)
            df = df.rename(columns={0:'tweet'})
            #print(df)
            break
    return df
