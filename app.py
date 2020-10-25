from flask import Flask, render_template, request, send_from_directory, redirect, url_for
app = Flask(__name__)

import uuid
import imp
import rnote_for_webapp as rnote

DEFAULT_TEXT = """// Enter your note below and click 'compile' to generate it!
.pp theme modern
.pp size letter
.pp margin normal
.pp title My RNote Demo Note
.pp align vert
"""

# Displays the homepage
# Page has to go into templates regardless of whether it actually uses the template features or not
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html', pdf_filename='./out', code=DEFAULT_TEXT)

    elif request.method == 'POST':
        # Get the "code" and generate a new filename with a UUID
        code = request.form['code']
        filename = 'temp/' + str(uuid.uuid4()) + '.pdf'

        # Send off the code and filename to be processed
        rnote.run(code, filename)
        return render_template('index.html', pdf_filename=filename, code=code)


# Displays the pdf
@app.route('/out')
def showIntroPDF():
    return send_from_directory('', 'out.pdf')

@app.route('/favicon')
def showFavicon():
    return send_from_directory('', 'favicon.ico')    


@app.route('/temp/<string:filename>')
def displayNewPdf(filename):
    return send_from_directory('temp', filename)


# This is how you do error handling
# We need to pass in the error parameter in regardless
# This part can stay, we just need to modify error.html
# Look into wekzeug for error codes for insufficient storage
@app.errorhandler(404)
def error_404(error):
    return render_template('error.html'), 404
