from flask import Flask, request, make_response, Response
from google.cloud import storage

app = Flask(__name__)
bucket = "bhiraoka-hw2-bucket"
directory = "content/"

'''
@app.route('/', methods=['GET'])
def main():
    if request.method != 'GET':
        response = make_response("<h1>Not Implemented</h1>", 501)
        return response

    filename = request.args.get('filename')

    storage_client = storage.Client();
    bucket = storage_client.bucket(bucket_name)

    blob_path = directory + filename
    blob = bucket.blob(blob_path)

    if blob.exists():
        content = blob.download_as_text()
        reponse = Response(content, content_type='text/plain')
        return response
    else:
        response = make_response("<h1>File Not Found</h1>", 404)
        return response

if __name__ == '__main__':
    app.run(port=8000)

app = Flask(__name__)
'''


@app.route("/")
def hello() -> str:
    """Return a friendly HTTP greeting.

    Returns:
        A string with the words 'Hello World!'.
    """
    return "Hello World!"


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app.
    app.run(host="127.0.0.1", port=8080, debug=True)