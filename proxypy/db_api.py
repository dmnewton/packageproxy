from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class Package(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  blackwhite = db.Column(db.String(1), unique=False, nullable=False)
  regex = db.Column(db.String(80), unique=True, nullable=False)
  description = db.Column(db.String(120), unique=True, nullable=False)

  def __init__(self, blackwhite,regex, description):
    self.blackwhite = blackwhite
    self.regex = regex
    self.description = description

@app.route('/packages/<id>', methods=['GET'])
def get_package(id):
  package = package.query.get(id)
  del package.__dict__['_sa_instance_state']
  return jsonify(package.__dict__)

@app.route('/packages', methods=['GET'])
def get_packages():
  packages = []
  for package in db.session.query(Package).all():
    del package.__dict__['_sa_instance_state']
    packages.append(package.__dict__)
  app.logger.info("packages %s",packages)
  return jsonify(packages)

@app.route('/packages', methods=['POST'])
def create_package():
  body = request.get_json()
  db.session.add(Package(body['blackwhite'],body['regex'], body['description']))
  db.session.commit()
  return "package created"

@app.route('/packages/<id>', methods=['PUT'])
def update_package(id):
  body = request.get_json()
  db.session.query(Package).filter_by(id=id).update(
    dict(blackwhite=body['blackwhite'],regex=body['regex'], description=body['description']))
  db.session.commit()
  return "package updated"

@app.route('/packages/<id>', methods=['DELETE'])
def delete_package(id):
  db.session.query(Package).filter_by(id=id).delete()
  db.session.commit()
  return "package deleted"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0',debug = True)