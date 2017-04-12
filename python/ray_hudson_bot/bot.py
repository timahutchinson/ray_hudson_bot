from sys import stderr
import random
import time

import praw

players = ['messi', 'di maria']

r = praw.Reddit('ray_hudson_bot', user_agent='Ray Hudson comment bot for r/soccer v0.1 by tskee2')
subreddit = r.subreddit('soccer+barca')

j = 0
replied = []
while True:
    print "Waking..."
    i = 0
    for submission in subreddit.new(limit=10):
        i += 1
        if submission.shortlink not in replied:
            print "Checking submission #%s..." % i
            for player in players:
                if player in submission.title.lower():
                    with open('../../data/%s.txt' % player, 'r') as f:
                        print "Replying to post: %s ..." % submission.shortlink
                        lines = f.readlines()
                        line = lines[random.randint(0,len(lines)-1)]
                        submission.reply(line)
                        replied.append(submission.shortlink)
                        break
    j += 1
    if j == 11:
        replied = []
        j = 0
    for i in range(60,0,-1):
        stderr.write("\rSleeping for %s seconds..." % i)
        time.sleep(1)
    print ''
    
