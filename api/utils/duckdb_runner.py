import duckdb
import os

def get_ddl_files(ddl_dir):
    return [os.path.join(ddl_dir, f) for f in os.listdir(ddl_dir) if f.endswith('.sql')]

class DuckDBRunner:
    @staticmethod
    def run_all_ddls():
        db_path = os.environ.get('DUCKDB_PATH', '../data/duckdb/db/data.db')
        ddl_dir = '../data/duckdb/ddl'
        # create a connection to a file called 'file.db'
        con = duckdb.connect(db_path)
        ddl_files = get_ddl_files(ddl_dir)
        for ddl_file in ddl_files:
            with open(ddl_file, 'r') as f:
                sql = f.read()
                con.execute(sql) 
        
        con.close()

    @staticmethod
    def execute_query(query):
        db_path = os.environ.get('DUCKDB_PATH', '../data/duckdb/db/data.db')
        con = duckdb.connect(db_path)
        con.execute(query)
        result = con.fetchall()
        con.close()

        return result
    
        
    @staticmethod
    def executemany_query(query, df):
        db_path = os.environ.get('DUCKDB_PATH', '../data/duckdb/db/data.db')
        con = duckdb.connect(db_path)
        con.executemany(query,df)
        result = con.fetchall()
        con.close()

        return result
