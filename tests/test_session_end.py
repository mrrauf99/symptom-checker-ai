#!/usr/bin/env python
"""Test script to debug session end operation"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime
from backend.database.collections import chat_sessions_collection
from backend.services.session_service import create_session, end_session
from bson.objectid import ObjectId

# Test user
test_user_id = "test_user_123"

# Create a test session
print("Creating test session...")
session_id = create_session(test_user_id, "Test Session")
print(f"Created session: {session_id}")

# Verify it was created
session = chat_sessions_collection.find_one({"_id": ObjectId(session_id)})
print(f"Session in DB: {session}")
print(f"Session user_id: {session.get('user_id') if session else 'NOT FOUND'}")
print(f"Session status: {session.get('status') if session else 'NOT FOUND'}")

# Try to end it
print("\nAttempting to end session...")
try:
    end_session(session_id, test_user_id)
    print("Successfully ended session")
except Exception as e:
    print(f"ERROR: {str(e)}")

# Verify it was updated
session = chat_sessions_collection.find_one({"_id": ObjectId(session_id)})
print(f"Session after end: {session}")
print(f"Session status: {session.get('status') if session else 'NOT FOUND'}")

# Clean up
chat_sessions_collection.delete_one({"_id": ObjectId(session_id)})
print("Cleaned up test session")
