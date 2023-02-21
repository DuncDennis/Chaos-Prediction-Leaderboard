"""Firestore project: chaos_prediction_leaderboard"""
import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json
import pandas as pd
import numpy as np
import datetime
import pytz

@st.cache_resource
def connect_to_db():
    """Connect to firestore database and return database object."""
    print("db connection made")
    key_dict = json.loads(st.secrets["textkey"])
    creds = service_account.Credentials.from_service_account_info(key_dict)  # no read/write
    db = firestore.Client(credentials=creds, project="chaos-prediction-leaderboard")  #
    return db

def clear_cache_data():
    """Clear st.cache_data to reload leaderboard."""
    print("cache cleared")
    st.cache_data.clear()

@st.cache_data
def read_leaderboard():
    """Read leaderboard from database."""
    print("db read out made")
    results_ref = db.collection(LEADERBOARD_STR)
    docs = results_ref.stream()
    items = list(map(lambda x: x.to_dict(), docs))
    df = pd.DataFrame(items)
    df = df[["name", "date", "valid time"]]
    df["date"] = df["date"].dt.tz_convert("Europe/Berlin")
    df["date"] = df["date"].dt.strftime("%d-%m-%Y %H:%M")
    df.sort_values(by="valid time", inplace=True)
    return df

LEADERBOARD_STR = "results"

if __name__ == "__main__":
    st.set_page_config("Chaos Prediction Leaderboard", page_icon="🎯")

    # get db connection:
    db = connect_to_db()

    # Add entry:
    with st.sidebar:

        # Data upload:
        st.header("Upload data")
        true_data = st.file_uploader("True",
                                     type=["npy"],
                                     accept_multiple_files=False)
        if true_data is not None:
            true_data = np.load(true_data)

        pred_data = st.file_uploader("Prediction",
                                     type=["npy"],
                                     accept_multiple_files=False)
        if pred_data is not None:
            pred_data = np.load(pred_data)
        if pred_data is not None and true_data is not None:
            st.success("True and Pred data uploaded successfully.")

        # Add entry:
        st.header("Add entry:")
        with st.form(key="entry"):
            name = st.text_input("Name")
            valid_time = st.number_input("Valid time")
            time = datetime.datetime.now(pytz.timezone("Europe/Berlin"))
            ID = name + " " + str(time)
            data_to_add = {"name": name,
                           "date": time,
                           "valid time": valid_time}
            submitted = st.form_submit_button("Submit")
            if submitted:
                # Check arguments
                # ...

                # submit to database
                db.collection(LEADERBOARD_STR).document(ID).set(data_to_add)  # WRITE DATA

                # Clear cache to reload Leaderboard:
                clear_cache_data()

    # Show leaderboard
    df = read_leaderboard()

    st.header("Leaderboard")
    if st.button("🔄"):
        clear_cache_data()
    st.dataframe(df)
