import os
import io
import pytest
from modules.supabase_client import SupaClient
import toml

toml_data = toml.load(".streamlit/secrets.toml")
os.environ["SUPABASE_URL"] = toml_data["SUPABASE_URL"]
os.environ["SUPABASE_KEY"] = toml_data["SUPABASE_KEY"]
os.environ["SUPABASE_BUCKET_NAME"] = toml_data["SUPABASE_BUCKET_NAME"]


@pytest.fixture
def client():
    return SupaClient()


class TestSupaClient:

    def test_upload(self, client):
        example_file = "sl_app_data/file_2023-07-18_13-45-47.mp3"
        with open(example_file, "rb") as audio_file:
            res, _ = client.upload(audio_file.read(), "example_file.mp3")
        assert res

    def test_download(self, client):
        res = client.download("example_file.mp3")
        assert isinstance(res, bytes)

    def test_list_bucket(self, client):
        res = client._list_bucket()
        assert isinstance(res, list)
        assert len(res) > 0

    def test_does_files_exist(self, client):
        res = client.does_files_exist("example_file.mp3")
        assert res

    def test_delete_file(self, client):
        res, _ = client.delete_file("example_file.mp3")
        assert res
