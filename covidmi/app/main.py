import pandas as pd
from covidmi_repo import CovidmiRepo
from data_loader import DataLoader
from data_parser import DataParser
from flask import Flask, Response, jsonify

def insert_data(repo, record):
  county = record['county']
  cases = record['cases']
  deaths = record['deaths']

  if repo.exists_for_today(county): return

  repo.insert((county,cases,deaths))


app = Flask(__name__)

@app.route("/load_data", methods=['POST'])
def load_data():
  repo = CovidmiRepo()
  parser = DataParser()
  dl = DataLoader(parser)
  data = dl.load_data()
  df = pd.DataFrame(data)

  for index, row in df.iterrows():
    insert_data(repo,row)

  return Response(status=200)

@app.route("/counties")
def get_county_data():
  repo = CovidmiRepo()
  data = repo.get_all()
  return jsonify(data)

@app.route("/counties/latest")
def get_county_data_latest():
  repo = CovidmiRepo()
  data = repo.get_all_latest()
  return jsonify(data)

@app.route("/counties/<name>")
def get_county_by_name(name):
  repo = CovidmiRepo()
  data = repo.get_by_county(name)
  return jsonify(data)

if __name__ == "__main__":        # on running python app.py
    app.run('0.0.0.0',8989)