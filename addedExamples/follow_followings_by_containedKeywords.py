"""
    instabot example

    Workflow:
        Follow user's following by username by contained keywords.
"""

import argparse
import os
import sys

sys.path.append(os.path.join(sys.path[0], "../"))
from instabot import Bot  # noqa: E402

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("-u", type=str, help="username")
parser.add_argument("-p", type=str, help="password")
parser.add_argument("-proxy", type=str, help="proxy")
parser.add_argument("users", type=str, nargs="+", help="users")
#parser.add_argument("-k", type=str, help="keyword")
args = parser.parse_args()

bot = Bot()
bot.login(username=args.u, password=args.p, proxy=args.proxy)

key = input("Input contained keywords : ")

for username in args.users:
    #bot.follow_following(username)
    bot.follow_contain_str_following(username,key)
