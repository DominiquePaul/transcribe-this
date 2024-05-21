import io
import os
from pathlib import Path
import tempfile
import streamlit as st
from datetime import datetime

# pip install pydub streamlit supabase

# from pydub import AudioSegment

from modules.whispa import split_mp3, transcribe_mp3_group
# from modules.supabase_client import SupaClient

# supa_client = SupaClient()


def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True


if check_password():
    st.title('Transcribe any .mp3 file')
    uploaded_file = st.file_uploader("Upload your audio file here", type="mp3")
    if uploaded_file is not None:
        # Format the datetime as a filename-friendly string
        filename_datetime_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"file_{filename_datetime_str}"
        # supa_client.upload(uploaded_file.read(), filename + ".mp3")

        with tempfile.TemporaryDirectory() as temp_dir:
            mp3_file_path = os.path.join(temp_dir, filename + ".mp3")
            with open(mp3_file_path, "wb") as f:
                f.write(uploaded_file.getvalue())

            num_parts, path_template = split_mp3(mp3_file_path, filename, duration=5 * 60 *
                                                 1000, folder_path=Path(temp_dir))  # Split every 5 minutes

            transcript = transcribe_mp3_group(path_template, num_parts)
        st.markdown(transcript)
