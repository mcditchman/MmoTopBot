import praw
import string
import OAuth2Util

subreddits = list()
reddit = praw.Reddit('Top MMORPG post aggregator')

# Setup Authentication
oAuth = OAuth2Util.OAuth2Util(reddit)
oAuth.refresh(force=True)

print('!! MMORPG Top Bot has started !!')

# Get MMORPG sidebar info
sidebar =  reddit.get_subreddit('mmorpg').description.split('\n')

# Grab popular MMO list from sidebar
index = 0
start = False
for line in sidebar:
    if line == '###**Popular MMO Subreddits**':
        start = True
        continue
    if start and line != '':
        loc = line.index('/r/') + 3
        subreddits.append(line[loc:-1])
        index += 1 
    if start and line == '' and len(subreddits) > 0:
        start = False
        break

# Create the output
print('Creating output...');
output = 'Greetings adventurers!\n\nI have compiled a list of all the top posts from last week for all of the popular MMO subreddits in the sidebar. It may be news or it may be fluff but its all here in one place!\n\n'
output += 'Subreddit | Top Post Last Week | Points\n---|---|---\n'

# Loop through subreddits and get top post from past week 
for sub in subreddits:
    submissions = reddit.get_subreddit(sub).get_top_from_week(limit=1)
    for post in submissions:
        output += '/r/{0} | [{1}]({2}) | {3}\n'.format(sub, post.title, post.url, post.score)
    
output += '\n\n---\n\n I am a bot and this is an automated post. Please direct any questions to the mods via modmail.\n\n*beep boop*'

# Submit post to subreddit
print('Making post...');
reddit.submit('mmorpg','Top MMO posts last week, tonight!',output)

