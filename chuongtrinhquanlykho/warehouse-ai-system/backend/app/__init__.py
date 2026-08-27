"""
app/__init__.py — Package init cho app
========================================
Expose create_app để Flask CLI và tests có thể import.

Khi chạy: flask --app app run
Flask sẽ tìm create_app() trong app/__init__.py hoặc app/main.py
"""

def create_app(*args, **kwargs):
	"""Nạp application factory khi được gọi để tránh import vòng khi chạy -m."""
	from app.main import create_app as application_factory

	return application_factory(*args, **kwargs)

__all__ = ["create_app"]
