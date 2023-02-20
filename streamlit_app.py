"""Firestore project: chaos_prediction_leaderboard"""
import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json
import pandas as pd
import datetime

@st.cache_resource
def connect_to_db():
    """Connect to firestore database and return database object."""
    print("db connection made")
    key_dict = json.loads(st.secrets["textkey"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds, project="chaos-prediction-leaderboard")
    return db


LEADERBOARD_STR = "results"

# get db connection:
db = connect_to_db()

# Add entry:
with st.sidebar:
    st.header("Add entry:")
    with st.form(key="entry"):
        name = st.text_input("Name")
        valid_time = st.number_input("Valid time")
        time = datetime.datetime.now()

        ID = name + " " + str(time)
        data_to_add = {"name": name,
                       "date": time,
                       "valid time": valid_time}
        submitted = st.form_submit_button("Submit")
        if submitted:
            # Check arguments
            # ...

            # submit to database
            db.collection(LEADERBOARD_STR).document(ID).set(data_to_add)



# show leaderboard:
results_ref = db.collection(LEADERBOARD_STR)
docs = results_ref.stream()
items = list(map(lambda x: x.to_dict(), docs))
df = pd.DataFrame(items)
df = df[["name", "date", "valid time"]]
# df["date"] = df["date"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["date"] = df["date"].dt.strftime("%d-%m-%Y %H:%M")
df.sort_values(by="valid time", inplace=True)
st.header("Leaderboard")
st.dataframe(df)



