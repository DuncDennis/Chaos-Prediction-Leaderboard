"""Firestore project: chaos_prediction_leaderboard"""
import streamlit as st
import numpy as np
import datetime
import pytz

import src.streamlit_elements.database as database

if __name__ == "__main__":
    st.set_page_config("Chaos Prediction Leaderboard", page_icon="🎯")

    # get db connection:
    db = database.connect_to_db()

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
                database.write_to_leaderboard(db, ID, data_to_add)


    st.header("Leaderboard")
    if st.button("🔄"):
        database.clear_cache_data()

    # Show leaderboard
    df = database.read_leaderboard(db)
    st.dataframe(df)
