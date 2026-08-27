#!/usr/bin/env python
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.main import create_app
from app.models import User

app = create_app()
with app.app_context():
    users = User.query.all()
    print(f"Total users in DB: {len(users)}")
    for u in users:
        print(f"  - {u.username} | hash: {u.password_hash[:20]}... | active: {u.is_active}")
        
        # Test password
        if u.check_password('Password@123'):
            print(f"    ✅ Password 'Password@123' is CORRECT")
        else:
            print(f"    ❌ Password 'Password@123' is WRONG")
