"""Firestore project: chaos_prediction_leaderboard"""
import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json
import pandas as pd
import datetime

LEADERBOARD_STR = "results"

# get db connection:
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="chaos-prediction-leaderboard")

# Add entry:
with st.sidebar:
    st.header("Add entry:")
    name = st.text_input("Name")
    valid_time = st.number_input("Valid time")
    time = datetime.datetime.now()
    ID = name + " " + str(time)
    data_to_add = {"name": name,
                   "date": time,
                   "valid time": valid_time}

    if st.button("submit"):
        db.collection(LEADERBOARD_STR).document(ID).set(data_to_add)

# show leaderboard:
results_ref = db.collection(LEADERBOARD_STR)
docs = results_ref.stream()
items = list(map(lambda x: x.to_dict(), docs))
df = pd.DataFrame(items)
df = df[["name", "date", "valid time"]]
st.header("Leaderboard")
st.dataframe(df)



