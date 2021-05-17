import twint

from flask import Flask
from flask_cors import CORS, cross_origin
import os
import requests
import shutil
import json

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app, resources={r"/*": {"origins": "*"}})

proxyuser = os.environ['PROXY_USER']
proxypass = os.environ['PROXY_PASS']
baseurl = os.environ['BASE_URL']+"/"

imagefolder = "static/images/"
datafolder = "static/data/"

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
    if not os.path.exists(datafolder+username):
        with open(datafolder+username, 'wb') as f:
            tweets = json.load(f)

        return {
            "username": str(username),
            "tweets": tweets
        }

    else:
        response = initialScrape(username)

        with open(datafolder+username, 'w') as outfile:
            json.dump(response, outfile)

        return response


def initialScrape(username):
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
    # Run
    twint.run.Search(c)

    df = twint.storage.panda.Tweets_df

    username = df["username"][0]
    # userid = df["user_id"][0]

    tweets = []

    for index, row in df.iterrows():
        photos = []
        for photo in row["photos"]:
            r = requests.get(photo, stream=True)
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            # Open a local file with wb ( write binary ) permission.
            r.raw.decode_content = True
            url = photo.split("/")[-1]

            if not os.path.exists(imagefolder+url):
                with open(imagefolder+url, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)

            photos.append(baseurl+imagefolder+url)

        tweets.append({"id": str(row["id"]), "created_at": str(
            row["created_at"]), "tweet": row["tweet"], "photos": photos})

    return {
        "username": str(username),
        "tweets": tweets
    }
