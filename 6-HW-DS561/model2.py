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

query = "SELECT TimeStamp, Income FROM Requests"
data = pd.read_sql(query, con=conn)
connector.close()

# Preprocess the data: Convert categorical features
one_hot_encoded_data = pd.get_dummies(data, columns=['TimeStamp'])

X = one_hot_encoded_data.drop(columns=['Income'])
Y = one_hot_encoded_data['Income']

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

model = DecisionTreeClassifier()

model.fit(X_train, Y_train)

accuracy = model.score(X_test, Y_test)
print(f"Model accuracy: {accuracy}")