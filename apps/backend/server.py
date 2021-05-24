import twint

from flask import Flask, request
from flask_cors import CORS, cross_origin
import os
import requests
import shutil
import json
from multiprocessing import Process
import random

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app, resources={r"/*": {"origins": "*"}})

proxyuser = os.environ['PROXY_USER']
proxypass = os.environ['PROXY_PASS']
baseurl = os.environ['BASE_URL']+"/"

imagefolder = "static/images/"
datafolder = "static/data/"

scraping = []


@app.route("/")
@cross_origin(origin='*')
def index():
    return "Hello World!"


@app.route('/profile/<username>', methods=['GET'])
@cross_origin(origin='*')
def getUserProfile(username):
    return {
        "username": str(username)
    }


@app.route('/profile/<username>/Posts', methods=['GET'])
@cross_origin(origin='*')
def getUserPosts(username):
    firstscrape = False
    start = request.args.get('start')
    end = request.args.get('end')
    if start == None:
        start = 0
    else:
        start = int(start)

    if os.path.exists(datafolder+username.lower()+".json"):
        with open(datafolder+username.lower()+".json", 'rb') as f:
            response = json.load(f)
            print("Accessing from cache")

            if start == 0:  # if its the first few tweets, check and update
                p = Process(target=checkAndUpdate, args=(
                    username.lower(), response,))
                p.start()
    else:
        p = Process(target=initialBackgroundScrape, args=(username.lower(),))
        p.start()

        response = scrape(username.lower(), limit=10)
        print("Got tweets!")

        firstscrape = True

        if not os.path.exists(datafolder+username.lower()+".json"):
            with open(datafolder+username.lower()+".json", 'w') as outfile:
                json.dump(response, outfile)

    tweetcount = len(response['tweets'])

    if end == None:
        end = len(response['tweets'])
    else:
        end = int(end)

    if start > end:
        start = end

    if end > len(response['tweets']):
        end = len(response['tweets'])

    response['tweets'] = response['tweets'][start:end]

    if (start > tweetcount) or (end >= tweetcount):
        if firstscrape:
            response = {"tweets": [{"tweet": "Still downloading content"}]}
        else:
            response['tweets'] = []

    print("Sending response!")

    return response


def initialBackgroundScrape(username):
    if username not in scraping:  # prevent double scrape
        scraping.append(username)
        response = scrape(username)
        with open(datafolder+username.lower()+".json", 'w') as outfile:
            json.dump(response, outfile)
            print("Saved "+datafolder+username.lower()+".json")
            scraping.remove(username)


def checkAndUpdate(username, response):
    # Check if there's an update to feed
    latestPost = scrape(username.lower(), limit=1)

    if latestPost['tweets'][0] not in response['tweets']:
        print("Found new tweet!")
        p = Process(target=initialBackgroundScrape,
                    args=(username.lower(),))
        p.start()
    else:
        print("Tweets are updated!")


def downloadAndSavePhoto(photo):
    print("Downloading " + photo)
    url = photo.split("/")[-1]

    if not os.path.exists(imagefolder+url):
        while True:
            try:
                r = requests.get(photo, stream=True, proxies=getProxy())
                # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                # Open a local file with wb ( write binary ) permission.
                r.raw.decode_content = True

                with open(imagefolder+url, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
                    print("Saved " + imagefolder+url)
                break
            except Exception as e:
                print(e, 'retrying')
                continue

    else:
        print("Image already exists!")


def scrape(username, limit=None):

    if not os.path.exists(imagefolder):
        os.makedirs(imagefolder)
    if not os.path.exists(datafolder):
        os.makedirs(datafolder)

    # Configure
    c = twint.Config()
    c.Username = username
    c.Proxy_host = getProxy()
    c.Proxy_port = 6060
    c.Proxy_type = "http"
    c.Proxy_Username = proxyuser
    c.Proxy_Password = proxypass
    c.Media = True
    c.Pandas = True
    c.Hide_output = True
    c.Limit = limit

    # Run
    print("Scraping from " + username + "'s twitter...")

    twint.run.Search(c)

    print("Scraped!")

    df = twint.storage.panda.Tweets_df

    username = df["username"][0]
    # userid = df["user_id"][0]

    tweets = []

    for index, row in df.iterrows():
        # photos = []
        # for photo in row["photos"]:

        #     url = photo.split("/")[-1]

        #     if index <= 5:
        #         p = Process(target=downloadAndSavePhoto, args=(url,))
        #         p.start()

        #     photos.append(baseurl+imagefolder+url)

        # tweets.append({"id": str(row["id"]), "created_at": str(
        #     row["created_at"]), "tweet": row["tweet"], "photos": photos})

        if row["video"] == 0:
            embed = requests.get(
                f"https://publish.twitter.com/oembed?url=https://twitter.com/{username}/status/{row['id']}")
            embed = embed.json()["html"]
        else:
            embed = ""

        tweets.append({"id": str(row["id"]), "created_at": str(
            row["created_at"]), "tweet": row["tweet"], "photos": row["photos"], "video": embed})

    print("Converted dataframe!")
    return {
        "username": str(username),
        "tweets": tweets
    }


def getProxy():
    proxyList = [
        "hk.torguard.com",
        "id.torguard.com",
        "jp.torguard.com",
        "nz.torguard.com",
        "sg.torguard.com",
        "sg2.torguard.com",
        "tw.torguard.com",
        "au.torguard.com",
        "au2.torguard.com",
        "th.torguard.com",
        "br.torguard.com",
        "br2.torguard.com",
        "ca.torguard.com",
        "us-lv.torguard.com",
        "ch.torguard.com",
        "cavan.torguard.com",
        "mx.torguard.com",
        "us-atl.torguard.com",
        "us-la.torguard.com",
        "us-fl.torguard.com",
        "us-dal.torguard.com",
        "us-nj.torguard.com",
        "us-ny.torguard.com",
        "us-chi.torguard.com",
        "us-lv.torguard.com",
        "us-sf.torguard.com",
        "us-sa.torguard.com",
        "us-slc.torguard.com",
        "aus.torguard.com",
        "bg.torguard.com",
        "bul.torguard.com",
        "cz.torguard.com",
        "dn.torguard.com",
        "fn.torguard.com",
        "fr.torguard.com",
        "ger.torguard.com",
        "gre.torguard.com",
        "hg.torguard.com",
        "ice.torguard.com",
        "ire.torguard.com",
        "it.torguard.com",
        "lv.torguard.com",
        "md.torguard.com",
        "nl.torguard.com",
        "no.torguard.com",
        "pl.torguard.com",
        "pg.torguard.com",
        "ro.torguard.com",
        "ru.torguard.com",
        "slk.torguard.com",
        "sp.torguard.com",
        "swe.torguard.com",
        "swiss.torguard.com",
        "tk.torguard.com",
        "ukr.torguard.com",
        "uk.torguard.com",
        "in.torguard.com",
        "isr-loc1.torguard.com",
        "sa.torguard.com",
        "uae.torguard.com",
    ]

    proxy_index = random.randint(0, len(proxyList) - 1)
    proxy = proxyList[proxy_index]

    return proxy
