# Import Dependencies
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping

# Set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# Tells Python that our app will connect to Mongo using a URI, a uniform resource identifier similar to a URL
# This URI is saying that the app can reach Mongo through our localhost server, using port 27017, using a database named ”mars_app”
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#Set up App Routes

# Define the route for the HTML page
# This route, @app.route("/"), tells Flask what to display when we’re looking at the home page, index.html 
@app.route("/")
def index():
   # Use PyMongo to find the “mars” collection in the database, which is created when the Jupyter scraping code is converted to the Python Script. Assign that path to the mars variable for use later.  
   mars = mongo.db.mars.find_one()
   # Tell Flask to return an HTML template using an index.html file. This file will be created after the Flask routes are creared, mars=mars) tells Python to use the “mars” collection in MongoDB.
   return render_template("index.html", mars=mars)

   # Set up scraping route

   # Defines the route that Flask will be using. This route, “/scrape”, will run the function that is created beneath it.
@app.route("/scrape")
def scrape():
   # Assign a new variable that points to our Mongo database
   mars = mongo.db.mars
   # Create a new variable to hold the newly scraped data. Reference the scrape_all function in the scraping.py file exported from Jupyter Notebook
   mars_data = scraping.scrape_all()
   # Update the database (insert data): need to add an empty JSON object with {} in place of the query_parameter. U se the data stored in mars_data. Include upsert=True. This indicates to Mongo to create
   # a new document if one doesn’t already exist, and new data will always be saved (even if we haven’t already created a document for it).
   mars.update({}, mars_data, upsert=True)
   return "Scraping Successful!"

# Tell Flask to run
if __name__ == "__main__":
   app.run()