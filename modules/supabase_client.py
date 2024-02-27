import os
import io
import supabase
import config as cfg


class SupaClient:
    def __init__(self, bucket=None):
        self.client = supabase.create_client(cfg.SUPABASE_URL,
                                             cfg.SUPABASE_KEY)
        self.bucket = bucket or cfg.SUPABASE_BUCKET_NAME

    def _list_bucket(self) -> list:
        return self.client.storage.from_(self.bucket).list()

    def does_files_exist(self, file) -> bool:
        item_names = [x["name"] for x in self._list_bucket()]
        return True if file in item_names else False

    def upload(self, bytes: io.BytesIO, destination):
        if self.does_files_exist(destination):
            raise ValueError("File already exists")
        try:
            self.client.storage.from_(self.bucket).upload(destination, bytes)
            return True, None
        except Exception as e:
            return False, e

    def download(self, source: str) -> io.BytesIO:
        if self.does_files_exist(source):
            return self.client.storage.from_(self.bucket).download(source)
        else:
            raise ValueError("File does not exist")

    def delete_file(self, source: str) -> bool:
        try:
            self.client.storage.from_(self.bucket).remove(source)
            return True, None
        except Exception as e:
            return False, e

    def delete_all_files(self):
        for item in self._list_bucket():
            self.delete_file(item["name"])
