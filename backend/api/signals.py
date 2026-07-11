# backend/api/signals.py
from fastapi import APIRouter, HTTPException
from typing import List

from models.signal import SignalType

router = APIRouter(prefix="/signals", tags=["signals"])

@router.get("/types", response_model=List[str])
async def get_signal_types():
    """Get all available signal types"""
    return [signal_type.value for signal_type in SignalType]