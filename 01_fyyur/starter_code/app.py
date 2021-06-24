#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
from forms import VenueForm,ArtistForm,ShowForm
import dateutil.parser
from datetime import datetime
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from wtforms import validators
from wtforms.validators import *
from flask_migrate import Migrate
from sqlalchemy.sql import text
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Shows(db.Model):
  __tablename__= 'shows'
  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer,nullable=False)
  venue_id = db.Column(db.Integer,nullable=False)
  start_date = db.Column(db.DateTime,nullable=False)
  def __init__(self,artist_id,venue_id,start_date):
    self.artist_id=artist_id
    self.venue_id=venue_id
    self.start_date=start_date

class Venue(db.Model):
    __tablename__ = 'venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(200))
    website_link = db.Column(db.String(200))
    looking_for_talent = db.Column(db.Boolean,default=False)
    seeking_description = db.Column(db.String(200))


    def __init__(self,name,city,state,address,phone,genres,image_link,facebook_link,website_link,looking_for_talent,seeking_description):
      self.name = name
      self.city = city
      self.state = state
      self.address = address
      self.phone = phone
      self.genres = genres
      self.image_link = image_link
      self.facebook_link = facebook_link
      self.website_link = website_link
      self.looking_for_talent = looking_for_talent
      self.seeking_description = seeking_description



    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(200))
    looking_for_venues = db.Column(db.Boolean,default=False)
    seeking_description = db.Column(db.String(200))

    

    def __init__(self,name,city,state,phone,genres,image_link,facebook_link,website_link,looking_for_venues,seeking_description):
      self.name = name
      self.city = city
      self.state = state
      self.phone = phone
      self.genres = genres
      self.image_link = image_link
      self.facebook_link = facebook_link
      self.website_link = website_link
      self.looking_for_venues = looking_for_venues
      self.seeking_description = seeking_description


    # TODO: implement any missing fields, as a database migration using Flask-Migrate



#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

# Time= now
now = datetime.now()
datetime_To_string = now.strftime("%Y-%m-%d %H:%M:%S")
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  querylist_oftuples = [list(elem) for elem in db.session.query(Venue.id,Venue.name).all()]
  data1 = "["
  for item in querylist_oftuples:
    if item and len(data1)>2:
        data1+=","
    data1 += '{\n\t"id":%s,\n\t"name":"%s"\n}'% (item[0],item[1])
  data1+="]"
    
  artistdata = json.loads(data1)
  data=[{
    "city": "San Francisco",
    "state": "CA",
    "venues": [{
      "id": 1,
      "name": "The Musical Hop",
      "num_upcoming_shows": 0,
    }, {
      "id": 3,
      "name": "Park Square Live Music & Coffee",
      "num_upcoming_shows": 1,
    }]
  }, {
    "city": "New York",
    "state": "NY",
    "venues": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }]
  return render_template('pages/venues.html', venues=artistdata)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  searchterm = request.form.get('search_term','')
  statement = "SELECT venue.id,venue.name FROM venue WHERE UPPER(venue.name) LIKE UPPER('%{0}%');".format(searchterm)
  countStatement = "select count(venue.id) from venue where UPPER(venue.name) LIKE UPPER('%{0}%')".format(searchterm)
  searchQuery = db.engine.execute(text(statement)).all()
  countQuery = db.engine.execute(text(countStatement)).first()[0]
  datatext = ''
  response = '{'
  response +='\n\t"count":%s,\n\t"data":['%(countQuery)
  for searches in searchQuery:
    if len(datatext)>2:
      datatext+=','
    datatext +='{\n\t"id":%s,\n\t"name":"%s",\n\t"num_upcoming_shows":%s}'%(searches[0],searches[1],get_upcoming_shows(searches[0],'venue','countvenue'))
  response+= datatext+']\n}'
  # response={
  #   "count": 0,
  #   "data": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  print(response)
  response_final = json.loads(response)
  
  return render_template('pages/search_venues.html', results=response_final, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  

  querylist_oftuples = [list(elem) for elem in db.session.query(Venue.id,Venue.name,Venue.genres,Venue.address,Venue.city,Venue.state,Venue.phone,Venue.website_link,Venue.facebook_link,Venue.looking_for_talent,Venue.seeking_description,Venue.image_link).all()]
  datax = "["
  for item in querylist_oftuples:
    if item and len(datax)>2:
        datax+=","
    datax += '{\n\t"id":%s,\n\t"name":"%s",\n\t"genres":['% (item[0],item[1])
    # print(item[2].split(','))
    for items in item[2].split(','):
      datax+='"%s",'% items
    datax = datax.rstrip(datax[-1])
    
    datax += '],\n\t"address":"%s",\n\t"city":"%s",\n\t"state":"%s",\n\t"phone":"%s",\n\t"website":"%s",\n\t"facebook_link":"%s",\n\t"seeking_talent":%s,\n\t"seeking_description":"%s",\n\t"image_link":"%s",\n\t"past_shows":['%(item[3],item[4],item[5],item[6],item[7],item[8],str(item[9]).lower(),item[10],item[11])
    pastshow = ''
    for something in get_past_shows(item[0],'venue','listvenue'):
        if something:
          if len(pastshow)>2:
            pastshow +=','
          pastshow += '{\n\t"artist_id":%s,\n\t"artist_name":"%s",\n\t"artist_image_link":"%s",\n\t"start_time":"%s"\n}'%(something[0],something[1],something[2],something[3])
    datax+=pastshow+'],\n\t"upcoming_shows":['
    upcomingshow = ''
    for something in get_upcoming_shows(item[0],'venue','listvenue'):
        if something:
          if len(upcomingshow)>2:
            upcomingshow +=','
          upcomingshow += '{\n\t"artist_id":%s,\n\t"artist_name":"%s",\n\t"artist_image_link":"%s",\n\t"start_time":"%s"\n}'%(something[0],something[1],something[2],something[3])
    datax+=upcomingshow+'],\n\t"past_shows_count":%s,\n\t"upcoming_shows_count":%s\n}'%(get_past_shows(item[0],'venue','countvenue'),get_upcoming_shows(item[0],'venue','countvenue'))
    
  datax+="]"
  print(datax)
  print(datax[226])
  
  print("----------------------------------------------------------------")
  artistdata = json.loads(datax)
  print(artistdata)

  data = list(filter(lambda d: d['id'] == venue_id,artistdata ))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  # form = request.form['form']
  # if form.is_submitted():
  form = VenueForm()
  if form.validate_on_submit():
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    address = request.form['address']
    phone = request.form['phone']
    genres = ','.join(form.genres.data)
    # for genre in request.form['genres']:
    #   genres+= genre + ','
    facebook_link = request.form['facebook_link']
    image_link = request.form['image_link']
    website_link = request.form['website_link']
    # looking_for_talent = False
    # if(request.form['seeking_talent'] == 'y'):
    #   looking_for_talent = True
    # else:
    #   looking_for_talent = False
    # looking_for_talent = request.form['seeking_talent']
    seeking_talent = True if 'seeking_talent' in request.form else False
    seeking_description = request.form['seeking_description']
    print(form.genres.data)
    print(request.form.getlist('genres'))
    venue = Venue(name,city,state,address,phone,genres,image_link,facebook_link,website_link,seeking_talent,seeking_description)

    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] +' was successfully listed!')
    db.session.close()
    return render_template('pages/home.html')
  else:
    flash('Venue ' + request.form['name']+' was NOT successfully listed!')
    return render_template('forms/new_venue.html',form = form)
  ############### else:
    # flash('Venue ' + request.form['name'] + ' wasnt successfully listed :(((((')
  # on successful db insert, flash success
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    #return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  # data=[{
  #   "id": 4,
  #   "name": "Guns N Petals",
  # }, {
  #   "id": 5,
  #   "name": "Matt Quevedo",
  # }, {
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  # }]
  # list(filter(None, db.session.query(Artist.name).all()))
  # db.session.query(Artist.name).all()
  
  querylist_oftuples = [list(elem) for elem in db.session.query(Artist.id,Artist.name).all()]
  data = "["
  for item in querylist_oftuples:
    if item and len(data)>2:
        data+=","
    data += '{\n\t"id":%s,\n\t"name":"%s"\n}'% (item[0],item[1])
  data+="]"
  artistdata = json.loads(data)
  # print(artistdata)
  # print(querylist_oftuples)
  # id = 4
  # statment = 'select * from shows where artist_id = %s and start_date < now();'%id
  # start_time_query = db.engine.execute(text(statment)).all()
  new_query = get_past_shows(1,'artist','listartist')
  if new_query:
    for row in new_query:
      print(row)

  return render_template('pages/artists.html', artists=artistdata)
################################################################
# Methods to get past and upcoming shows
################################################################
# past shows
def get_past_shows(*args):
  if args[2]:
    if args[2] == 'listvenue':
      statement = 'select artist.id, artist.name, artist.image_link, start_date \
                  from artist,venue,shows \
                  where venue.id = venue_id and\
                  artist_id = artist.id and\
                  venue_id = %s and\
                  start_date < now();'%args[0]
      pastshows_query = db.engine.execute(text(statement)).all()
      return pastshows_query
    elif args[2] == 'listartist':
      statement = 'select venue.id, venue.name, venue.image_link, start_date \
                  from artist,venue,shows \
                  where venue.id = venue_id and\
                  artist_id = artist.id and\
                  artist_id = %s and\
                  start_date < now();'%args[0]
      pastshows_query = db.engine.execute(text(statement)).all()
      return pastshows_query
    elif args[2] == 'countvenue':
      statment = 'select count(*) from shows where venue_id = %s and start_date < now();'%args[0]
      pastshows_query = db.engine.execute(text(statment)).first()[0]
      return pastshows_query
    elif args[2] == 'countartist':
      statment = 'select count(*) from shows where artist_id = %s and start_date < now();'%args[0]
      pastshows_query = db.engine.execute(text(statment)).first()[0]
      return pastshows_query
  else:
    if args[1] == 'artist':
      statment = 'select * from shows where artist_id = %s and start_date < now();'%args[0]
      pastshows_query = db.engine.execute(text(statment)).all()
      return pastshows_query
    elif args[1] == 'venue':
      statment = 'select * from shows where venue_id = %s and start_date < now();'%args[0]
      pastshows_query = db.engine.execute(text(statment)).all()
      return pastshows_query
# upcoming shows
def get_upcoming_shows(*args):
  if args[2] == 'listvenue':
    statement = 'select artist.id, artist.name, artist.image_link, start_date \
                from artist,venue,shows \
                where venue.id = venue_id and\
                artist_id = artist.id and\
                venue_id = %s and\
                start_date > now();'%args[0]
    pastshows_query = db.engine.execute(text(statement)).all()
    return pastshows_query
  if args[2] == 'listartist':
    statement = 'select venue.id, venue.name, venue.image_link, start_date \
                from artist,venue,shows \
                where venue.id = venue_id and\
                artist_id = artist.id and\
                artist_id = %s and\
                start_date > now();'%args[0]
    pastshows_query = db.engine.execute(text(statement)).all()
    return pastshows_query
  if args[2] == 'countvenue':
    statment = 'select count(*) from shows where venue_id = %s and start_date > now();'%args[0]
    pastshows_query = db.engine.execute(text(statment)).first()[0]
    return pastshows_query
  if args[2] == 'countartist':
    statment = 'select count(*) from shows where artist_id = %s and start_date > now();'%args[0]
    pastshows_query = db.engine.execute(text(statment)).first()[0]
    return pastshows_query
  if args[1] == 'artist':
    statment = 'select * from shows where artist_id = %s and start_date > now();'%args[0]
    pastshows_query = db.engine.execute(text(statment)).all()
    return pastshows_query
  elif args[1] == 'venue':
    statment = 'select * from shows where venue_id = %s and start_date > now();'%args[0]
    pastshows_query = db.engine.execute(text(statment)).all()
    return pastshows_query

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  searchterm = request.form.get('search_term','')
  statement = "SELECT artist.id,artist.name FROM artist WHERE UPPER(artist.name) LIKE UPPER('%{0}%');".format(searchterm)
  countStatement = "select count(artist.id) from artist where UPPER(artist.name) LIKE UPPER('%{0}%')".format(searchterm)
  searchQuery = db.engine.execute(text(statement)).all()
  countQuery = db.engine.execute(text(countStatement)).first()[0]
  datatext = ''
  response = '{'
  response +='\n\t"count":%s,\n\t"data":['%(countQuery)
  for searches in searchQuery:
    if len(datatext)>2:
      datatext+=','
    datatext +='{\n\t"id":%s,\n\t"name":"%s",\n\t"num_upcoming_shows":%s}'%(searches[0],searches[1],get_upcoming_shows(searches[0],'artist','countartist'))
  response+= datatext+']\n}'
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 4,
  #     "name": "Guns N Petals",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  response_finale = json.loads(response)
  return render_template('pages/search_artists.html', results=response_finale, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  data1={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "past_shows": [{
      "venue_id": 1,
      "venue_name": "The Musical Hop",
      "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
      "start_time": "2019-05-24 21:30:00"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data2={
    "id": 5,
    "name": "Matt Quevedo",
    "genres": ["Jazz"],
    "city": "New York",
    "state": "NY",
    "phone": "300-400-5000",
    "facebook_link": "https://www.facebook.com/mattquevedo923251523",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "past_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data3={
    "id": 6,
    "name": "The Wild Sax Band",
    "genres": ["Jazz", "Classical"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "432-325-5432",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "past_shows": [],
    "upcoming_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 0,
    "upcoming_shows_count": 3,
  }
  # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]

  querylist_oftuples = [list(elem) for elem in db.session.query(Artist.id,Artist.name,Artist.genres,Artist.city,Artist.state,Artist.phone,Artist.website_link,Artist.facebook_link,Artist.looking_for_venues,Artist.seeking_description,Artist.image_link).all()]
  datax = "["
  for item in querylist_oftuples:
    if item and len(datax)>2:
        datax+=","
    datax += '{\n\t"id":%s,\n\t"name":"%s",\n\t"genres":['% (item[0],item[1])
    # print(item[2].split(','))
    for items in item[2].split(','):
      datax+='"%s",'% items
    datax = datax.rstrip(datax[-1])
    
    datax += '],\n\t"city":"%s",\n\t"state":"%s",\n\t"phone":"%s",\n\t"website":"%s",\n\t"facebook_link":"%s",\n\t"seeking_venue":%s,\n\t"seeking_description":"%s",\n\t"image_link":"%s",\n\t"past_shows":['%(item[3],item[4],item[5],item[6],item[7],str(item[8]).lower(),item[9],item[10])
    pastshow = ''
    for something in get_past_shows(item[0],'artist','listartist'):
        if something:
          if len(pastshow)>2:
            pastshow +=','
          pastshow += '{\n\t"venue_id":%s,\n\t"venue_name":"%s",\n\t"venue_image_link":"%s",\n\t"start_time":"%s"\n}'%(something[0],something[1],something[2],something[3])
    datax+=pastshow+'],\n\t"upcoming_shows":['
    upcomingshow = ''
    for something in get_upcoming_shows(item[0],'artist','listartist'):
        if something:
          if len(upcomingshow)>2:
            upcomingshow +=','
          upcomingshow += '{\n\t"venue_id":%s,\n\t"venue_name":"%s",\n\t"venue_image_link":"%s",\n\t"start_time":"%s"\n}'%(something[0],something[1],something[2],something[3])
    datax+=upcomingshow+'],\n\t"past_shows_count":%s,\n\t"upcoming_shows_count":%s\n}'%(get_past_shows(item[0],'artist','countartist'),get_upcoming_shows(item[0],'artist','countartist'))
    
  datax+="]"
  print(datax)
  print(datax[226])
  
  print("----------------------------------------------------------------")
  artistdata = json.loads(datax)
  print(artistdata)

  data = list(filter(lambda d: d['id'] == artist_id,artistdata ))[0]


  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue3={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  genres_list = list(filter(None, db.session.query(Venue.genres).filter_by(id=venue_id).first()))

  venue = {
    'id':venue_id,
    'name':db.session.query(Venue.name).filter_by(id=venue_id).first()[0],
    'genres':genres_list,
    'address':db.session.query(Venue.address).filter_by(id=venue_id).first()[0],
    'city':db.session.query(Venue.city).filter_by(id=venue_id).first()[0],
    'state':db.session.query(Venue.state).filter_by(id=venue_id).first()[0],
    'phone':db.session.query(Venue.phone).filter_by(id=venue_id).first()[0],
    'website':db.session.query(Venue.website_link).filter_by(id=venue_id).first()[0],
    'facebook_link':db.session.query(Venue.facebook_link).filter_by(id=venue_id).first()[0],
    'seeking_talent':db.session.query(Venue.looking_for_talent).filter_by(id=venue_id).first()[0],
    'seeking_description':db.session.query(Venue.seeking_description).filter_by(id=venue_id).first()[0],
    'image_link':db.session.query(Venue.image_link).filter_by(id=venue_id).first()[0]
  }
  print(venue)
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form,venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  form = ArtistForm()
  if form.validate_on_submit():
    name= request.form['name']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    genres = ','.join(form.genres.data)
    facebook_link = request.form['facebook_link']
    image_link = request.form['image_link']
    website_link = request.form['website_link']
    seeking_venue = True if 'seeking_venue' in request.form else False
    seeking_description = request.form['seeking_description']
    artist = Artist(name,city,state,phone,genres,image_link,facebook_link,website_link,seeking_venue,seeking_description)
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    db.session.close()
    return render_template('pages/home.html')
  else:
    flash('Artist '+ request.form['name'] + ' was NOT seccessfully listed')
  # on successful db insert, flash success
  # flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('forms/new_artist.html',form=form)


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  # querylist_oftuples = [list(elem) for elem in db.session.query(Venue.id,Artist.name,Artist.genres,Artist.city,Artist.state,Artist.phone,Artist.website_link,Artist.facebook_link,Artist.looking_for_venues,Artist.seeking_description,Artist.image_link).all()]
  
  # for item in querylist_oftuples:
  #   if item and len(datax)>2:
  #       datax+=","
  #   datax += '{\n\t"id":%s,\n\t"name":"%s",\n\t"genres":['% (item[0],item[1])
  #   # print(item[2].split(','))
  #   for items in item[2].split(','):
  #     datax+='"%s",'% items
  #   datax = datax.rstrip(datax[-1])
  newquery = db.engine.execute(text('select venue.id, venue.name, artist.id, artist.name, artist.image_link,start_date \
                                    from venue,artist,shows\
                                    where venue.id = venue_id and artist.id = artist_id;')).all()
  datax = '['
  for query in newquery:
    if query and len(datax) > 2:
      datax +=","
    datax +='{\n\t"venue_id":%s,\n\t"venue_name":"%s",\n\t"artist_id":%s,\n\t"artist_name":"%s",\n\t"artist_image_link":"%s",\n\t"start_time":"%s"},'%(query[0],query[1],query[2],query[3],query[4],query[5])
    datax = datax.rstrip(datax[-1])
  datax +=']'
  print(datax)
  
  print("----------------------------------------------------------------")
  artistdata = json.loads(datax)
  print(artistdata)
  data=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
  }]
  return render_template('pages/shows.html', shows=artistdata)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  form = ShowForm()
  if form.validate_on_submit():
    artist_id = request.form['artist_id']
    venue_id = request.form['venue_id']
    start_date = request.form['start_time']
    show = Shows(artist_id,venue_id,start_date)
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
    db.session.close()
    return render_template('pages/home.html')
  else:
    flash('An error occurred. Show could not be listed.')
  # on successful db insert, flash success
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('forms/new_show.html',form = form)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug=True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
