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

if not os.path.exists(imagefolder):
    os.makedirs(imagefolder)
if not os.path.exists(datafolder):
    os.makedirs(datafolder)


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
    if os.path.exists(datafolder+username.lower()+".json"):
        with open(datafolder+username.lower()+".json", 'rb') as f:
            response = json.load(f)

            print("Accessing from cache")

    else:
        p = Process(target=initialBackgroundScrape, args=(username.lower(),))
        p.start()

        response = scrape(username.lower(), full=False)
        print("Got tweets!")

        if not os.path.exists(datafolder+username.lower()+".json"):
            with open(datafolder+username.lower()+".json", 'w') as outfile:
                json.dump(response, outfile)

    start = request.args.get('start')
    end = request.args.get('end')
    tweetcount = len(response['tweets'])

    if start == None:
        start = 0
    else:
        start = int(start)

    if end == None:
        end = len(response['tweets'])
    else:
        end = int(end)

    if start > end:
        start = end

    if end > len(response['tweets']):
        end = len(response['tweets'])

    originalresponse = response

    response['tweets'] = response['tweets'][start:end]

    extraend = end+10
    if extraend > len(response['tweets']):
        extraend = len(response['tweets'])

    # print('1', originalresponse['tweets'][start:end])
    # print('2', originalresponse['tweets'][start:extraend])

    # for tweet in originalresponse['tweets'][start:extraend]:
    #     print('tweet', tweet)
    #     for photo in tweet['photos']:
    #         print('photo', photo)
    #         url = photo.split("/")[-1]
    #         url = 'https://pbs.twimg.com/media/'+url
    #         p = Process(target=downloadAndSavePhoto, args=(url,))
    #         p.start()

    if start > tweetcount:
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


def scrape(username, full=True):
    # Configure
    c = twint.Config()
    c.Username = username
    c.Proxy_host = "jp.torguard.com"
    c.Proxy_port = 6060
    c.Proxy_type = "http"
    c.Proxy_Username = proxyuser
    c.Proxy_Password = proxypass
    c.Images = True
    c.Pandas = True
    c.Hide_output = True

    if (not full):
        c.Limit = 5

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
        tweets.append({"id": str(row["id"]), "created_at": str(
            row["created_at"]), "tweet": row["tweet"], "photos": row["photos"]})

    print("Converted dataframe!")
    return {
        "username": str(username),
        "tweets": tweets
    }


def getProxy():
    proxyList = [
        "http://"+proxyuser+":"+proxypass+"@hk.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@id.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@jp.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@nz.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@sg.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@sg2.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@tw.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@au.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@au2.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@th.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@br.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@br2.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@ca.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@us-lv.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@ch.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@cavan.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@mx.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@us-atl.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@us-la.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@us-fl.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@us-dal.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@us-nj.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@us-ny.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@us-chi.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@us-lv.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@us-sf.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@us-sa.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@us-slc.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@aus.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@bg.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@bul.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@cz.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@dn.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@fn.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@fr.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@ger.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@gre.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@hg.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@ice.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@ire.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@it.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@lv.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@md.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@nl.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@no.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@pl.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@pg.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@ro.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@ru.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@slk.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@sp.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@swe.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@swiss.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@tk.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@ukr.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@uk.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@in.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@isr-loc1.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@sa.torguard.com:6060",
        "http://"+proxyuser+":"+proxypass+"@uae.torguard.com:6060",
    ]

    proxy_index = random.randint(0, len(proxyList) - 1)
    proxy = {"https": proxyList[proxy_index]}

    return proxy
