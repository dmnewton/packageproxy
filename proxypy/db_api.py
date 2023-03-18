from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class Packages(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  blackwhite = db.Column(db.String(1), unique=False, nullable=False)
  regex = db.Column(db.String(80), unique=False, nullable=False)
  description = db.Column(db.String(120), unique=False, nullable=False)

  def __init__(self, body):
    self.blackwhite = body['blackwhite']
    self.regex = body['regex']
    self.description = body['description']

class Repositories(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  server = db.Column(db.String(80), unique=True, nullable=False)
  description = db.Column(db.String(120), unique=False, nullable=False)

  def __init__(self, body):
    self.server = body['server']
    self.description = body['description']

class Clients(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  server = db.Column(db.String(80), unique=True, nullable=False)
  description = db.Column(db.String(120), unique=False, nullable=False)

  def __init__(self, body):
    self.server = body['server']
    self.description = body['description']

# add table to dictionary to link URL base and table

tables = { 'packages': Packages, 'repositories' : Repositories, 'clients' : Clients}

@app.route('/<table>/<id>', methods=['GET'])
def get_package(table,id):
  package = db.session.get(Packages,id)
  del package.__dict__['_sa_instance_state']
  return jsonify(package.__dict__)

@app.route('/<table>', methods=['GET'])
def get_packages(table):
  tab = tables.get(table)
  packages = []
  for package in db.session.query(tab).all():
    del package.__dict__['_sa_instance_state']
    packages.append(package.__dict__)
  return jsonify(packages)

def copy_body_to_dict(body,tab):
    """copied only required fields"""
    res = dict()
    columns =tab.__table__.columns
    for col in columns:
      try:
        res[col.name] = body[col.name]
      except:
        continue
    return res

@app.route('/<table>', methods=['POST'])
def create_package(table):
  tab = tables.get(table)
  #app.logger.info("xxx %s",tab.__table__.c)
  body = request.get_json()
  d_body=copy_body_to_dict(body,tab)
  db.session.add(tab(d_body))
  db.session.commit()
  return "package created"

@app.route('/<table>/<id>', methods=['PUT'])
def update_package(table,id):
  tab = tables.get(table)
  body = request.get_json()
  d_body=copy_body_to_dict(body,tab)
  rows_updated=db.session.query(Packages).filter_by(id=id).update(d_body)
  db.session.commit()
  return f"rows updated {rows_updated}"

@app.route('/<table>/<id>', methods=['DELETE'])
def delete_package(table,id):
  tab = tables.get(table)
  rows_deleted=db.session.query(tab).filter_by(id=id).delete()
  db.session.commit()
  return f"rows deleted {rows_deleted}"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0',debug = True, use_reloader= False)