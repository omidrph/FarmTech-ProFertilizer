# backend/app/routes/auth.py
"""مسیرهای احراز هویت (Authentication)"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
import logging
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserLogin, UserResponse, Token
import app.crud as crud
from app.security import (
    create_session_token,
    delete_session,
    get_current_user,
    get_password_hash,
    verify_password
)

# ===== تنظیمات Logger =====
logger = logging.getLogger(__name__)

# ===== ایجاد Router =====
auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

# ============================================================
# مسیرهای احراز هویت
# ============================================================

@auth_router.post("/register", response_model=UserResponse)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """ثبت‌نام کاربر جدید"""
    try:
        existing_user = crud.get_user_by_phone(db, user_data.phone_number)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="این شماره تلفن قبلاً ثبت شده است"
            )
        user = crud.create_user(db, user_data)
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in register: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در ثبت‌نام: {str(e)}"
        )

@auth_router.post("/login", response_model=Token)
def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """ورود کاربر و دریافت توکن تصادفی"""
    try:
        user = crud.get_user_by_phone(db, login_data.phone_number)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="شماره تلفن یا رمز عبور اشتباه است"
            )
        if not verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="شماره تلفن یا رمز عبور اشتباه است"
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="حساب کاربری غیرفعال است"
            )
        access_token = create_session_token(user.id, db, expires_in_hours=24)
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 86400
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در ورود: {str(e)}"
        )

@auth_router.post("/logout")
def logout(
    request: Request,
    db: Session = Depends(get_db)
):
    """خروج از حساب (غیرفعال کردن توکن)"""
    try:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:]
            if delete_session(token, db):
                return {"message": "خروج با موفقیت انجام شد", "success": True}
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="توکن پیدا نشد"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in logout: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در خروج: {str(e)}"
        )

@auth_router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user)
):
    """دریافت اطلاعات کاربر فعلی"""
    try:
        return current_user
    except Exception as e:
        logger.error(f"Error in get_me: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در دریافت اطلاعات کاربر: {str(e)}"
        )

@auth_router.get("/test")
def test_auth(
    current_user: User = Depends(get_current_user)
):
    """تست احراز هویت"""
    try:
        return {
            "message": "✅ احراز هویت موفق",
            "user": {
                "id": current_user.id,
                "phone": current_user.phone_number,
                "full_name": current_user.full_name
            }
        }
    except Exception as e:
        logger.error(f"Error in test_auth: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در تست احراز هویت: {str(e)}"
        )

# ============================================================
# 🆕 تغییر رمز عبور
# ============================================================
@auth_router.post("/change-password")
def change_password(
    password_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """🆕 تغییر رمز عبور کاربر"""
    try:
        current_password = password_data.get('current_password')
        new_password = password_data.get('new_password')
        
        if not current_password or not new_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="رمز عبور فعلی و جدید الزامی است"
            )
        
        if len(new_password) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="رمز عبور جدید باید حداقل ۶ کاراکتر باشد"
            )
        
        # بررسی رمز فعلی
        if not verify_password(current_password, current_user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="رمز عبور فعلی اشتباه است"
            )
        
        # به‌روزرسانی رمز عبور
        current_user.password_hash = get_password_hash(new_password)
        db.commit()
        
        logger.info(f"✅ رمز عبور کاربر {current_user.id} تغییر کرد")
        
        return {
            "message": "رمز عبور با موفقیت تغییر کرد",
            "success": True
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in change_password: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در تغییر رمز عبور: {str(e)}"
        )