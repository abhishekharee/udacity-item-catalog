# Project: Item Catalog

## Description
This project creates a web app that helps a specific user manage podcsts that he listens to. The web app allows the user to add, update, edit and delete current podcasts that the user is following, as well as add, update, edit and delete episodes for each podcast that the user is following. The web app provides JSON API end-points to enable other developers to leverage the content stored in the item catalog.

## Prerequisites
This project requires the following to be in place prior to successful execution:
- Ubuntu 16.04 LTS (available [here](http://releases.ubuntu.com/16.04/))
- Python 2.7.12 (available [here](https://www.python.org/downloads/release/python-2712/))
- All files currently stored in this repository. **These files must be laid out in their current file-folder structure.**

The python scripts that create the web app import several libraries in order to build the web app sucessfully. These libraries are:

- sqlalchemy
- sqlalchemy.orm
- sqlalchemy.ext.declarative
- os
- sys
- flask
- oauth2client.client
- random
- string
- httplib2
- json
- requests

In case these libraries are not already installed on your computer, they can be installed using the `pip install` comamand. For example, to install flask, run this command in the terminal:

`pip install flask`

_Note: The above set up can be achieved via a virtual machine. Set up of a virtual machine is optional, and beyond the scope of this README._

## Set up
1. Download and/or install all prerequisites described above.
2. Open the terminal, and change directory into the root directory of this repository (as downloaded on your machine).
3. Set up the podcast database by running `python podcast_database_setup.py`.
4. Load data into the database by running `python podcast_database_load.py`.
5. Run the app by running `python podcast_webapp.py`.

## Execution
The 'Set Up' steps above will have initialised the database of podcasts and podcast episodes, and created the web app that will allow users to interact with that database via the browser. To use the webapp, visit `http://localhost:5000`.

_Note: Any additions, deletions, and updates to the database will require the user to log in using a Google account.

## Author
Abhishekharee Parthasarathy

me@abhishekharee.com
