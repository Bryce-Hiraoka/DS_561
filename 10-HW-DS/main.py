from flask import Flask, request, abort, Response
from google.cloud import storage, logging, pubsub_v1
from google.cloud.sql.connector import Connector
import sqlalchemy

app = Flask(__name__)
project_ID = "ds-561-398918"
bucket_name = "hw2-vm-bucket"
directory = "webdir/"
region = "us-east1"
instance_name = "hw5-database"
logger_name = "file_server_log"
topic_name = "file_server_topic"

# initialize parameters
INSTANCE_CONNECTION_NAME = f"{project_ID}:{region}:{instance_name}" # i.e demo-project:us-central1:demo-instance
print(f"Your instance connection name is: {INSTANCE_CONNECTION_NAME}")
# DB_USER = "file-server-user"
DB_USER = "mainUser"
DB_PASS = "Ryozo2011"
DB_NAME = "file_store"

connector = Connector()

# function to return the database connection object
def getconn():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    return conn

# create connection pool with 'creator' argument to our connection object function
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
    pool_size=20,
    max_overflow=30
)

def table_exists(engine, table_name):
    result = engine.execute(
        sqlalchemy.text(f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}')")
    )
    return result.scalar()


def db_entry(method=None, country=None, Client_IP=None, TimeStamp=None, RequestedFile=None, Gender=None, Age=None, Income=None, isBanned=None, exists=True):
    with pool.connect() as db_conn:
    # Check to see if table exist. If they do not we create them:
        if not table_exists(db_conn, 'RequestErrors'):
            db_conn.execute(sqlalchemy.text(
                """
                    CREATE TABLE RequestErrors (
                        ErrorID INT AUTO_INCREMENT PRIMARY KEY,
                        TimeOfRequest TIMESTAMP,
                        RequestedFile VARCHAR(255),
                        ErrorCode INT
                    )
                """
            ))

        if not table_exists(db_conn, 'Requests'):
            db_conn.execute(sqlalchemy.text(
                """
                    CREATE TABLE Requests (
                        RequestID INT AUTO_INCREMENT PRIMARY KEY,
                        Country VARCHAR(255),
                        Client_IP VARCHAR(255),
                        TimeStamp VARCHAR(255),
                        RequestedFile VARCHAR(255),
                        Gender VARCHAR(255),
                        Age VARCHAR(255),
                        Income VARCHAR(255),
                        IsBanned BOOLEAN
                    )
                """
            ))

        insert_stmt = sqlalchemy.text(f'INSERT INTO RequestErrors (TimeOfRequest, RequestedFile, ErrorCode) VALUES (:TimeOfRequest, :RequestedFile, :ErrorCode)')
        if isBanned:
            db_conn.execute(insert_stmt, parameters={"TimeOfRequest": TimeStamp, "RequestedFile": RequestedFile, "ErrorCode": 400})
        elif method != "GET":
            db_conn.execute(insert_stmt, parameters={"TimeOfRequest": TimeStamp, "RequestedFile": RequestedFile, "ErrorCode": 501})
        elif not exists:
            db_conn.execute(insert_stmt, parameters={"TimeOfRequest": TimeStamp, "RequestedFile": RequestedFile, "ErrorCode": 404})
        
        db_conn.execute(sqlalchemy.text(f"INSERT INTO Requests (Country, Client_IP, TimeStamp, RequestedFile, Gender, Age, Income, isBanned) VALUES ('{country}', '{Client_IP}', '{TimeStamp}', '{RequestedFile}', '{Gender}', '{Age}', '{Income}', {isBanned})"))
        db_conn.commit()

    return

def write_entry(message):
    logging_client = logging.Client()
    logger = logging_client.logger(logger_name)
    logger.log_text(message, severity='ERROR')

@app.route('/<path:filename>', methods=['GET', 'PUT', 'POST', 'DELETE', 'HEAD', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'])
def file_server(filename):
    banned_countries = ["North Korea", "Iran", "Cuba", "Myanmar", "Iraq", "Libya", "Sudan", "Zimbabwe", "Syria"]
    country = request.headers.get('X-country')
    client_ip = request.headers.get('X-client-IP')
    gender = request.headers.get('X-gender')
    age = request.headers.get('X-age')
    income = request.headers.get('X-income')
    time = request.headers.get('X-time')
    filename = filename.rsplit('/', 1)[-1]

    # Check to see if the method is other than GET
    if request.method != 'GET':
        write_entry('Not Implemented')
        db_entry(
            method=request.method, 
            country=country, 
            Client_IP=client_ip, 
            TimeStamp=time, 
            RequestedFile=filename, 
            Gender=gender, 
            Age=age, 
            Income=income, 
            isBanned=1 if country in banned_countries else 0
        )
        return abort(501, 'Not Implemented')
    
    # Check to see if it's forbidden
    if country in banned_countries:
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project_ID, topic_name)
        message_data = 'Forbidden Request from {}'.format(country)
        future = publisher.publish(topic_path, message_data.encode('utf-8'))

        db_entry(
            method=request.method, 
            country=country, 
            Client_IP=client_ip, 
            TimeStamp=time, 
            RequestedFile=filename, 
            Gender=gender, 
            Age=age, 
            Income=income, 
            isBanned=True
        )

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
        db_entry(
            method=request.method, 
            country=country, 
            Client_IP=client_ip, 
            TimeStamp=time, 
            RequestedFile=filename, 
            Gender=gender, 
            Age=age, 
            Income=income, 
            isBanned=1 if country in banned_countries else 0
        )
        return response
    else:
        write_entry('File not Found')
        db_entry(
            method=request.method, 
            country=country, 
            Client_IP=client_ip, 
            TimeStamp=time, 
            RequestedFile=filename, 
            Gender=gender, 
            Age=age, 
            Income=income, 
            isBanned=1 if country in banned_countries else 0,
            exists=False
        )
        return abort(404, 'File not Found')

# main driver function
if __name__ == '__main__':

 app.run(host='0.0.0.0', port=8080)