from fastapi import APIRouter, Depends, Request, FastAPI
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from src.schemas.users import User
from src.services.auth import get_current_user

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.add_middleware(SlowAPIMiddleware)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=User)
@limiter.limit("5/minute")
async def me(request: Request, user: User = Depends(get_current_user)):
    return user


app.include_router(router)
