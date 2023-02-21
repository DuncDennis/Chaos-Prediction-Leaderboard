"""Functions to handle the database."""
import pandas as pd
import json
import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account

@st.cache_resource
def connect_to_db():
    """Connect to firestore database and return database object."""
    print("db connection made")
    key_dict = json.loads(st.secrets["textkey"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds, project="chaos-prediction-leaderboard")
    return db


def clear_cache_data():
    """Clear st.cache_data to reload leaderboard."""
    print("cache cleared")
    st.cache_data.clear()


@st.cache_data
def read_leaderboard(_db):
    """Read leaderboard from database and return pandas df."""
    print("db read out made")
    results_ref = _db.collection("results")
    docs = results_ref.stream()
    items = list(map(lambda x: x.to_dict(), docs))
    df = pd.DataFrame(items)
    df = df[["name", "date", "valid time"]]
    df["date"] = df["date"].dt.tz_convert("Europe/Berlin")
    df["date"] = df["date"].dt.strftime("%d-%m-%Y %H:%M")
    df.sort_values(by="valid time", inplace=True)
    return df


def write_to_leaderboard(db, ID, data_to_add):
    """Write to database. """
    print("write to db")
    # submit to database
    db.collection("results").document(ID).set(data_to_add)  # WRITE DATA

    # Clear cache to reload Leaderboard:
    clear_cache_data()
