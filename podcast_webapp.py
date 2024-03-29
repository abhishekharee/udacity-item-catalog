# IMPORT BLOCK

from flask import (Flask, render_template, request, redirect, url_for, flash,
                   jsonify, make_response)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from podcast_database_setup import Base, User, Podcast, Episode

from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests

# SET UP BLOCK

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secret.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Podcasts Web App"

engine = create_engine('sqlite:///podcastepisodes.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# LOGIN BLOCK

# Create anti-forgery state token


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# Disconnect; Revoke a current user's token and reset their login_session


@app.route('/logout')
def gdisconnect():
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s'
           % login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(
            json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# USER MANAGEMENT BLOCK


def createUser(login_session):
    new_user = User(
        user_name=login_session['username'],
        user_email=login_session['email'])
    session.add(new_user)
    session.commit()
    user = session.query(
        User).filter_by(user_email=login_session['email']).one()
    return user.user_id


def getUserInfo(user_id):
    user = session.query(User).filter_by(user_id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(user_email=email).one()
        return user.user_id
    except:
        return None

# PODCAST MANAGEMENT BLOCK

# Load homepage


@app.route('/')
def show_podcasts():
    podcasts = session.query(Podcast).all()
    return render_template('index.html', podcasts=podcasts)

# Load podcasts into JSON format for API endpoint


@app.route('/JSON')
def show_podcasts_JSON():
    podcasts = session.query(Podcast).all()
    return jsonify(Podcast=[i.serialize for i in podcasts])

# Add a Podcast


@app.route('/new', methods=['GET', 'POST'])
def new_podcasts():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        if (request.form['podcast_name'] and
                request.form['podcast_description']):
            new_podcast = Podcast(podcast_name=request.form['podcast_name'],
                                  podcast_description=request.form[
                                      'podcast_description'],
                                  podcast_user_id=login_session['user_id'])
            session.add(new_podcast)
            session.commit()
            return redirect(url_for('show_podcasts'))
        else:
            flash("Yeah..... you need to populate all of these fields to "
                  "proceed... Try again please!")
            return render_template('new_podcasts.html')
    else:
        return render_template('new_podcasts.html')

# Edit Podcasts data


@app.route('/<int:podcast_id>/edit', methods=['GET', 'POST'])
def edit_podcasts(podcast_id):
    podcast_for_edit = session.query(
        Podcast).filter_by(podcast_id=podcast_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if podcast_for_edit.podcast_user_id != login_session['user_id']:
        return ("<script>function myFunction() {alert('You are not "
                "authorized to edit this Podcast.');}</script><body onload="
                "'myFunction()''>")
    if request.method == 'POST':
        if (request.form['podcast_name'] and
                request.form['podcast_description']):
            podcast_for_edit.podcast_name = request.form['podcast_name']
            podcast_for_edit.podcast_description = request.form[
                'podcast_description']
            session.add(podcast_for_edit)
            session.commit()
            return redirect(url_for('show_podcasts'))
        else:
            flash("Yeah..... you need to populate all of these fields to "
                  "proceed... Try again please!")
            return render_template(
                'edit_podcasts.html', podcast=podcast_for_edit)
    else:
        return render_template('edit_podcasts.html', podcast=podcast_for_edit)

# Delete Podcast from database


@app.route('/<int:podcast_id>/delete', methods=['GET', 'POST'])
def delete_podcasts(podcast_id):
    podcast_for_deletion = session.query(
        Podcast).filter_by(podcast_id=podcast_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if podcast_for_deletion.podcast_user_id != login_session['user_id']:
        return ("<script>function myFunction() {alert('You are not "
                "authorized to delete this Podcast.');}</script><body onload="
                "'myFunction()''>")
    if request.method == 'POST':
        session.delete(podcast_for_deletion)
        session.commit()
        return redirect(url_for('show_podcasts'))
    else:
        return render_template(
            'delete_podcasts.html', podcast=podcast_for_deletion)

# EPISODE MANAGEMENT BLOCK

# Load list of episodes


@app.route('/<int:podcast_id>')
def show_episodes(podcast_id):
    podcast = session.query(Podcast).filter_by(podcast_id=podcast_id).one()
    episodes = session.query(Episode).filter_by(podcast_id=podcast_id).all()
    return render_template(
        'show_episodes.html', podcast=podcast, episodes=episodes)

# Load Podcast episodes (for a particular podcast) into JSON format for API
# endpoint


@app.route('/<int:podcast_id>/JSON')
def show_episodes_JSON(podcast_id):
    episodes = session.query(Episode).filter_by(podcast_id=podcast_id).all()
    return jsonify(Episode=[i.serialize for i in episodes])

# Load a particular podcast episode into JSON format for API endpoint


@app.route('/<int:podcast_id>/<int:episode_id>/JSON')
def show_episodes_particular_JSON(podcast_id, episode_id):
    episode = session.query(Episode).filter_by(episode_id=episode_id).one()
    return jsonify(Episode=episode.serialize)

# Add a new episode


@app.route('/<int:podcast_id>/new', methods=['GET', 'POST'])
def new_episodes(podcast_id):
    if 'username' not in login_session:
        return redirect('/login')
    podcast = session.query(Podcast).filter_by(podcast_id=podcast_id).one()
    if request.method == 'POST':
        if (request.form['episode_name'] and
                request.form['episode_description'] and
                request.form['episode_date']):
            new_episode = Episode(
                episode_name=request.form['episode_name'],
                episode_description=request.form['episode_description'],
                episode_date=request.form['episode_date'],
                episode_listened='',
                podcast_id=podcast_id,
                episode_user_id=login_session['user_id'])
            session.add(new_episode)
            session.commit()
            return redirect(url_for('show_episodes', podcast_id=podcast_id))
        else:
            flash("Yeah..... you need to populate all of these fields to "
                  "proceed... Try again please!")
            return render_template('new_episodes.html', podcast=podcast)
    else:
        return render_template('new_episodes.html', podcast=podcast)

# Edit an existing episode


@app.route('/<int:podcast_id>/<int:episode_id>/edit', methods=['GET', 'POST'])
def edit_episodes(podcast_id, episode_id):
    podcast = session.query(
        Podcast).filter_by(podcast_id=podcast_id).one()
    episode_for_edit = session.query(
        Episode).filter_by(episode_id=episode_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if episode_for_edit.episode_user_id != login_session['user_id']:
        return ("<script>function myFunction() {alert('You are not "
                "authorized to edit this episode.');}</script><body onload="
                "'myFunction()''>")
    if request.method == 'POST':
        if (request.form['episode_name'] and
                request.form['episode_description'] and
                request.form['episode_date']):
            episode_for_edit.episode_name = request.form['episode_name']
            episode_for_edit.episode_description = request.form[
                'episode_description']
            episode_for_edit.episode_date = request.form['episode_date']
            episode_for_edit.episode_listened = request.form[
                'episode_listened']
        else:
            flash("Yeah..... you need to populate all of these fields to "
                  "proceed (except the 'Listened' one)... Try again please!")
            return render_template(
                'edit_episodes.html',
                podcast=podcast,
                episode=episode_for_edit)
        session.add(episode_for_edit)
        session.commit()
        return redirect(url_for('show_episodes', podcast_id=podcast_id))
    else:
        return render_template(
            'edit_episodes.html', podcast=podcast, episode=episode_for_edit)

# Delete an existing episode


@app.route('/<int:podcast_id>/<int:episode_id>/delete',
           methods=['GET', 'POST'])
def delete_episodes(podcast_id, episode_id):
    podcast = session.query(Podcast).filter_by(podcast_id=podcast_id).one()
    episode_for_deletion = session.query(
        Episode).filter_by(episode_id=episode_id).one()
    if episode_for_deletion.episode_user_id != login_session['user_id']:
        return ("<script>function myFunction() {alert('You are not "
                "authorized to delete this episode.');}</script><body onload="
                "'myFunction()''>")
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        session.delete(episode_for_deletion)
        session.commit()
        return redirect(url_for('show_episodes', podcast_id=podcast_id))
    else:
        return render_template(
            'delete_episodes.html',
            podcast=podcast,
            episode=episode_for_deletion)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    # app.debug = True
    app.run(host='0.0.0.0', port=5000)
