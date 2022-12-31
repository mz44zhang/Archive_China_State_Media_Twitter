from twarc import Twarc2, expansions
import json
import pandas as pd
import re
import pickle

# Replace your bearer token below
client = Twarc2(
    bearer_token="YOUR TOKEN HERE")


def get_timeline_tweets(userid):
    # This timeline functions gets the Tweet timeline for a specified user
    try:
        user_timeline = client.timeline(user=userid)
        all_tweets = []
        # Twarc returns all Tweets for the criteria set above, so we page through the results
        for page in user_timeline:
            # The Twitter API v2 returns the Tweet information and the user, media etc.  separately
            # so we use expansions.flatten to get all the information in a single JSON
            result = expansions.flatten(page)
            for tweet in result:
                # Here we are printing the full Tweet object JSON to the console
                all_tweets.append(tweet)

        outfile = open(userid + '.pickle', 'wb')
        pickle.dump(all_tweets, outfile)
        outfile.close()
        print("------- finishing ", userid, "---------")
    except:
        with open('error_', userid, '.txt', 'w') as f:
            f.write(userid)
        print("------- not found ", userid, "---------")


# ---------------------------------------------------------------
def archive_list_userid(userids):
    for userid in userids:
        try:
            get_timeline_tweets(userid)
        except:
            with open('error_', userid, '.txt', 'w') as f:
                f.write(userid)


archive_list_userid(clean_usereid[124:])

#------------------------------------------------------------------
# pickle_file = 'rgrus.pickle'
def pickle_to_csv(pickle_file):
    file = open(pickle_file, 'rb')
    data = pickle.load(file)
    file.close()
    df = pd.DataFrame.from_dict(data)
    df.to_csv('Archive_China_State_Media_Twitter/'+pickle_file[:-7]+'.csv')

pickle_to_csv('rgrus.pickle')


import glob
# absolute path to search all text files inside a specific folder
path = r'*.pickle'
files = glob.glob(path)

for file in files:
    pickle_to_csv(file)
    print("------- finishing ",file,'----------')


