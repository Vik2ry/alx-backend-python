#!/usr/bin/python3
from itertools import islice
import importlib.util

# Dynamic import of 0-stream_users.py
spec = importlib.util.spec_from_file_location("stream_users", "./0-stream_users.py")
stream_users_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stream_users_module)
stream_users = stream_users_module.stream_users

# Use the generator
for user in islice(stream_users(), 6):
    print(user)
