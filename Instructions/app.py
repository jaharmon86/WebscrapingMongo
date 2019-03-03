from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/test_mars"
mongo = PyMongo(app)


@app.route("/")
def homepage():
    result = mongo.db.test_collection.find_one()
    return render_template("index.html", result = result)


@app.route("/scrape")
def scrape():
    pass
    # that function returns a dicitionary
    result = scrape_mars.scrape_master()
    mongo.db.test_collection.update({}, result, upsert=True)
    return redirect("/", 302)





if __name__ == '__main__':
    app.run(debug=True, port=5544)
