import hashlib
import json
import os


TRACK_FILE = "file_state.json"


def compute_file_hash(path):
    hasher = hashlib.md5()
    with open(path, "rb") as f:
        hasher.update(f.read())
    return hasher.hexdigest()


def has_file_changed(path):
    current_hash = compute_file_hash(path)

    if not os.path.exists(TRACK_FILE):
        return True

    with open(TRACK_FILE, "r") as f:
        data = json.load(f)

    stored_hash = data.get("hash")

    return current_hash != stored_hash


def update_file_hash(path):
    current_hash = compute_file_hash(path)

    with open(TRACK_FILE, "w") as f:
        json.dump({"hash": current_hash}, f)