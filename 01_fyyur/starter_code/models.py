from app import db 




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


