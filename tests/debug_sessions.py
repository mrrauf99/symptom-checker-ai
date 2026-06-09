#!/usr/bin/env python
"""Debug script to check sessions in the database"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.database.collections import chat_sessions_collection, users_collection
from pprint import pprint

print("=" * 60)
print("ALL SESSIONS IN DATABASE")
print("=" * 60)
sessions = list(chat_sessions_collection.find().limit(10))
for session in sessions:
    print(f"\nSession ID: {session['_id']}")
    print(f"User ID: {session.get('user_id')}")
    print(f"Title: {session.get('title')}")
    print(f"Status: {session.get('status')}")
    print(f"Created: {session.get('created_at')}")

print("\n" + "=" * 60)
print("ALL USERS IN DATABASE")
print("=" * 60)
users = list(users_collection.find().limit(10))
for user in users:
    print(f"\nUser ID: {user['_id']}")
    print(f"Email: {user.get('email')}")
    print(f"Name: {user.get('name')}")
    print(f"Created: {user.get('created_at')}")

print("\n" + "=" * 60)
print("Checking session/user ID matches")
print("=" * 60)
for session in sessions[:3]:
    session_user_id = session.get('user_id')
    user = users_collection.find_one({"_id": eval(session_user_id) if session_user_id.startswith('ObjectId') else session_user_id})
    if user:
        print(f"✓ Session {session['_id']} has valid user")
    else:
        print(f"✗ Session {session['_id']} references missing user: {session_user_id}")
