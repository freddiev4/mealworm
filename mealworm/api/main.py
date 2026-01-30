import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from mealworm.api.routes.v1_router import v1_router
from mealworm.api.settings import api_settings

logger = logging.getLogger(__name__)


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Catch unhandled exceptions so we always return a response from our app.
    That way CORS middleware adds headers (fixes "CORS header missing" on 500).
    Log the real error so you can see it in Vercel function logs.
    """
    logger.exception("Unhandled exception: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


def create_app() -> FastAPI:
    """
    Create a FastAPI App
    """

    # Create FastAPI App
    app: FastAPI = FastAPI(
        title=api_settings.title,
        version=api_settings.version,
        docs_url="/docs" if api_settings.docs_enabled else None,
        redoc_url="/redoc" if api_settings.docs_enabled else None,
        openapi_url="/openapi.json" if api_settings.docs_enabled else None,
    )

    # Global handler: any unhandled exception returns JSON 500 from our app (CORS gets applied)
    app.add_exception_handler(Exception, global_exception_handler)

    # Add v1 router
    app.include_router(v1_router)

    # Add Middlewares
    app.add_middleware(
        CORSMiddleware,
        allow_origins=api_settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


# Create a FastAPI app
app = create_app()
