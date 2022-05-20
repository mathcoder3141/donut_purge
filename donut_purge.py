from datetime import datetime, timedelta, date
from slack_bolt import App
from dotenv import load_dotenv
import pandas as pd
import time
import os
import pprint

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

# Reads in file using pandas
# and filters down dataframe to those who weren't active in last 60 days
file = f"/home/randall/Downloads/Locally Optimistic Member Analytics All time - May 17, 2022.csv"
lo_analytics = pd.read_csv(file)
lo_analytics["Last Active"] = pd.to_datetime(lo_analytics['Last active (UTC)'])
last_60 = lo_analytics[lo_analytics["Last Active"] >= date.today() - timedelta(days=60)]

# Store to variable people who are in donut_members that are not in
# lo_analytics_last_active
not_active_id = [member for member in donut_members if member not in last_60['User ID'].tolist()]

not_active_name = []
for user_id in not_active_id:
    user = client.users_info(user=user_id)
    real_name = user['user']['profile']['real_name']
    display_name = user['user']['profile']['display_name']
    if not user['user']['is_bot']:
        pprint.pprint(f"Real Name: {real_name} | Display Name: {display_name}")
#         # automated for kicking not used in this version
#         # conversations.kick(channel=donut_buddes, user=user_id)