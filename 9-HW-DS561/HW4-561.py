# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, request, abort, Response
from google.cloud import storage, logging, pubsub_v1

# current module (__name__) as argument.
app = Flask(__name__)
project_ID = "ds-561-398918"
bucket_name = "hw2-vm-bucket"
directory = "webdir/"
logger_name = "file_server_log"
topic_name = "file_server_topic"

def write_entry(message):
    logging_client = logging.Client()
    logger = logging_client.logger(logger_name)
    logger.log_text(message, severity='ERROR')

@app.route('/<path:filename>', methods=['GET', 'PUT', 'POST', 'DELETE', 'HEAD', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'])
def file_server(filename):
    # Check to see if the method is other than GET
    if request.method != 'GET':
        write_entry('Not Implemented')
        return abort(501, 'Not Implemented')

    filename = filename.rsplit('/', 1)[1]
    print(filename)
    # Check to see if it's forbidden
    banned_countries = ["North Korea", "Iran", "Cuba", "Myanmar", "Iraq", "Libya", "Sudan", "Zimbabwe", "Syria"]
    country = request.headers.get('X-country')
    if country and country in banned_countries:
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project_ID, topic_name)
        message_data = 'Forbidden Request from {}'.format(country)
        future = publisher.publish(topic_path, message_data.encode('utf-8'))

        return abort(400, 'Permision Denied')

    # filename = request.args.get('filename')

    # Initialize Storage Client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    blob_path = directory + filename
    blob = bucket.blob(blob_path)

    if blob.exists():
        content = blob.download_as_text()
        response = Response(content, content_type='text/plain')
        return response
    else:
        write_entry('File not Found')
        return abort(404, 'File not Found')

# main driver function
if __name__ == '__main__':

 app.run(host='0.0.0.0', port=8080)