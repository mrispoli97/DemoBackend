import pickle as pkl
import json
from datetime import datetime
import uuid


def load_pickle(filepath):
    with open(filepath, 'rb') as handle:
        data = pkl.load(handle)
    return data


def read_binary(filepath):
    with open(filepath, 'rb') as f:
        bytes = f.read()
    return bytes


def load_json(filepath):
    print(filepath)
    with open(filepath, encoding='utf-8', mode='r') as f:
        data = json.load(f)
    return data


def get_percentage(current_step, num_steps):
    return current_step / num_steps * 100 if num_steps > 0 else 100


def get_time():
    # datetime object containing current date and time
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y-%H_%M_%S")
    return dt_string


def get_random_id():
    return str(uuid.uuid4())
