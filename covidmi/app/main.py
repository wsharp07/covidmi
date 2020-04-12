import pandas as pd
from covidmi_repo import CovidmiRepo
from data_loader import DataLoader
from data_parser import DataParser
from flask import Flask, Response, jsonify
from dotenv import load_dotenv
from flask_restx import Resource, Api, fields


def insert_data(repo, record):
    county = record['county']
    cases = record['cases']
    deaths = record['deaths']

    if repo.exists_for_today(county):
        return

    repo.insert((county, cases, deaths))


load_dotenv()

app = Flask(__name__)

api = Api(app, version='1.0',
          title='COVID-MI',
          description='County COVID-19 data in Michigan'
          )

ns_counties = api.namespace('counties', description='County operations')

county_model = api.model('CountyResponse',
                         {'id': fields.Integer(
                            required=True,
                            description="Record identifier",
                            example=1),
                          'county': fields.String(
                            required=True,
                            description="The county reporting",
                            example="Oakland"),
                          'cases': fields.Integer(
                            required=True,
                            description="Number of reported cases",
                            example=1000),
                          'deaths': fields.Integer(
                            required=True,
                            description="Number of reported deaths",
                            example=10),
                          'createdAt': fields.DateTime(
                            required=True,
                            description="When the record was created")})


@ns_counties.route('/load_data')
class LoadData(Resource):
    @api.doc(responses={201: 'Loaded New Data', 500: 'Server Error'})
    def post(self):
        repo = CovidmiRepo()
        parser = DataParser()
        dl = DataLoader(parser)
        data = dl.load_data()
        df = pd.DataFrame(data)

        for index, row in df.iterrows():
            insert_data(repo, row)

        return Response(status=201)


@ns_counties.route('/')
class Counties(Resource):
    @api.response(200, 'Success', county_model)
    def get(self):
        repo = CovidmiRepo()
        data = repo.get_all()
        return jsonify(data)


@ns_counties.route('/latest')
class CountiesLatest(Resource):
    @api.response(200, 'Success', county_model)
    def get(self):
        repo = CovidmiRepo()
        data = repo.get_all_latest()
        return jsonify(data)


@ns_counties.route('/<string:name>')
@ns_counties.param('name', 'County Name')
class CountyByName(Resource):
    @api.response(200, 'Success', county_model)
    def get(self, name):
        repo = CovidmiRepo()
        data = repo.get_by_county(name)
        return jsonify(data)


if __name__ == "__main__":
    app.run('0.0.0.0', 8989)
