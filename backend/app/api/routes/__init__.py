"""API routes module"""

from fastapi import APIRouter

router = APIRouter(prefix="/api")

from . import health, files, analysis, workflow

router.include_router(health.router, tags=["health"])
router.include_router(files.router, tags=["files"])
router.include_router(analysis.router, tags=["analysis"])
router.include_router(workflow.router, tags=["workflow"])
