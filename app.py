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
import dataframe_image as dfi
import numpy as np
from sklearn.mixture import GaussianMixture
from bson.objectid import ObjectId
from plot_data import table_maker, do_ttest
import pickle

import db
from views import posts, comments
from io import StringIO
from cluster_explorer import cluster_explore,cluster_explore2
import gridfs

app = Flask(__name__)
CORS(app)
db.init_database_connection(app)
api = Api(app)

dbname=app.config['MONGODB_SETTINGS']['db']
client = MongoClient('mongodb+srv://'+os.environ.get('DB_USER')+':'+os.environ.get('DB_PASSWORD')+'@' + os.environ.get('HOST') + '/' + os.environ.get('DATABASE_NAME') + '?retryWrites=true&w=majority')
newdb=client[dbname]
#griddb=newdb.gridfs_example
#fs = gridfs.GridFS(newdb)


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

# @app.route('/verify-data/')
# def view_data():
#     dbname = app.config['MONGODB_SETTINGS']['db']
#     client = MongoClient(
#         'mongodb+srv://' + os.environ.get('DB_USER') + ':' + os.environ.get('DB_PASSWORD') + '@' + os.environ.get(
#             'HOST') + '/' + os.environ.get('DATABASE_NAME') + '?retryWrites=true&w=majority')
#     newdb = client[dbname]
#     collection = newdb['csvs']
#     doc=collection[0]
#     print(doc)

@app.route('/learn-cluster/')
def learn_cluster():
    return render_template('learn-cluster.html')

@app.route('/cluster-explore/')
def explore_cluster():
    return render_template('cluster-explore.html')


@app.route('/learn-cluster/',methods=['POST'])
def make_cluster():
    #Workspace=request.form.get("workspace")
    #num_clusters = request.form.get("numofc")
    print(request.form)
    num_clusters = int(request.form.get("nofc"))
    ##this could get it from workspace name if we figure out endpoints
    data = pd.read_csv('temp1.csv')
    z = GaussianMixture(n_components=num_clusters, random_state=0)
    z.fit(data)
    filename = 'finalized_model.sav'
    pickle.dump(z, open(filename, 'wb'))
    cluster_explore(num_clusters)
    return redirect('/cluster-explore/')

@app.route('/cluster-explore/',methods=['POST'])
def compare_cluster():
    #Workspace=request.form.get("workspace")
    #num_clusters = request.form.get("numofc")
    clustera = int(request.form.get("groups"))-1
    clusterb = int(request.form.get("groups1"))-1
    print(clustera)
    ##this could get it from workspace name if we figure out endpoints
    filename = 'finalized_model.sav'
    z= pickle.load(open(filename, 'rb'))
    num_cluster=z.n_components
    data = pd.read_csv('temp1.csv')
    different_list,same_list=do_ttest(data,z,clustera,clusterb)
    print(different_list)
    print(same_list)
    #cluster_explore(num_clusters)
    cluster_explore2(num_cluster,different_list,same_list,clustera,clusterb)
    return redirect('/feature-compare/')

@app.route('/feature-compare/')
def feature_compare():
    return render_template('cluster-explore2.html')

@app.route('/feature-compare/',methods=['POST'])
def compare_cluster2():
    #Workspace=request.form.get("workspace")
    #num_clusters = request.form.get("numofc")
    clustera = int(request.form.get("groups"))-1
    clusterb = int(request.form.get("groups1"))-1
    print(clustera)
    ##this could get it from workspace name if we figure out endpoints
    filename = 'finalized_model.sav'
    z= pickle.load(open(filename, 'rb'))
    num_cluster=z.n_components
    data = pd.read_csv('temp1.csv')
    different_list,same_list=do_ttest(data,z,clustera,clusterb)
    print(different_list)
    print(same_list)
    #cluster_explore(num_clusters)
    cluster_explore2(num_cluster,different_list,same_list,clustera,clusterb)
    return redirect('/feature-compare/')


@app.route('/add-cluster/',methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    workspace = request.form.get("wspace")
    if uploaded_file.filename != '':
        name_file = uploaded_file.filename
        #uploaded_file.save('temp1.csv')
        data = pd.read_csv(uploaded_file)
        collection = newdb['csvs']
        collection2 = newdb['index']
        names_taken=collection2.find().distinct('_id')
        if workspace in names_taken:
            return "Workspace name taken, please go back and try again."
        df2 = data.head(5)
        samples=len(data)
        cols=len(data.columns)

        def rower(data):
            s = data.index % 2 != 0
            s = pd.concat([pd.Series(s)] * data.shape[1], axis=1)  # 6 or the n of cols u have
            z = pd.DataFrame(np.where(s, 'background-color:#add8e6', ''),
                             index=data.index, columns=data.columns)
            return z

        df_styled = df2.style.set_caption(f'Your table, {name_file}, has {samples} entries and {cols} columns!')
        df_styled= df_styled.apply(rower,axis=None)
        dfi.export(df_styled, "static/mytable.png")
        #df_table=table_maker(df2)
        #a = fs.put(df_table,filename=workspace+"table")
        data_dict = json.loads(data.to_json())
        _id = collection.insert(data_dict)
        idstr=str(_id)
        collection2.insert({'_id':workspace, 'csvid':_id})
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