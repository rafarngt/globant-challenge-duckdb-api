import logging as logs
from flask_restful import Resource, reqparse
import duckdb
import werkzeug
from werkzeug.utils import secure_filename
from utils.utils_funtions import UtilsFuntions as utilsFuntions
import os
import pandas as pd
import time

class DataUpload(Resource):
    """API resource for uploading data to DuckDB."""
    section = 'upload-data'
    

    def post(self):
        """Handles the POST request for uploading data."""
        logs.info("endpoint {}".format(self.section))
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files', required=True)
        parser.add_argument('table_name', type=str, location='form', required=True, help='El nombre de la tabla es obligatorio')
        args = parser.parse_args()
        file = args['file']
        table_name = args['table_name']

        if not file:
            return {'message': 'No se encontro ningun archivo'}, 400

        filename = secure_filename(file.filename)
        extension = os.path.splitext(filename)[1]
        table_name = table_name.lower()

        try:
            if not utilsFuntions.validate_table_name(table_name):
                return {'message': f'El nombre de tabla {table_name} no es valido'}, 400

            if extension != '.csv':
                return {'message': 'Formato de archivo no compatible'}, 400
            
            # Leer CSV a DataFrame (sin cabecera)
            df = pd.read_csv(file, header=None)
            df_cleaned, df_removed = utilsFuntions.remove_rows_with_nan(df)

            # Crear tabla si no existe e insertar datos por lotes
            db_path = os.environ.get('DUCKDB_PATH', '../data/duckdb/db/data.db')
            con = duckdb.connect(db_path)
            batch_size = 1000
            total_rows = len(df_cleaned)
            print(f"Total de filas: {total_rows}")
            for start in range(0, total_rows, batch_size):
                logs.info(f"Insertando datos por lotes de {start} a {start + batch_size}")
                end = min(start + batch_size, total_rows)
                batch = df_cleaned.iloc[start:end]
                placeholders = ','.join(['?'] * len(batch.columns))
                con.executemany(
                    f"INSERT INTO {table_name} VALUES ({placeholders})",
                    batch.values.tolist()
                )
            con.close()

            # Guardar filas removidas localmente si existen
            if len(df_removed) > 0:
                removed_path = f"../data/csv/removed_{filename}_{time.time()}.csv" 
                df_removed.to_csv(removed_path, index=False)

            return {'message': f'Registros insertados en {table_name}', 'filas_removidas': len(df_removed)}
        
        except Exception as e:
            return {'message': f'Error al procesar el archivo: {str(e)}'}, 500
