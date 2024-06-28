import hmac
import os
import tempfile
import streamlit as st
from datetime import datetime

from modules.transcription import transcribe_mp3_file

# from modules.transcription import split_mp3, transcribe_mp3_group
# pip install pydub streamlit supabase
# from pydub import AudioSegment
# from modules.supabase_client import SupaClient
# supa_client = SupaClient()

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["PASSWORD"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


if check_password():
    st.title('Transcribe any .mp3 file')
    language = st.selectbox("Select the language of the audio file", ["English", "German"])
    st.caption("Transcription is faster if you don't identify speakers.")
    identify_speakers = st.checkbox("Identify speakers", value=False)
    language_code = "en" if language == "English" else "de"
    uploaded_file = st.file_uploader("Upload your audio file here", type="mp3")
    if uploaded_file is not None:
        # Format the datetime as a filename-friendly string
        filename_datetime_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"file_{filename_datetime_str}"
        # supa_client.upload(uploaded_file.read(), filename + ".mp3")
        st.subheader("Transcript")
        with tempfile.TemporaryDirectory() as temp_dir:
            mp3_file_path = os.path.join(temp_dir, filename + ".mp3")
            with open(mp3_file_path, "wb") as f:
                f.write(uploaded_file.getvalue())

            # num_parts, path_template = split_mp3(mp3_file_path, filename, duration=5 * 60 *
            #                                      1000, folder_path=Path(temp_dir))  # Split every 5 minutes

            transcript = transcribe_mp3_file(mp3_file_path, identify_speakers, language_code=language_code)
        st.markdown(transcript)
