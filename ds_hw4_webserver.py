import functions_framework
from flask import Flask, request, make_response, Response
#from google.cloud import storage

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    if request.method != 'GET':
        response = make_response("<h1>Not Implemented</h1>", 501)
        return response
    return 'hello world'
"""
    file = request.args.get('filename')

    storage_client = storage.Client();
    bucket = storage_client.bucket(bucket)

    blob_path = directory + filename
    blob = bucket.blob(blob_path)

    if blob.exists():
        content = blob.download_as_text()
        reponse = Response(content, content_type='text/plain')
        return response
    else:
        response = make_response("<h1>File Not Found</h1>", 404)
        return response
"""

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port='8000')