import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token

router = APIRouter(prefix="/auth", tags=["Auth"])
security = HTTPBearer()


def _normalize_optional(value: str | None) -> str | None:
    if not value:
        return None
    stripped = value.strip()
    return stripped if stripped else None


def _conflict_detail_from_error(err: IntegrityError) -> str:
    msg = str(err.orig or "")
    if "uq_users_email" in msg:
        return "Użytkownik o tym adresie email już istnieje"
    if "uq_users_nickname" in msg:
        return "Ten nick jest już zajęty"
    if "uq_users_phone" in msg:
        return "Ten numer telefonu jest już przypisany do innego konta"
    return "Użytkownik o podanych danych już istnieje"


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    nickname = _normalize_optional(user_in.nickname)
    phone_number = _normalize_optional(user_in.phone_number)

    conditions = [User.email == user_in.email]
    if nickname is not None:
        conditions.append(User.nickname == nickname)
    if phone_number is not None:
        conditions.append(User.phone_number == phone_number)

    stmt = select(User).where(User.deleted_at.is_(None), or_(*conditions))
    result = await db.execute(stmt)
    existing_user = result.scalars().first()

    if existing_user is not None:
        if existing_user.email == user_in.email:
            raise HTTPException(status_code=400, detail="Użytkownik o tym adresie email już istnieje")
        if nickname is not None and existing_user.nickname == nickname:
            raise HTTPException(status_code=400, detail="Ten nick jest już zajęty")
        if phone_number is not None and existing_user.phone_number == phone_number:
            raise HTTPException(status_code=400, detail="Ten numer telefonu jest już przypisany do innego konta")

    hashed_pass = hash_password(user_in.password)
    new_user = User(
        nickname=nickname,
        name=_normalize_optional(user_in.name),
        surname=_normalize_optional(user_in.surname),
        email=user_in.email,
        phone_number=phone_number,
        hash_password=hashed_pass,
    )
    db.add(new_user)
    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=_conflict_detail_from_error(exc))

    await db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
async def login(login_data: UserLogin, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(
        User.deleted_at.is_(None),
        or_(User.email == login_data.credential, User.nickname == login_data.credential),
    )
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if user is None or not user.hash_password or not verify_password(login_data.password, user.hash_password):
        raise HTTPException(status_code=401, detail="Nieprawidłowy login lub hasło")
    if user.account_status == "banned":
        raise HTTPException(status_code=403, detail="Konto zostało zablokowane")

    token = create_access_token(data={"sub": str(user.id), "role": user.user_role})
    return Token(access_token=token, token_type="bearer")


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Nieprawidłowy lub wygasły token")

    try:
        user_id = uuid.UUID(payload["sub"])
    except (ValueError, TypeError):
        raise HTTPException(status_code=401, detail="Nieprawidłowy identyfikator użytkownika w tokenie")

    user = await db.get(User, user_id)
    if not user or user.deleted_at is not None:
        raise HTTPException(status_code=401, detail="Użytkownik nie istnieje")
    return user


@router.get("/me", response_model=UserResponse)
async def info(current_user: User = Depends(get_current_user)):
    return current_user
