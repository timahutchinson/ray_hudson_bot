from sys import stderr
import random
import time

import praw

def should_post(submission, replied):
    players = ['messi', 'di maria', 'iniesta', 'ronaldo']
    if submission.shortlink not in replied:
        for player in players:
            if player in submission.title.lower():
                return True, player
            else:
                return False, None
    else:
        return False, None
            

def submit(submission, player, replied):
    comment_template = "%s \n\n \n\n ***** \n\n*I'm a bot. If you have any feedback, please* [*message me.*](https://www.reddit.com/message/compose?to=ray_hudson_bot&subject=Feedback)"
    with open('../../data/%s.txt' % player, 'r') as f:
        print "Replying to post: %s ..." % submission.shortlink
        lines = f.readlines()
        line = lines[random.randint(0,len(lines)-1)]
        submission.reply( comment_template % line )
        replied.append(submission.shortlink)

def sleep_timer(seconds):
    for i in range(seconds, 0, -1):
        stderr.write("\rSleeping for %s seconds..." % i)
        time.sleep(1)
    print ''

def main():
    j = 0
    replied = []
    r = praw.Reddit('ray_hudson_bot', user_agent='Ray Hudson comment bot for r/soccer v0.1 by tskee2')
    subreddit = r.subreddit('soccer+barca+realmadrid')
    while True:
        print "Waking..."
        i = 0
        for submission in subreddit.new(limit=10):
            i += 1
            print "Checking submission #%s..." % i
            post, player = should_post(submission, replied)
            if post:
                submit(submission, player, replied)
        j += 1
        if j == 11:
            replied = []
            j = 0
        sleep_timer(60)
    
if __name__ == '__main__':
    main()
