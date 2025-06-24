
import pandas as pd
import json
from datetime import datetime

class UtilsFuntions:

    @staticmethod
    def validate_table_name(table_name):
        """Validates if the provided table name is valid."""
        return table_name in ['departments', 'hired_employees', 'jobs']
    @staticmethod
    def read_csv_into_dataframe(file, schema):
        """Reads a CSV file into a pandas DataFrame using the provided schema."""
        df = pd.read_csv(file, sep=',', header=None, names=[field.name for field in schema])
        return df
    @staticmethod
    def remove_rows_with_nan(df):
        df_cleaned = df.dropna()
        df_removed = df[~df.index.isin(df_cleaned.index)]
        return df_cleaned, df_removed
    
    @staticmethod
    def save_failed_rows_to_gcs(errors, filename, gcs_client, gcs_bucket):
        bucket = gcs_client.get_bucket(gcs_bucket)
        blob = bucket.blob(f'failed_rows/{filename}')
        blob.upload_from_string(json.dumps(errors))
    
    @staticmethod
    def save_removed_rows_to_gcs(df_removed, filename, gcs_client, gcs_bucket):
        log_message = "\n".join([f"Row {i}: {row}" for i, row in df_removed.iterrows()])
        bucket = gcs_client.get_bucket(gcs_bucket)
        current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        blob = bucket.blob(f'failed_rows/{filename}-dataframe_log-{current_datetime}.txt')
        blob.upload_from_string(log_message)