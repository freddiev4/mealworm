from typing import List, Optional

from pydantic import Field, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings


class ApiSettings(BaseSettings):
    """Api settings that are set using environment variables."""

    title: str = "mealworm-api"
    version: str = "1.0.0"

    # Set to False to disable docs at /docs and /redoc
    docs_enabled: bool = True

    # CORS allowed origins. Set CORS_ORIGIN_LIST (comma-separated) in env to add
    # more origins (e.g. Vercel frontend URL, preview deployments, custom domain).
    cors_origin_list: Optional[List[str]] = Field(None, validate_default=True)

    @field_validator("cors_origin_list", mode="before")
    def set_cors_origin_list(cls, cors_origin_list, info: FieldValidationInfo):
        # Start empty; we'll merge env-provided origins with built-in defaults.
        valid_cors: List[str] = []

        # Parse CORS_ORIGIN_LIST from env. Pydantic may pass a string (comma-separated)
        # or a list (e.g. from JSON). Handle both so env vars work reliably.
        if cors_origin_list is not None:
            if isinstance(cors_origin_list, str):
                valid_cors = [o.strip() for o in cors_origin_list.split(",") if o.strip()]
            elif isinstance(cors_origin_list, list):
                valid_cors = list(cors_origin_list)

        # Built-in origins: localhost, Agno playground, and production Vercel frontend.
        # These are always allowed; env additions are merged in (no duplicates).
        defaults = [
            "https://app.agno.com",
            "http://localhost",
            "http://localhost:3000",
            "https://mealworm-zeta.vercel.app",
        ]
        # Append each default only if not already present (avoids duplicates).
        seen = set(valid_cors)
        for o in defaults:
            if o not in seen:
                valid_cors.append(o)
                seen.add(o)

        return valid_cors


# Create ApiSettings object
api_settings = ApiSettings()
