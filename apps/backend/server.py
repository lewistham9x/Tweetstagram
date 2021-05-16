import twint

from flask import Flask
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app, resources={r"/*": {"origins": "*"}})

proxyuser = os.environ['PROXY_USER']
proxypass = os.environ['PROXY_PASS']

print('proxyuser', proxyuser)
print('proxypass', proxypass)

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
def getUserTweets(username):
	# Configure
	c = twint.Config()
	c.Username = username
	c.Proxy_host = "jp.torguard.com"
	c.Proxy_port = 6060
	c.Proxy_type = "http"
	c.Proxy_Username = proxyuser
	c.Proxy_Password = proxypass
	c.Images=True
	c.Pandas=True
	# Run
	twint.run.Search(c)

	df = twint.storage.panda.Tweets_df

	username = df["username"][0]
	userid = df["user_id"][0]

	tweets = []
	for index, row in df.iterrows():
		tweets.append({"id": str(row["id"]), "created_at": str(row["created_at"]), "tweet": row["tweet"], "photos":row["photos"]})

	return {
		"username": str(username),
		"userid": str(userid),
		"tweets": tweets
	}
