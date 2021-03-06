from sys import stderr
from os.path import exists
import random
import time

import praw

def get_subreddit():
    '''Connect to reddit API and pull subreddit data'''
    r = praw.Reddit('ray_hudson_bot', user_agent='Ray Hudson comment bot for r/soccer v0.1 by tskee2')
    subreddit = r.subreddit('soccercirclejerk+realmadrid+football+sports+spanishfootball+laliga+halamadrid')
    return subreddit

def should_post(submission, replied):
    '''Check if a submission contains one of the keywords and should be replied to'''
    players = {
               'messi':'messi', 'neymar':'neymar', 'iniesta':'iniesta', 'di maria':'di maria', 'ronaldo':'ronaldo',
               'cristiano':'ronaldo'
               }
        
    if submission.shortlink not in replied:
        for player in players.keys():
            if player in submission.title.lower():
                return True, players[player]
        else: return False, None
    else:
        return False, None
            
def submit(submission, player, replied):
    '''Construct and post a reply to a submission'''
    comment_template = "%s \n\n \n\n ***** \n\n*I'm a bot. If you have any feedback, please* [*message me.*](https://www.reddit.com/message/compose?to=ray_hudson_bot&subject=Feedback)"
    print "Replying to post: %s ..." % submission.shortlink
    with open('../../data/%s.txt' % player, 'r') as f:
        lines = f.read().split('\n')[:-1] # Ignore empty string from trailing newline on last line in file
        line = random.choice(lines)
        submission.reply( comment_template % line )
    replied = add_to_replied(replied, submission.shortlink)

def add_to_replied(replied, shortlink):
    '''Add shortlink to list of replied posts and write to text file in case of bot crash'''
    with open('../../data/replied.txt', 'a') as f:
        f.write('%s\n' % shortlink)
    replied.append(shortlink)
    print "Added %s to replied list." % shortlink
    return replied

def sleep_timer(seconds):
    for i in range(seconds, 0, -1):
        stderr.write("\rSleeping for %s seconds..." % i)
        time.sleep(1)
    print ''

def main():
    j = -1
    if exists('../../data/replied.txt'):
        with open('../../data/replied.txt', 'r') as f:
            replied = f.read().split('\n')
    else:
        replied = []
    subreddit = get_subreddit()
    while True:
        print "Waking..."
        i = 0
        for submission in subreddit.new(limit=50):
            i += 1
            print "Checking submission #%s..." % i
            post, player = should_post(submission, replied)
            if post:
                try:
                    submit(submission, player, replied)
                    submission.upvote()
                except:
                    pass
        j += 1
        if j == 10000:
            replied = []
            j = 0
        sleep_timer(60)
    
if __name__ == '__main__':
    main()
