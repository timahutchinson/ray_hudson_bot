import time

import praw

players = ['messi', 'neymar']

r = praw.Reddit('ray_hudson_bot', user_agent='Ray Hudson comment bot for r/soccer v0.1 by tskee2')
subreddit = r.subreddit('soccer')

for submission in subreddit.stream.submissions():
    print submission.title
    for player in players:
        if player in submission.title.lower():
            with open('../../data/%s.txt' % player, 'r') as f:
                # count lines, pick random one, post reply
                pass
            break
