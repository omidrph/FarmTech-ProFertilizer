# backend/app/security.py
"""امنیت و احراز هویت - JWT و هش کردن رمز با hashlib"""

from datetime import datetime, timedelta
import hashlib
import secrets
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import User
from app.schemas import TokenData

# ===== تنظیمات OAuth2 =====
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/auth/login")


# ============================================================
# توابع هش کردن و بررسی رمز عبور (با hashlib)
# ============================================================

def get_password_hash(password: str) -> str:
    """
    هش کردن رمز عبور با SHA-256 و نمک (salt)
    
    Args:
        password: رمز عبور خام
    
    Returns:
        str: رمز هش شده با فرمت salt:hash
    """
    # تولید نمک (salt) تصادفی
    salt = secrets.token_hex(16)
    # هش کردن رمز با نمک
    hash_obj = hashlib.sha256((salt + password).encode('utf-8'))
    hash_str = hash_obj.hexdigest()
    # برگرداندن salt:hash برای ذخیره
    return f"{salt}:{hash_str}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    بررسی رمز عبور با هش ذخیره شده
    
    Args:
        plain_password: رمز عبور خام
        hashed_password: هش ذخیره شده (به فرمت salt:hash)
    
    Returns:
        bool: آیا رمز عبور صحیح است
    """
    try:
        salt, stored_hash = hashed_password.split(':')
        hash_obj = hashlib.sha256((salt + plain_password).encode('utf-8'))
        computed_hash = hash_obj.hexdigest()
        return computed_hash == stored_hash
    except (ValueError, AttributeError):
        return False


# ============================================================
# توابع JWT
# ============================================================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    ایجاد توکن JWT
    
    Args:
        data: دیتای مورد نظر برای ذخیره در توکن
        expires_delta: زمان انقضای توکن
    
    Returns:
        str: توکن JWT
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt


def decode_access_token(token: str) -> Optional[TokenData]:
    """
    رمزگشایی توکن JWT
    
    Args:
        token: توکن JWT
    
    Returns:
        TokenData: دیتای توکن یا None در صورت خطا
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        phone_number: str = payload.get("phone")
        
        if user_id is None:
            return None
        
        return TokenData(user_id=user_id, phone_number=phone_number)
    
    except JWTError:
        return None


# ============================================================
# توابع دریافت کاربر فعلی
# ============================================================

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    دریافت کاربر فعلی از توکن JWT
    
    Args:
        token: توکن JWT
        db: Session دیتابیس
    
    Returns:
        User: کاربر فعلی
    
    Raises:
        HTTPException: اگر توکن نامعتبر باشد یا کاربر پیدا نشود
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="مشکل در اعتبارسنجی",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = decode_access_token(token)
    
    if token_data is None:
        raise credentials_exception
    
    if token_data.user_id is None:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == token_data.user_id).first()
    
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="حساب کاربری غیرفعال است"
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    دریافت کاربر فعال فعلی
    
    Args:
        current_user: کاربر فعلی
    
    Returns:
        User: کاربر فعال
    
    Raises:
        HTTPException: اگر کاربر غیرفعال باشد
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="حساب کاربری غیرفعال است"
        )
    return current_user