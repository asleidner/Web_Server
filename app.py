'''
To run on command line:
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
'''
from flask_restful import Api
from flask import Flask, request, Response
from flask_cors import CORS
from flask import render_template  # New in HW02
from flask import redirect, url_for
import pandas as pd
import os
from pymongo import MongoClient
import json
import numpy as np
import dataframe_image as dfi

import db
from views import posts, comments

app = Flask(__name__)
CORS(app)
db.init_database_connection(app)
api = Api(app)


########################### New in HW02
@app.route('/')
def list_posts():
    return render_template('get-posts.html')

@app.route('/add-cluster/')
def create_post():
    return render_template('create-cluster.html')

@app.route('/verify-data/')
def verify_data():
    return render_template('verify-data.html')

@app.route('/verify-data/')
def view_data():
    dbname = app.config['MONGODB_SETTINGS']['db']
    client = MongoClient(
        'mongodb+srv://' + os.environ.get('DB_USER') + ':' + os.environ.get('DB_PASSWORD') + '@' + os.environ.get(
            'HOST') + '/' + os.environ.get('DATABASE_NAME') + '?retryWrites=true&w=majority')
    newdb = client[dbname]
    collection = newdb['csvs']
    doc=collection[0]
    print(doc)

@app.route('/add-cluster/',methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        dbname=app.config['MONGODB_SETTINGS']['db']
        client = MongoClient('mongodb+srv://'+os.environ.get('DB_USER')+':'+os.environ.get('DB_PASSWORD')+'@' + os.environ.get('HOST') + '/' + os.environ.get('DATABASE_NAME') + '?retryWrites=true&w=majority')
        newdb=client[dbname]
        uploaded_file.save('temp1.csv')
        data = pd.read_csv('temp1.csv')
        collection = newdb['csvs']
        df2 = data.head(5)
        df_styled = df2.style.background_gradient()
        dfi.export(df_styled, "static/mytable.png",max_rows=5,max_cols=10)
        data_dict = json.loads(data.to_json())
        collection.insert(data_dict)
    return redirect('/verify-data/')

@app.route('/post/')
def get_single_post():
    return render_template('post-detail.html')
########################### End New in HW02


# routes from other files:
posts.initialize_routes(api)
comments.initialize_routes(api)



if __name__ == "__main__":
    print('running!')
    app.run(debug=True)