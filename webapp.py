from flask import Flask, render_template, request, send_from_directory
app = Flask(__name__)

# Displays the homepage
# Page has to go into templates regardless of whether it actually uses the template features or not
@app.route('/')
def index():
    return render_template('hi.html')

# Displays the pdf
# TODO: Accept an id to display the correct file to the correct user
@app.route('/out')
def peedeeeff():
    return send_from_directory('', 'out.pdf')

# Test route
@app.route('/hello')
def hello():
    return 'Hello world!'

# This is how you'd use a template with an input from the url
# Could be useful for displaying pdf?
@app.route('/user/<string:username>')
def user(username):
    return 'User {}'.format(username)

