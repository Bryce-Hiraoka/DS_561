from flask import Flask, request, make_response, Response, abort
from google.cloud import storage, pubsub_v1

bucket_name = "bhiraoka-hw2-bucket"
directory = "hw2-files/HW2/"
project_id = "ds-561-398918"
topic_name = "request-location"

app = Flask(__name__)

@app.route('/<path:filename>', methods=['GET','PUT','POST','DELETE','HEAD','CONNECT','OPTIONS','TRACE','PATCH'])
def index(filename):
    if request.method != 'GET':
        response = make_response("<h1>Not Implemented</h1>", 501)
        return response

    filename = filename.rsplit('/', 1)[1]

    countries = [b'North Korea', b'Iran', b'Cuba', b'Myanmar', b'Iraq', b'Libya', b'Sudan', b'Zimbabwe', b'Syria']
    country = request.headers.get('X-country')

    if country and country in countries:
        return "working kind of"
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project_id, topic_name)
        message_data = 'Forbidden Request from {}'.format(country)
        future = publisher.publish(topic_path, message_data.encode('utf-8'))

        return abort(400, 'Permision Denied')

    client = storage.Client();
    bucket = client.bucket(bucket_name)

    blob_path = directory + filename
    blob = bucket.blob(blob_path)

    if blob.exists():
        content = blob.download_as_text()
        response = Response(content, content_type='text/plain')
        return country
    else:
        response = make_response("<h1>File Not Found</h1>", 404)
        return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)