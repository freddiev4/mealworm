"""FastAPI entrypoint for deployment platforms (Railway, Modal, etc.)."""

from mealworm.api.main import app

__all__ = ["app"]
