import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

# Connect to Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# Load the employee data with specified encoding
df = pd.read_csv('employee.csv', encoding='ISO-8859-1')

# Clean the 'Annual Salary' column by removing dollar signs and commas, then convert to float
df['Annual Salary'] = df['Annual Salary'].replace({r'\$': '', ',': ''}, regex=True).astype(float)

# Drop rows with missing or invalid values (NaN) in important fields
df.dropna(subset=['Employee ID', 'Full Name', 'Job Title', 'Age', 'Annual Salary'], inplace=True)

# Create an index for employees (ignore if it already exists)
es.options(ignore_status=400).indices.create(index='employees')

# Function to generate data for bulk indexing
def generate_data(dataframe):
    for index, row in dataframe.iterrows():
        yield {
            "_index": "employees",
            "_id": index,
            "_source": {
                "employee_id": row['Employee ID'],
                "employee_name": row['Full Name'],
                "job_title": row['Job Title'],
                "age": row['Age'],
                "salary": row['Annual Salary']
            }
        }

# Attempt to bulk index the data and capture success and failure counts
try:
    success, failed = bulk(es, generate_data(df), stats_only=True)
    print(f"Data indexed successfully. {success} documents indexed, {failed} failed.")

    # If there are failed documents, log the errors
    if failed > 0:
        print(f"{failed} documents failed to index.")
        for action in generate_data(df):
            try:
                es.index(index='employees', id=action['_id'], body=action['_source'])
            except Exception as e:
                print(f"Failed to index document ID {action['_id']}: {e}")

except Exception as e:
    print(f"An error occurred during bulk indexing: {e}")

# Query to verify that data is indexed
res = es.search(index="employees", body={"query": {"match_all": {}}})
print(f"Total Records Found: {res['hits']['total']['value']}")
