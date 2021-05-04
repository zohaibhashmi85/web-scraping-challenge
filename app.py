from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Find one record of data from the mongo database
    mars_info = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars_info=mars_info)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
       
    mars_info_collection = mongo.db.mars_info

    # Run the scrape function
    results_dict = scrape_mars.scrape()
    
    # Update the Mongo database using update and upsert=True
    mars_info_collection.update({}, results_dict, upsert=True)
   
   
    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)