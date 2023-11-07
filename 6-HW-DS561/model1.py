from google.cloud.sql.connector import Connector
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

INSTANCE_CONNECTION_NAME = f"{'ds-561-398918'}:{'us-east1'}:{'hw5-database'}"
print(f"Your instance connection name is: {INSTANCE_CONNECTION_NAME}")
DB_USER = "mainUser"
DB_PASS = "Ryozo2011"
DB_NAME = "file_store"

connector = Connector()

conn = connector.connect(
    INSTANCE_CONNECTION_NAME,
    "pymysql",
    user=DB_USER,
    password=DB_PASS,
    db=DB_NAME
)

query = "SELECT Client_IP, Country FROM Requests"

df = pd.read_sql(query, con=conn)
connector.close()

df['Client_IP'] = df['Client_IP'].apply(lambda ip: list(map(int, ip.split('.'))))

# Split data into features and target
X = df['Client_IP'].to_list()
Y = df['Country']

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Train a decision tree classifier
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Evaluate the model on the testing data
accuracy = model.score(X_test, y_test)
print(f"Model accuracy: {accuracy}")
