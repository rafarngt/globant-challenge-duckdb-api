from flask_restful import Api, Resource, reqparse
from repositories.reports import Reports as reports
class HiresByQuarter(Resource):
    def get(self,year):
        result, columns = reports.hiries_by_quarter(year)
        rows = [dict(zip(columns, row)) for row in result]
        return rows
