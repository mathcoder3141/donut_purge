from datetime import datetime, timedelta, date
from slack_bolt import App
from dotenv import load_dotenv
import pandas as pd
import time

load_dotenv()

SLACK_APP_TOKEN=os.environ.get('SLACK_APP_TOKEN')
SLACK_SIGNING_SECRET=os.environ.get('SLACK_SIGNING_SECRET')

app = App(
    token=SLACK_APP_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET
)

donut_buddies = 'C0184AJUX3K'
client = app.client
file_analytics_date = date.strftime(date.today() - timedelta(days=2), format='%b %d, %Y')

# Gets members of #donut-buddies
donut_members = client.conversations_members(channel=donut_buddies, limit = 500)['members']

# uses the OS module to determine what the member analytics
# filepath is

if os.uname().sysname == 'Darwin':
    file = f"/Users/randallhall/Downloads/Locally Optimistic Member Analytics All time - {file_analytics_date}.csv"
elif os.uname().sysname == 'Linux':
    file = f"/home/randall/Downloads/Locally Optimistic Member Analytics All time - {file_analytics_date}.csv"

# Reads in file using pandas
# and filters down dataframe to those who weren't active in last 14 days
lo_analytics = pd.read_csv(file)
lo_analytics["Last Active"] = pd.to_datetime(lo_analytics['Last active (UTC)'])
last_14 = lo_analytics[lo_analytics["Last Active"] >= pd.Timestamp(date.today() - timedelta(days=14))]

# Store to variable people who are in donut_members that are not in
# lo_analytics_last_active
not_active_id = [member for member in donut_members if member not in last_14['User ID'].tolist()]

not_active_name = []
for user_id in not_active_id:
    user = client.users_info(user=user_id)
    real_name = user['user']['profile']['real_name']
    display_name = user['user']['profile']['display_name']
    if not user['user']['is_bot']:
        not_active_name.append(user_id)
        print(f"Real Name: {real_name} | Display Name: {display_name} | User ID: {user_id}")
print(len(not_active_name))
#         # automated for kicking not used in this version
#         # conversations.kick(channel=donut_buddes, user=user_id)