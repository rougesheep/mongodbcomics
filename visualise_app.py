from flask_pymongo import PyMongo
from flask import Flask, render_template
from flask import request, jsonify
import json
import ast

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'Physical_Comics'  # name of database on mongo
app.config["MONGO_URI"] = "mongodb://localhost:27017/Physical_Comics"
mongo = PyMongo(app)
marvel = mongo.db.marvel


@app.route('/')
def welcome():
    return render_template('homepage.html')


@app.route('/marvel', methods=['GET'])
def get_marvel_comics():
    # TODO create a page that gets the contents of the marvel collection

    m_comics = mongo.db.marvel
    output = []
    for m in marvel.find():
        output.append({'title': m['title'], 'writer': m['writer'], 'artist': m['artist']})
    return jsonify({'result': output})


@app.route('/marvel/', methods=['GET'])
def get_writer(name):
    marvel_writer = mongo.db.marvel
    n = marvel_writer.find_one({'name': name})
    if n:
        output = {'title': n['title'], 'writer': n['writer'], 'artist': n['artist']}
    else:
        output = "No such name"
    return jsonify({'result': output})


@app.route("/marvel/create", methods=['POST'])
def create_book():
    """
       Function to create new users.
       """
    try:
        # Create new users
        try:
            body = ast.literal_eval(json.dumps(request.get_json()))
        except:
            # Bad request as request body is not available
            # Add message for debugging purpose
            return "", 400

        record_created = marvel.insert(body)

        # Prepare the response
        if isinstance(record_created, list):
            # Return list of Id of the newly created item
            return jsonify([str(v) for v in record_created]), 201
        else:
            # Return Id of the newly created item
            return jsonify(str(record_created)), 201
    except:
        # Error while trying to create the resource
        # Add message for debugging purpose
        return "", 500


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)