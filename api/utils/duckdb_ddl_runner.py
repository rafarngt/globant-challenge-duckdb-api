import duckdb
import os

def get_ddl_files(ddl_dir):
    return [os.path.join(ddl_dir, f) for f in os.listdir(ddl_dir) if f.endswith('.sql')]

class DuckDBDDLRunner:
    def __init__(self, db_path=None, ddl_dir=None):

        self.db_path = db_path or os.environ.get('DUCKDB_PATH', '../data/duckdb/db/data.db')
        self.ddl_dir = ddl_dir or '../data/duckdb/ddl'
        # create a connection to a file called 'file.db'
        con = duckdb.connect(self.db_path)
        ddl_files = get_ddl_files(self.ddl_dir)
        for ddl_file in ddl_files:
            with open(ddl_file, 'r') as f:
                sql = f.read()
                con.execute(sql) 
        
        con.close()

    def run_all_ddls(self):
       pass