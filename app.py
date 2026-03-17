from flask import Flask, request, jsonify
from config import DATABASE_URI
from models.meal import Meal
from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/hello-world', methods=['GET'])
def hello_world():
  return 'Hello World!'

if __name__ == '__main__':
  app.run(debug=True)