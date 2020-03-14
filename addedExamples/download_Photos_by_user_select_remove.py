"""
    instabot example

    Workflow:
        Download the specified user's medias by selecting and removing

"""
import argparse
import os
import sys
import cv2
sys.path.append(os.path.join(sys.path[0], "../"))
from instabot import Bot  # noqa: E402

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("username", type=str, help="@username")
args = parser.parse_args()

if args.username[0] != "@":  # if first character isn't "@"
    args.username = "@" + args.username

bot = Bot()
bot.login()
medias = bot.get_total_user_medias(args.username)
broken = bot.download_photos(medias,"test3")
print(len(medias))
print(medias)
photolist = os.listdir("test3")
print(photolist)
#print(len(broken))

downloaded = []
for i in range(len(medias)):
    t = args.username[1:] + "_" + medias[i]
    tjpg = t + ".jpg"
    print(t)
    if tjpg in photolist:
        downloaded.append(tjpg)
    else :
        for j in photolist:
            if t in j:
                downloaded.append(j)

print(len(downloaded))
print(downloaded)
for x in range(len(downloaded)):
    img = cv2.imread("test3\\" + downloaded[x], cv2.IMREAD_COLOR)
    cv2.imshow('image', img)
    if cv2.waitKey(0) == 27:
        cv2.destroyAllWindows()
        os.remove("test3\\" + downloaded[x])
