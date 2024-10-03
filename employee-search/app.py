from flask import Flask, render_template, request, jsonify
from elasticsearch import Elasticsearch

app = Flask(__name__)

# Connect to Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    # Get search query from the form
    search_query = request.form['query']

    # Elasticsearch search
    body = {
        "query": {
            "multi_match": {
                "query": search_query,
                "fields": ["employee_name", "job_title", "employee_id"]
            }
        }
    }
    
    res = es.search(index="employees", body=body)
    
    # Extract the results
    hits = res['hits']['hits']
    results = []
    
    for hit in hits:
        results.append({
            'employee_id': hit['_source']['employee_id'],
            'employee_name': hit['_source']['employee_name'],
            'job_title': hit['_source']['job_title'],
            'age': hit['_source']['age'],
            'salary': hit['_source']['salary']
        })
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
