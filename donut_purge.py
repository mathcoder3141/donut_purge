from datetime import datetime, timedelta, date
from slack_bolt import App
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import csv
import pandas as pd
import time
import os

load_dotenv()

SLACK_APP_TOKEN=os.environ.get('SLACK_APP_TOKEN')
SLACK_SIGNING_SECRET=os.environ.get('SLACK_SIGNING_SECRET')

app = App(
    token=SLACK_APP_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET
)

donut_buddies = 'C0184AJUX3K'
client = app.client

# Gets members of #donut-buddies
donut_members = client.conversations_members(channel=donut_buddies, limit = 500)['members']

# uses the OS module to determine what the member analytics
# filepath is

if os.uname().sysname == 'Darwin':
    file = f"/Users/randallhall/Downloads/Locally Optimistic Member Analytics All time - Nov 25, 2024.csv"
elif os.uname().sysname == 'Linux':
    file = f"/home/randall/Downloads/Locally Optimistic Member Analytics All time - Nov 25, 2024.csv"

# Reads in file using pandas
# and filters down dataframe to those who weren't active in last 21 days
lo_analytics = pd.read_csv(file)
lo_analytics["Last Active"] = pd.to_datetime(lo_analytics['Last active (UTC)'])
last_21 = lo_analytics[lo_analytics["Last Active"] >= pd.Timestamp(date.today() - timedelta(days=21))]

# Store to variable people who are in donut_members that are not in
# lo_analytics_last_active
not_active_id = [member for member in donut_members if member not in last_21['User ID'].tolist()]

not_active_name = []
with open('inactive_donut_buddies.csv', 'w', newline='') as looker_descriptions:
    inactive_writer = csv.writer(looker_descriptions)
    inactive_writer.writerow(['Real Name', 'Display Name', 'User ID'])
    for user_id in not_active_id:
        user = client.users_info(user=user_id)
        real_name = user['user']['profile']['real_name']
        display_name = user['user']['profile']['display_name']
        if not user['user']['is_bot']:
            not_active_name.append(user_id)
            inactive_writer.writerow([real_name, display_name, user_id])
            print(f"Real Name: {real_name} | Display Name: {display_name} | User ID: {user_id}")
print(len(not_active_name))
