from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping

### Setup Flask
app = Flask(__name__)

### Connection to Mongo using PyMongo
## Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# app.config["MONGO_URI"] tells Python that our app will connect to Mongo using a URI, a uniform resource identifier similar to a URL.
#"mongodb://localhost:27017/mars_app" is the URI we'll be using to connect our app to Mongo. This URI is saying that the app can reach Mongo through our localhost server, using port 27017, using a database named "mars_app".

### Setup App Routes
# Flask routes bind URLs to functions. For example, the URL "ourpage.com/" brings us to the homepage of our web app. The URL "ourpage.com/scrape" will activate our scraping code.
# These routes can be embedded into our web app and accessed via links or buttons.

## Setup Homepage Route
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# mars = mongo.db.mars.find_one() uses PyMongo to find the "mars" collection in our database, which we will create when we convert our Jupyter scraping code to Python Script. 
# We will also assign that path to the mars variable for use later.
# the mars=mars tells Python to use the "mars" collection in MongoDB.

## Setup Scraping Route
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return "Scraping Successful!"

# mars = mongo.db.mars directs to our Mongo Database
# mars_data = scraping.scrape_all() - create a variable to hold the scraped data - the scrape_all function being used on the scraping.py file 
# .update() method has the syntax: .update(query_parameter, data, options) 
# In the above we're inserting data, so first we'll need to add an empty JSON object with {} in place of the query_parameter. 
# Next, we'll use the data we have stored in mars_data. Finally, the option we'll include is upsert=True. This indicates to Mongo to create a new document if one doesn't already exist, and new data will always be saved (even if we haven't already created a document for it).

### Tell Flask to run
if __name__ == "__main__":
   app.run()