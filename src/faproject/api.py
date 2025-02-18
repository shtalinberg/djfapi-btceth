from datetime import datetime, timedelta, timezone
from typing import List, Optional

from asgiref.sync import sync_to_async
from bstore.models import Block, Provider
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.sessions.models import Session
from django.core.paginator import Paginator
from fastapi import APIRouter, Cookie, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from starlette.responses import JSONResponse

from .dependencies import ALGORITHM, SECRET_KEY, get_current_user
from .schemas import BlockList, BlockResponse, ProviderResponse, Token, UserCreate

# app = FastAPI()
router = APIRouter()
User = get_user_model()


def create_access_token(data: dict):
    """Generate JWT token"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=24)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/users/", response_model=dict)
async def create_user(user: UserCreate):
    if User.objects.filter(username=user.username).exists():
        raise HTTPException(status_code=400, detail="Username already registered")

    db_user = User.objects.create(
        username=user.username,
        password=make_password(user.password),
        email=user.email,
        is_active=user.is_active,
    )
    return {"message": "User created successfully"}


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = User.objects.filter(username=form_data.username).first()
    if not user or not check_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/token/session", response_model=dict)
async def get_token_from_session(sessionid: str = Cookie(None)):
    """Retrieve JWT token for authenticated Django users"""
    if not sessionid:
        raise HTTPException(status_code=401, detail="No session ID provided")

    from django.contrib.auth.models import User
    from django.contrib.sessions.models import Session

    try:
        session = await sync_to_async(Session.objects.get)(session_key=sessionid)
        user_id = session.get_decoded().get('_auth_user_id')
        user = await sync_to_async(User.objects.get)(pk=user_id)
    except (Session.DoesNotExist, User.DoesNotExist):
        raise HTTPException(status_code=401, detail="Invalid session")

    # Create JWT token for authenticated user
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@sync_to_async
def get_blocks(currency=None, provider=None):
    block_qs = Block.objects.all().select_related('currency', 'provider')

    if currency:
        block_qs = block_qs.filter(currency__name=currency)
    if provider:
        block_qs = block_qs.filter(provider__name=provider)

    return block_qs


@sync_to_async
def get_paginated_blocks(currency, provider, page, page_size):
    block_qs = Block.objects.all().select_related('currency', 'provider')

    if currency:
        block_qs = block_qs.filter(currency__name=currency)
    if provider:
        block_qs = block_qs.filter(provider__name=provider)

    paginator = Paginator(block_qs, page_size)
    page_obj = paginator.get_page(page)
    results = [
        BlockResponse(
            id=block.id,
            currency_name=block.currency.name,
            provider_name=block.provider.name,
            block_number=block.block_number,
            block_created_at=block.block_created_at,
            created_at=block.created_at,
        )
        for block in page_obj.object_list
    ]
    return paginator.count, results


@router.get("/blocks/", response_model=BlockList)
async def list_blocks(
    currency: Optional[str] = None,
    provider: Optional[str] = None,
    page: int = Query(1, gt=0),
    page_size: int = Query(10, gt=0, le=100),
    current_user: User = Depends(get_current_user),
):
    total, results = await get_paginated_blocks(currency, provider, page, page_size)

    return BlockList(total=total, page=page, page_size=page_size, results=results)


@sync_to_async
def get_block_by_id_sync(block_id):
    return (
        Block.objects.filter(id=block_id).select_related('currency', 'provider').first()
    )


@router.get("/blocks/{block_id}", response_model=BlockResponse)
async def get_block_by_id(block_id, current_user: User = Depends(get_current_user)):
    block = await get_block_by_id_sync(block_id)
    if not block:
        raise HTTPException(status_code=404, detail="Block not found")

    return BlockResponse(
        id=block.id,
        currency_name=block.currency.name,
        provider_name=block.provider.name,
        block_number=block.block_number,
        block_created_at=block.block_created_at,
        created_at=block.created_at,
    )


@router.get("/blocks/by-currency-number/", response_model=BlockResponse)
async def get_block_by_currency_number(
    currency: str, block_number: int, current_user: User = Depends(get_current_user)
):
    block = (
        Block.objects.filter(currency__name=currency, block_number=block_number)
        .select_related('currency', 'provider')
        .first()
    )

    if not block:
        raise HTTPException(status_code=404, detail="Block not found")

    return BlockResponse(
        id=block.id,
        currency_name=block.currency.name,
        provider_name=block.provider.name,
        block_number=block.block_number,
        block_created_at=block.block_created_at,
        stored_at=block.stored_at,
    )


@router.get("/providers/", response_model=List[ProviderResponse])
async def list_providers(current_user: User = Depends(get_current_user)):
    providers = Provider.objects.all()
    return [ProviderResponse(id=p.id, name=p.name) for p in providers]
