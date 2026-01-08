"""Authentication Endpoints"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class TokenRequest(BaseModel):
    """토큰 발급 요청"""
    device_id: str


class TokenResponse(BaseModel):
    """토큰 응답"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    """토큰 갱신 요청"""
    refresh_token: str


@router.post("/token", response_model=TokenResponse)
async def create_token(request: TokenRequest):
    """JWT 토큰 발급"""
    # TODO: 실제 JWT 토큰 생성 로직 구현
    return TokenResponse(
        access_token="access_token_placeholder",
        refresh_token="refresh_token_placeholder",
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: RefreshRequest):
    """토큰 갱신"""
    # TODO: 실제 토큰 갱신 로직 구현
    return TokenResponse(
        access_token="new_access_token_placeholder",
        refresh_token="new_refresh_token_placeholder",
    )
