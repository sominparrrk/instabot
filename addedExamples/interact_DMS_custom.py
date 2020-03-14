# -*- coding: utf-8 -*-
"""
    instabot example
    Workflow:
        read and reply your DM easily.
"""

import argparse
import os
import sys

sys.path.append(os.path.join(sys.path[0], "../"))
from instabot import Bot  # noqa: E402

try:
    input = raw_input
except NameError:
    pass

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("-u", type=str, help="username")
parser.add_argument("-p", type=str, help="password")
parser.add_argument("-proxy", type=str, help="proxy")
args = parser.parse_args()


def choice(message):
    get_choice = input(message)
    if get_choice == "y":
        return True
    elif get_choice == "n":
        return False
    else:
        print("Invalid Input")
        return choice(message)


bot = Bot()
bot.login(username=args.u, password=args.p, proxy=args.proxy)


#if bot.api.get_inbox_v2():
if bot.api.get_inbox_v2():
    data = bot.last_json["inbox"]["threads"]
   
    #DM활성화 유저 리스트 추리기.
    list = []
    print("-------------------------------------------------------------------------------------------")
    for item in data:
        #DM 선택하기
        list.append(item)
        user = item["users"]
        print("ID : " + user[0]["username"] + " | " + "full_name : " + user[0]["full_name"])
        #last_DM : " + item["inviter"]["username"] + " : " + item["last_permanent_item"]["text"] if item["last_permanent_item"]["item_type"] == "text" else "Not Text")
        bot.console_print(item["inviter"]["username"], "lightgreen")
        print(item["last_permanent_item"]["text"] if item["last_permanent_item"]["item_type"] == "text" else "Not Text")
        print("---------------------------------------------------------------------------------------")
        
    while choice("Do you want to write DM?(y/n):"):
        try :
            id = input("who are you sending to?(write ID):")
            raise_n = 0
            for item in list:
                if item["users"][0]["username"] == id:
                    user_id = str(item["inviter"]["pk"])
                    last_item = item["last_permanent_item"]
                    item_type = last_item["item_type"]
                    while True:
                        text = input("write your message(if not want chat,input 'quit'): ")
                        if text=='quit':
                            raise_n = 1
                            break
                        if choice("send message?(y/n)"):
                            bot.send_message(
                                text, user_id, thread_id=item["thread_id"]
                            )
                else:
                    continue
            if raise_n == 0:
                raise Exception("Not exist ID")
        except Exception as e:
            print(e.args)
