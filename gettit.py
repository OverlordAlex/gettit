#!/usr/bin/env python

import argparse
import os
import praw
import sys

term_width = 120
max_title_length = 60
userfile = '.get/cleartext'


class bcolours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class procrastination:
    def __init__(self):
        self._login()

    def _login(self):
        raise NotImplementedError

    def fetch_articles(self):
        raise NotImplementedError

    def get_articles(self):
        raise NotImplementedError


class reddit(procrastination):

    user = None

    def __init__(self):
        self.user = praw.Reddit(user_agent='gettit command-line viewer')
        #self._login(user)

    def _login(self, userfile):
        username = 'user'
        password = 'pass'
        self.user.login(username, password)


    def fetch_articles(self, subreddit):
        posts = []
        sub = self.user.get_subreddit(subreddit)
        for post in sub.get_top():
            sub_string = str(post.subreddit)
            posts.append((sub_string + '/' + post.title, post.score, post.num_comments))

        return posts

    def get_articles(self, subreddit):
        pass


class get:

    curr = None

    def __init__(self):
        parser = argparse.ArgumentParser(
        usage='gettit <command> [<args>]',
        description='Just git. Nothing to see here, move along.',
        epilog='I recommend alias get=gettit')

        parser.add_argument('command', help='Subcommand to run')

        args = parser.parse_args(sys.argv[1:2])

        if not hasattr(self, args.command):
            print 'gettit: \'%s\' is not a recognized gettit command. See \'gettit --help\'' % args.command
            parser.print_help()
            exit(1)

        getattr(self, args.command)()


    def pull(self):
        parser = argparse.ArgumentParser(
                description='Fetch from and integrate with a website')

        parser.add_argument('website',
                            nargs='?',
                            const='none')

        parser.add_argument('subpage',
                            nargs='?',
                            const='all')

        args = parser.parse_args(sys.argv[2:])

        if args.website is 'none':
            # display the last pull that we got
            articles = curr.get_articles(args.subpage)
        else:
            curr = classes[args.website]()
            articles = curr.fetch_articles(args.subpage)

            max_comments = max(articles, key=lambda x: x[2])
            max_comments = max_comments[2]

            for title, score, comments in articles:
                if len(title) > max_title_length:
                    title = title[:max_title_length-3] + '...'

                print title.ljust(max_title_length), '|', score, bcolours.OKGREEN + '+'*int((comments*1.0/max_comments)*(term_width-max_title_length-6)) + bcolours.ENDC

        #print bcolours.OKGREEN + "++++" + bcolours.ENDC
        #print bcolours.FAIL + "----" + bcolours.ENDC




classes = {'reddit':reddit}


if __name__ == '__main__':
    get()
