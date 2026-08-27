#!/usr/bin/env python
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.main import create_app
from app.models import User

app = create_app()
with app.app_context():
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
    print(f"Database URI in Flask: {db_uri}")
    
    users = User.query.all()
    print(f"Total users: {len(users)}")
    for u in users:
        print(f"  - {u.username}")
