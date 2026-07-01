"""API routes"""

from fastapi import APIRouter
from . import routes

router = APIRouter(prefix="/api")

from . import routes as api_routes
router.include_router(api_routes.health.router, tags=["health"])
router.include_router(api_routes.files.router, tags=["files"])
router.include_router(api_routes.analysis.router, tags=["analysis"])