# backend/api/__init__.py
from .companies import router as companies_router
from .leads import router as leads_router
from .signals import router as signals_router
from .research import router as research_router

__all__ = ["companies_router", "leads_router", "signals_router", "research_router"]