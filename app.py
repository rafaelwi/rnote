from flask import Flask, render_template, request, send_from_directory
app = Flask(__name__)

import uuid
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
    return send_from_directory('', 'Welcome.pdf')


# Displays the webapp's favicon
@app.route('/favicon')
def showFavicon():
    return send_from_directory('', 'favicon.ico')    


# Display's user's PDF
@app.route('/temp/<string:filename>')
def displayNewPdf(filename):
    return send_from_directory('temp', filename)


# Error handler for 404
@app.errorhandler(404)
def error_404(error):
    return render_template('error.html'), 404
