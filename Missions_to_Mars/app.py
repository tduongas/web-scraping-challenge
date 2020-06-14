from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Retrieve collections
    latestMarsNews = mongo.db.latestMarsNews.find_one()
    featuredImage = mongo.db.featuredImage.find_one()
    weather = mongo.db.marsWeather.find_one()
    marsFacts = mongo.db.marsFacts.find_one()
    marsHemispheres = mongo.db.marsHemispheres.find_one()

    # Return template and data
    return render_template("index.html", 
    latestMarsNews=latestMarsNews, 
    featuredImage=featuredImage,
    weather = weather,
    marsFacts = marsFacts,
    marsHemispheres = marsHemispheres)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    # # Scrape for latest Mars news and store in mongo database
    # latest_mars_news = scrape_mars.latest_mars_news()
    # mongo.db.latestMarsNews.update({}, latest_mars_news, upsert=True)

    # # Scrape latest featured image and store in mongo database
    # featured_image = scrape_mars.featured_image()
    # mongo.db.featuredImage.update({}, featured_image, upsert=True)

    # # Scrape latest Mars weather and store in mongo database
    # weather = scrape_mars.current_mars_weather()
    # mongo.db.marsWeather.update({}, weather, upsert=True)

    # # Scrape Mars facts and store in mongo database
    # mars_facts = scrape_mars.mars_facts()
    # mongo.db.marsFacts.update({}, mars_facts, upsert=True)

    # Scrape Mars hemispheres and store in mongo database
    mars_hemispheres = scrape_mars.mars_hemispheres()
    
    # mongo.db.marsHemispheres.update({}, value, upsert=True)
    mongo.db.marsHemispheres.update_many({}, mars_hemispheres, upsert=True)
    
        
    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
