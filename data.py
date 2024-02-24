# This .py file does the following after execution from the command line
#    - Calls the Reddit API 
#    - requests and verifies access to Reddit API with credentials stored in seperate credentials.py file
#    - Scrapes two subreddits, 'Repulican' and 'democrats', and stores information in a dataframe
#    - Reads in 'rep_vs_dem_data.csv', appends newly scraped data, drops duplicate rows and first 
#      unnecessary column, saves back to csv
#    - In terminal outputs current time, shape of cmaster_df, most recent 'after' endpoint markers

# Source: Referenced GA Breakfast Hour and GA Lessons 5.01, 5.02 

# Import Libraries
import pandas as pd
import requests
import time
import credentials

# Setup Credentials and pull 'after' endpoints from last scrape
client_id = credentials.client_id()
client_secret =  credentials.client_secret()
user_agent =  credentials.user_agent() 
username =  credentials.username() 
password =  credentials.password()
dem_after =  credentials.dem_after() 
rep_after =  credentials.rep_after() 

# Establish scrape process
auth = requests.auth.HTTPBasicAuth(client_id, client_secret)

data = {
    'grant_type': 'password',
    'username': username, 
    'password': password
}

# Create application header
headers = {'User-Agent': 'jr/0.0.1'}
res = requests.post(
    'https://www.reddit.com/api/v1/access_token',
    auth = auth,
    data = data,
    headers = headers)
print(res)

# Request and verify access with Reddit API
token = res.json()['access_token']
headers['Authorization'] = f'bearer {token}'
requests.get('https://oauth.reddit.com/api/v1/me', headers=headers).status_code == 200

# Set parameters to maximum posts and latest 'after' endpoint marker
dem_params = {'limit': 100, 'after': dem_after}
rep_params = {'limit': 100, 'after': rep_after}

# Request data from democrat and Republican subreddit
base_url = 'https://oauth.reddit.com/r/'
subreddit = 'democrats'
res_dem = requests.get(base_url + subreddit, headers = headers, params = dem_params)
base_url = 'https://oauth.reddit.com/r/'
subreddit = 'Republican'
res_rep = requests.get(base_url + subreddit, headers = headers, params = rep_params)

# Cycle through posts gathering desired information from Republican and democrat scrape
dem = []
for i in range(len(res_dem.json()['data']['children'])):
    post = {}
    post['title'] = res_dem.json()['data']['children'][i]['data']['title']
    post['domain'] = res_dem.json()['data']['children'][i]['data']['domain']
    post['author'] = res_dem.json()['data']['children'][i]['data']['author']
    post['upvote_ratio'] = res_dem.json()['data']['children'][i]['data']['upvote_ratio']
    post['id'] = res_dem.json()['data']['children'][i]['data']['id']
    post['created_utc'] = time.ctime(res_dem.json()['data']['children'][i]['data']['created_utc'])
    post['subreddit'] = res_dem.json()['data']['children'][i]['data']['subreddit']
    dem.append(post)  
dem = pd.DataFrame(dem)

rep = []
for i in range(len(res_rep.json()['data']['children'])):
    post = {}
    post['title'] = res_rep.json()['data']['children'][i]['data']['title']
    post['domain'] = res_rep.json()['data']['children'][i]['data']['domain']
    post['author'] = res_rep.json()['data']['children'][i]['data']['author']
    post['upvote_ratio'] = res_rep.json()['data']['children'][i]['data']['upvote_ratio']
    post['id'] = res_rep.json()['data']['children'][i]['data']['id']
    post['created_utc'] = time.ctime(res_rep.json()['data']['children'][i]['data']['created_utc'])
    post['subreddit'] = res_rep.json()['data']['children'][i]['data']['subreddit']
    rep.append(post) 
rep = pd.DataFrame(rep)

# Initial append and write to csv
#master_df = pd.concat([dem, rep], ignore_index = True)
#master_df.to_csv('rep_vs_dem_data.csv')

# Read in .csv, append new data, drop 'Unnamed: 0' and duplicates, save to csv
master_df = pd.read_csv('./datasets/rep_vs_dem.csv')
master_df = pd.concat([master_df, dem, rep], ignore_index = True)
master_df.drop(columns = 'Unnamed: 0', inplace = True)
master_df.drop_duplicates(subset = 'id', inplace = True)
master_df.to_csv('./datasets/rep_vs_dem.csv')

# Print useful information in terminal
print(time.ctime(time.time()))
print(master_df.shape)
print(f'dem_after: {res_dem.json()["data"]["after"]}')
print(f'rep_after: {res_rep.json()["data"]["after"]}')