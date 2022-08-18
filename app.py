#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from sqlalchemy import ForeignKey
from forms import *
from flask_migrate import Migrate
import sys

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_description = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    website_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    shows = db.relationship('Show', backref='Venue', lazy='dynamic')


    def __init__(self, name, genres, address, city, state, phone, website_link, facebook_link, image_link, seking_talent=False, seeking_description=""):
      self.name = name
      self.genres = genres
      self.city = city
      self.state = state
      self.address = address
      self.phone = phone
      self.image_link = image_link
      self.facebook_link = facebook_link
      self.website_link = website_link
      self.seeking_description = seeking_description

    def insert(self):
      db.session.add(self)
      db.session.commit()

    def update(self):
      db.session.commit()

    def delete(self):
      db.session.delete(self)
      db.session.commit()

    def short(self):
      return{
        'id':self.id,
        'name':self.name,
      }

    def short(self):
      print(self)
      return{
        'id':self.id,
        'name':self.name,
        'city':self.city,
        'state':self.state,
      }

    def details(self):
      return{
        'id':self.id,
        'name':self.name,
        'genres':self.genres,
        'address':self.address,
        'city':self.city,
        'phone':self.phone,
        'website_link':self.website_link,
        'facebook_link':self.facebook_link,
        'seeking_talent':self.seeking_talent,
        'seeking_description':self.seeking_description,
        'image_link':self.image_link
      }


    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120), default='')
    website_link = db.Column(db.String(120))
    shows = db.relationship('Show', backref='Artist', lazy=True)


    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    
    def __init__(self, name, genres, city, state, phone, image_link, website_link, facebook_link, seeking_venue=False, seeking_description=""):
      self.name = name
      self.genres = genres
      self.city = city
      self.state = state
      self.phone = phone
      self.website_link = website_link
      self.facebook_link = facebook_link
      self.seeking_description = seeking_description
      self.image_link = image_link


    def insert(self):
      db.session.add(self)
      db.session.commit()

    def update(self):
      db.session.commit()

    def short(self):
      return{
        'id':self.id,
        'name':self.name,
      }

    def short(self):
      print(self)
      return{
        'id':self.id,
        'name':self.name,
        'city':self.city,
        'state':self.state,
      }

    def details(self):
      return{
        'id':self.id,
        'name':self.name,
        'genres':self.genres,
        'city':self.city,
        'state':self.state,
        'phone':self.phone,
        'website_link':self.website_link,
        'facebook_link':self.facebook_link,
        'seeking_venue':self.seeking_venue,
        'seeking_description':self.seeking_description,
        'image_link':self.image_link

      }





# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
#show model

class Show(db.Model):

  __tablename__ = 'show'
  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, ForeignKey(Venue.id), nullable=False)
  artist_id = db.Column(db.Integer, ForeignKey(Artist.id), nullable=False)
  start_time = db.Column(db.String(), nullable=False)

  def __init__(self, venue_id, artist_id, start_time):
    self.venue_id = venue_id
    self.artist_id = artist_id
    self.start_time = start_time

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def detail(self):
    return{
      'venue_id':self.venue_id,
      'venue_name':self.Venue.name,
      'artist_id':self.artist_id,
      'artist_name':self.Artist.name,
      'artist_image_link':self.Artist.image_link,
      'start_time':self.start_time

    }

  def artist_details(self):
    return{
      'artist_id':self.artist_id,
      'artist_name':self.Artist.name,
      'artist_image_link':self.Artist.image_link,
      'start_time':self.start_time
    }

  def venue_details(self):
    return{
      'venue_id':self.venue_id,
      'venue_name':self.Venue.name,
      'venue_image_link':self.Venue.image_link,
      'start_time':self.start_time
    }



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
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  current_time = datetime.now().strftime('%Y-%m-%d %H:%S:%M')
  venues = Venue.query.group_by(Venue.id, Venue.state, Venue.city).all()
  venue_state_and_city = ''
  data = []

  #loop through venues to check for upcoming shows, city, states and venue information
  for venue in venues:
    #filter upcoming shows given that the show start time is greater than the current time
    print(venue)
    upcoming_shows = venue.shows.filter(Show.start_time > current_time).all()
    if venue_state_and_city == venue.city + venue.state:
      data[len(data) - 1]["venues"].append({
        "id":venue.id,
        "name":venue.name,
        "num_upcoming_shows": len(upcoming_shows) # a count of the number of shows
      })
    else:
      venue_state_and_city == venue.city + venue.state
      data.append({
        "city":venue.city,
        "state":venue.state,
        "venues": [{
          "id": venue.id,
          "name":venue.name,
          "num_upcoming_shows": len(upcoming_shows)
        }]
      })
  return render_template('pages/venues.html', areas=data)



@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  venue_query = Venue.query.filter(Venue.name.ilike('%' + request.form['search_term'] + '%'))
  venue_list = list(map(Venue.short, venue_query))
  response = {
    "count":len(venue_list),
    "data": venue_list
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  venue_query = Venue.query.get(venue_id)
  if venue_query:
    venue_details = Venue.details(venue_query)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_shows_query = Show.query.options(db.joinedload(Show.Venue)).filter(Show.venue_id == venue_id).filter(Show.start_time > current_time).all()
    new_show = list(map(Show.artist_details, new_shows_query))
    venue_details["upcoming_shows"] = new_show
    venue_details["upcoming_shows_count"] = len(new_show)
    past_shows_query = Show.query.options(db.joinedload(Show.Venue)).filter(Show.venue_id == venue_id).filter(Show.start_time <= current_time).all()
    past_shows = list(map(Show.artist_details, past_shows_query))
    venue_details["past_shows"] = past_shows
    venue_details["past_shows_count"] = len(past_shows)

    return render_template('pages/show_venue.html', venue=venue_details)
  return render_template('errors/404.html')

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

  form = VenueForm(request.form)

  try:
    venue = Venue(form.name.data, form.genres.data, form.address.data, form.city.data, form.state.data, form.phone.data, form.website_link.data, form.facebook_link.data, form.image_link.data, form.seeking_talent.data, form.seeking_description.data)
    #insert new venue records into the db

    db.session.add(venue)
    db.session.commit()
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    # TODO: on successful db insert, flash error instead.
    # e.g, flash('An error occrued. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    db.session.rollback()
    flash('Venue ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()


  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database

  # query all artists in the database
  artist_query = Artist.query.all()
  # data = list(map(Artist.short, artist_query))
  return render_template('pages/artists.html', artists=artist_query)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  artist_query = Artist.query.filter(Artist.name.ilike('%' + request.form['search_term'] + '%'))
  artist_list = list(map(Artist.short, artist_query))
  response = {
    "count":len(artist_list),
    "data": artist_list
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id

  artist_query = Artist.query.get(artist_id)
  if artist_query:
    artist_details = Artist.details(artist_query)
    #get the current system time
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_shows_query = Show.query.options(db.joinedload(Show.Artist)).filter(Show.artist_id == artist_id).filter(Show.start_time > current_time).all()
    new_shows_list = list(map(Show.venue_details, new_shows_query))
    artist_details["upcoming_shows"] = new_shows_list
    artist_details["upcoming_shows_count"] = len(new_shows_list)
    past_shows_query = Show.query.options(db.joinedload(Show.Artist)).filter(Show.artist_id == artist_id).filter(Show.start_time <= current_time).all()
    past_shows_list = list(map(Show.venue_details, past_shows_query))
    artist_details["past_shows"] = past_shows_list
    artist_details["past_shows_count"] = len(past_shows_list)
    return render_template('pages/show_artist.html', artist=artist_details)
  return render_template('errors/404.html')

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  if artist:
    form.name.data = artist.name
    form.genres.data = artist.genres
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.website_link.data = artist.website_link
    form.facebook_link.data = artist.facebook_link
    form.seeking_venue.data = artist.seeking_venue
    form.seeking_description.data = artist.seeking_description
    form.image_link.data = artist.image_link

    # TODO: populate form with fields from artist with ID <artist_id>

    return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  
  form = ArtistForm(request.form)


  try:
    edit_artist = Artist.query.get(artist_id)
    edit_artist.name = form.name.data
    edit_artist.city = form.city.data
    edit_artist.state = form.state.data
    edit_artist.phone = form.phone.data
    edit_artist.genres = form.genres.data
    edit_artist.image_link = form.image_link.data
    edit_artist.facebook_link = form.facebook_link.data
    edit_artist.website_link = form.website_link.data
    edit_artist.seeking_venue = form.seeking_venue.data
    edit_artist.seeking_description = form.seeking_description.data

    db.session.commit()
    flash('Artist ' + request.form['name'] + '  was successfully updated!')

  except:
    db.session.rollback()
    flash('An error occured. Artist ' + request.form['name'] + ' could not be changed.')

  finally:
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  if venue:
    form.name.data = venue.name
    form.genres.data = venue.genres
    form.city.data = venue.city
    form.address.data = venue.address
    form.state.data = venue.state
    form.phone.data = venue.phone
    form.website_link.data = venue.website_link
    form.facebook_link.data = venue.facebook_link
    form.seeking_talent.data = venue.seeking_talent
    form.seeking_description.data = venue.seeking_description
    form.image_link.data = venue.image_link

  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  form = VenueForm(request.form)


  try:
    edit_venue = Venue.query.get(venue_id)
    edit_venue.name = form.name.data
    edit_venue.city = form.city.data
    edit_venue.address = form.address.data
    edit_venue.state = form.state.data
    edit_venue.phone = form.phone.data
    edit_venue.genres = form.genres.data
    edit_venue.image_link = form.image_link.data
    edit_venue.facebook_link = form.facebook_link.data
    edit_venue.website_link = form.website_link.data
    edit_venue.seeking_talent = form.seeking_talent.data
    edit_venue.seeking_description = form.seeking_description.data

    db.session.commit()
    flash('Venue ' + request.form['name'] + '  was successfully updated!')

  except:
    db.session.rollback()
    flash('An error occured. Venue ' + request.form['name'] + ' could not be changed.')

  finally:
    db.session.close()
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
  form = ArtistForm(request.form)

  try:
    artist = Artist(
      name=form.name.data, 
      genres=form.genres.data, 
      city=form.city.data, 
      state=form.state.data, 
      phone=form.phone.data, 
      website_link=form.website_link.data, 
      image_link=form.image_link.data, 
      facebook_link=form.facebook_link.data, 
      seeking_venue=form.seeking_venue.data, 
      seeking_description=form.seeking_description.data
      )
    #insert new venue records into the db

    db.session.add(artist)
    db.session.commit()
    
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    flash('Artist ' + request.form['name'] + ' could not be listed. ')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')



#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.

  # a query of all shows from db using join
  show_query = Show.query.options(db.joinedload(Show.Venue), db.joinedload(Show.Artist)).all()
  data = list(map(Show.detail, show_query))
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  try:
    new_show = Show(
      venue_id=request.form['venue_id'],
      artist_id=request.form['artist_id'],
      start_time=request.form['start_time'],
    )

    db.session.add(new_show)
    db.session.commit()
    # on successful db insert, flash success
    flash('Show was successfully listed!')

  except:
    db.session.rollback()
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    flash('An error occured. Show could not be listed.')
  return render_template('pages/home.html')

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
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
