"""
Simple flask app
"""
import os
from flask import (Flask, request, redirect, url_for, send_from_directory,
                   flash, render_template)
import pandas as pd
from werkzeug.utils import secure_filename
from output_keys import output_keys
import requests
import asyncio
import json

#import tempfile
app = Flask(__name__)

# Set the location where uploaded files will be stored (/tmp/ is probably ok)
# Note that at present these will remain on the server until it is rebooted.

ALLOWED_EXTENSIONS = set(['csv'])
UPLOAD_FOLDER = '/tmp/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set the app secret key to prevent CSRF

app.secret_key = os.urandom(24)

# Which extensions are allowed to be uploaded?


def call_register_checker(string_to_match, register, field = 'name'):
    """
    What do I do?

    :param string_to_match: <str> This is what is expected....

    """
    url = 'https://registerchecker.cloudapps.digital'
    payload = {
        'strings': string_to_match,
        'register': register,
        'field': field,
        }
    headers = {'content-type': 'application/json'}
    r = requests.post(url, json=payload, headers=headers)
    rj = json.loads(r.text)

    if rj['register']:
        return rj


def allowed_file(filename):
    """
    Check that the selected file is allowed

    :param filename: <string> Filename of local file to be uploaded
    :return: <boolean> True if filename is valid and extension is in
     ALLOWED_EXTENSIONS, else False.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Demonstrate an example of how to upload files to the server.


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """
    Upload a file using a simple form
    """
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash(u'No file part', 'error')
            return redirect(request.url)
        selected_file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if selected_file.filename == '':
            flash(u'No selected file', 'error')
            return redirect(request.url)
        if selected_file and not allowed_file(selected_file.filename):
            flash(u'File is not of authorised type', 'error')
            return redirect(request.url)
        if selected_file and allowed_file(selected_file.filename):
            filename = secure_filename(selected_file.filename)
            selected_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('parse_file',
                                    filename=filename))
    return render_template('upload.html')

# Render the file back to the user.

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    Render uploaded file as a new webpage
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/parse/<filename>', methods=['GET', 'POST'])
def parse_file(filename):
    """

    """
    filepath = UPLOAD_FOLDER + secure_filename(request.path.split('/')[-1])
    df = pd.read_csv(filepath)
    if request.method == 'POST':
        field = request.form['field']
        if field not in df.columns:
            flash(u'Please select a valid field', 'error')
            return redirect(request.url)
        return redirect(url_for('parse_confirm', filename=filename, field=field))
    return render_template('parse.html', filename=filename)

@app.route('/parse_confirm/<filename>/<field>', methods=['GET', 'POST'])
def parse_confirm(filename, field):
    """

    """
    filepath = UPLOAD_FOLDER + secure_filename(request.path.split('/')[-2])
    df = pd.read_csv(filepath)
    column = df[field].head(20).tolist()

    if request.method == 'POST':
        if request.form['submit'] == 'Yes':
            return redirect(url_for('parse_confirmed', filename=filename, field=field))
        else:
            return redirect(url_for('parse_file', filename=filename))

    return render_template('parse_confirm.html', filename=filename, field=field, column=column)

    #selected_field = request.args.get('field')

@app.route('/parse_confirmed/<filename>/<field>', methods=['GET', 'POST'])
def parse_confirmed(filename, field):
    """

    """
    filepath = UPLOAD_FOLDER + secure_filename(request.path.split('/')[-2])
    df = pd.read_csv(filepath)

    output = []

    if request.method == 'GET':
        for index, row in df.iterrows():
            check = call_register_checker(row[field], 'local-authority-eng', field=field)
            output.append(check)
    
    unwanted = ['row.names','phase','index-entry-number','entry-number','entry-timestamp','key']


    output = [i for i in output if i]
    for i, j in enumerate(output):

        if i == 0:
            j = output_keys(j, unwanted)
            j = pd.DataFrame.from_dict(j)
            j['origin'] = df['name'][i]
            result_table = j.copy()
        if i > 0:
            j = output_keys(j, unwanted)
            j = pd.DataFrame.from_dict(j)
            j['origin'] = df['name'][i]
            result_table = pd.concat([result_table, j])

    # Convert start date to UTC date
    
    result_table['start-date'] = pd.to_datetime(result_table['start-date'])
    # Order columns more senibly
    
    #result_table = result_table[[<list of column names here>]]
    
    return render_template('table.html',table=[result_table.to_html(classes='name')])

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
