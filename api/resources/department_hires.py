from flask_restful import Api, Resource, reqparse
from repositories.reports import Reports as reports
class DepartmentHires(Resource):
    def get(self,year):
        result, columns = reports.departments_by_hires(year)
        rows = [dict(zip(columns, row)) for row in result]
        return rows