# backend/app/routes/auth.py
"""مسیرهای احراز هویت (Authentication) - نسخه امنیتی کامل"""

from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.orm import Session
import logging
from datetime import datetime, timedelta

from app.config import settings
from app.database import get_db
from app.models import User, PasswordResetToken, SecurityLog
from app.schemas import (
    UserCreate, UserLogin, UserResponse, Token,
    ChangePasswordRequest, ChangePasswordResponse,
    ForgotPasswordRequest, ForgotPasswordResponse,
    ResetPasswordRequest, ResetPasswordResponse,
    Enable2FARequest, Enable2FAResponse,
    Verify2FARequest, Verify2FAResponse,
    Disable2FARequest, Disable2FAResponse
)
import app.crud as crud
from app.security import (
    create_session_token,
    delete_session,
    get_current_user,
    get_password_hash,
    verify_password,
    validate_password_strength,
    increment_failed_attempts,
    reset_failed_attempts,
    check_account_lock,
    generate_totp_secret,
    generate_backup_codes,
    verify_totp,
    verify_backup_code,
    delete_user_sessions
)
from app.security_logger import log_security_event
from app.sms import sms_provider, generate_verification_code, generate_reset_token

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
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    ثبت‌نام کاربر جدید با اعتبارسنجی امنیتی
    """
    try:
        # دریافت IP و User-Agent
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("User-Agent", "unknown")
        
        # بررسی وجود کاربر
        existing_user = crud.get_user_by_phone(db, user_data.phone_number)
        if existing_user:
            # ثبت رویداد امنیتی
            log_security_event(
                db=db,
                event_type="REGISTER_FAILED",
                ip_address=client_ip,
                user_agent=user_agent,
                endpoint="/auth/register",
                method="POST",
                details={"phone": user_data.phone_number, "reason": "User already exists"},
                severity="WARNING"
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="این شماره تلفن قبلاً ثبت شده است"
            )
        
        # اعتبارسنجی قدرت رمز عبور
        is_valid, password_message = validate_password_strength(user_data.password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=password_message
            )
        
        # ایجاد کاربر
        user = crud.create_user(db, user_data)
        
        # ثبت رویداد امنیتی
        log_security_event(
            db=db,
            event_type="REGISTER_SUCCESS",
            user_id=user.id,
            ip_address=client_ip,
            user_agent=user_agent,
            endpoint="/auth/register",
            method="POST",
            details={"phone": user.phone_number}
        )
        
        # ایجاد نشست
        access_token = create_session_token(
            user_id=user.id,
            db=db,
            ip_address=client_ip,
            user_agent=user_agent
        )
        
        # تنظیم Cookie
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=settings.SESSION_EXPIRY_HOURS * 3600,
            path="/"
        )
        
        logger.info(f"User registered: {user.id} - {user.phone_number}")
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
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    ورود کاربر و دریافت توکن تصادفی - با قفل حساب و Rate Limiting
    """
    try:
        # دریافت IP و User-Agent
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("User-Agent", "unknown")
        
        # پیدا کردن کاربر
        user = crud.get_user_by_phone(db, login_data.phone_number)
        
        # اگر کاربر وجود نداشت
        if not user:
            # ثبت رویداد امنیتی
            log_security_event(
                db=db,
                event_type="LOGIN_FAILED",
                ip_address=client_ip,
                user_agent=user_agent,
                endpoint="/auth/login",
                method="POST",
                details={"phone": login_data.phone_number, "reason": "User not found"},
                severity="WARNING"
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="شماره تلفن یا رمز عبور اشتباه است"
            )
        
        # بررسی قفل حساب
        is_locked, lock_message = check_account_lock(user)
        if is_locked:
            # ثبت رویداد امنیتی
            log_security_event(
                db=db,
                event_type="LOGIN_BLOCKED",
                user_id=user.id,
                ip_address=client_ip,
                user_agent=user_agent,
                endpoint="/auth/login",
                method="POST",
                details={"phone": user.phone_number, "locked_until": user.locked_until.isoformat()},
                severity="ERROR"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=lock_message
            )
        
        # بررسی رمز عبور
        if not verify_password(login_data.password, user.password_hash):
            # افزایش تعداد تلاش‌های ناموفق
            increment_failed_attempts(user, db)
            
            # ثبت رویداد امنیتی
            log_security_event(
                db=db,
                event_type="LOGIN_FAILED",
                user_id=user.id,
                ip_address=client_ip,
                user_agent=user_agent,
                endpoint="/auth/login",
                method="POST",
                details={
                    "phone": user.phone_number,
                    "failed_attempts": user.failed_attempts,
                    "reason": "Wrong password"
                },
                severity="WARNING"
            )
            
            # اگر حساب قفل شده است
            if user.is_locked:
                remaining = (user.locked_until - datetime.utcnow()).seconds // 60
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"حساب کاربری به دلیل {user.failed_attempts} تلاش ناموفق قفل شده است. {remaining} دقیقه دیگر تلاش کنید."
                )
            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="شماره تلفن یا رمز عبور اشتباه است"
            )
        
        # بررسی فعال بودن حساب
        if not user.is_active:
            # ثبت رویداد امنیتی
            log_security_event(
                db=db,
                event_type="LOGIN_BLOCKED",
                user_id=user.id,
                ip_address=client_ip,
                user_agent=user_agent,
                endpoint="/auth/login",
                method="POST",
                details={"phone": user.phone_number, "reason": "Account inactive"},
                severity="ERROR"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="حساب کاربری غیرفعال است"
            )
        
        # ورود موفق - بازنشانی تلاش‌های ناموفق
        reset_failed_attempts(user, db)
        
        # به‌روزرسانی اطلاعات آخرین ورود
        user.last_login = datetime.utcnow()
        user.last_ip = client_ip
        user.last_user_agent = user_agent
        db.commit()
        
        # ثبت رویداد امنیتی
        log_security_event(
            db=db,
            event_type="LOGIN_SUCCESS",
            user_id=user.id,
            ip_address=client_ip,
            user_agent=user_agent,
            endpoint="/auth/login",
            method="POST",
            details={"phone": user.phone_number}
        )
        
        # ایجاد نشست
        access_token = create_session_token(
            user_id=user.id,
            db=db,
            ip_address=client_ip,
            user_agent=user_agent
        )
        
        # تنظیم Cookie
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=settings.SESSION_EXPIRY_HOURS * 3600,
            path="/"
        )
        
        logger.info(f"User logged in: {user.id} - {user.phone_number}")
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.SESSION_EXPIRY_HOURS * 3600
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
    response: Response,
    db: Session = Depends(get_db)
):
    """
    خروج از حساب (غیرفعال کردن توکن)
    """
    try:
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("User-Agent", "unknown")
        
        # دریافت توکن از Cookie یا Header
        token = request.cookies.get("access_token")
        if not token:
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header[7:]
        
        if token:
            # پیدا کردن نشست برای لاگ
            from app.security import get_session_by_token
            session = get_session_by_token(token, db)
            user_id = session.user_id if session else None
            
            # حذف نشست
            if delete_session(token, db):
                # ثبت رویداد امنیتی
                log_security_event(
                    db=db,
                    event_type="LOGOUT",
                    user_id=user_id,
                    ip_address=client_ip,
                    user_agent=user_agent,
                    endpoint="/auth/logout",
                    method="POST"
                )
                logger.info(f"User logged out: {user_id}")
        
        # پاک کردن Cookie
        response.delete_cookie(
            key="access_token",
            path="/",
            secure=False,
            httponly=True,
            samesite="lax"
        )
        
        return {"message": "خروج با موفقیت انجام شد", "success": True}
        
    except Exception as e:
        logger.error(f"Error in logout: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در خروج: {str(e)}"
        )


# ============================================================
# 🔐 دریافت اطلاعات کاربر فعلی
# ============================================================

@auth_router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user)
):
    """
    دریافت اطلاعات کاربر فعلی
    """
    try:
        return current_user
    except Exception as e:
        logger.error(f"Error in get_me: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در دریافت اطلاعات کاربر: {str(e)}"
        )


# ============================================================
# 🔐 تغییر رمز عبور
# ============================================================

@auth_router.post("/change-password", response_model=ChangePasswordResponse)
def change_password(
    password_data: ChangePasswordRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    تغییر رمز عبور کاربر
    """
    try:
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("User-Agent", "unknown")
        
        # بررسی رمز فعلی
        if not verify_password(password_data.current_password, current_user.password_hash):
            # ثبت رویداد امنیتی
            log_security_event(
                db=db,
                event_type="PASSWORD_CHANGE_FAILED",
                user_id=current_user.id,
                ip_address=client_ip,
                user_agent=user_agent,
                endpoint="/auth/change-password",
                method="POST",
                details={"reason": "Wrong current password"},
                severity="WARNING"
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="رمز عبور فعلی اشتباه است"
            )
        
        # اعتبارسنجی رمز جدید
        is_valid, password_message = validate_password_strength(password_data.new_password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=password_message
            )
        
        # به‌روزرسانی رمز عبور
        current_user.password_hash = get_password_hash(password_data.new_password)
        db.commit()
        
        # غیرفعال کردن تمام نشست‌های قبلی (به جز نشست فعلی)
        delete_user_sessions(current_user.id, db)
        
        # ثبت رویداد امنیتی
        log_security_event(
            db=db,
            event_type="PASSWORD_CHANGE_SUCCESS",
            user_id=current_user.id,
            ip_address=client_ip,
            user_agent=user_agent,
            endpoint="/auth/change-password",
            method="POST"
        )
        
        logger.info(f"✅ رمز عبور کاربر {current_user.id} تغییر کرد")
        
        return {
            "message": "رمز عبور با موفقیت تغییر کرد. لطفاً دوباره وارد شوید.",
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


# ============================================================
# 🔐 فراموشی رمز عبور (با پیامک)
# ============================================================

@auth_router.post("/forgot-password", response_model=ForgotPasswordResponse)
def forgot_password(
    data: ForgotPasswordRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    درخواست فراموشی رمز عبور - ارسال کد پیامک
    """
    try:
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("User-Agent", "unknown")
        
        # پیدا کردن کاربر
        user = crud.get_user_by_phone(db, data.phone_number)
        if not user:
            # برای امنیت، پیام موفقیت نشان بده (حتی اگر کاربر وجود نداشته باشد)
            return {
                "message": "اگر این شماره در سیستم ثبت شده باشد، کد تأیید برای شما ارسال خواهد شد.",
                "success": True,
                "reset_id": None
            }
        
        # بررسی قفل حساب
        is_locked, _ = check_account_lock(user)
        if is_locked:
            # ثبت رویداد امنیتی
            log_security_event(
                db=db,
                event_type="PASSWORD_RESET_BLOCKED",
                user_id=user.id,
                ip_address=client_ip,
                user_agent=user_agent,
                endpoint="/auth/forgot-password",
                method="POST",
                details={"reason": "Account locked"},
                severity="WARNING"
            )
            return {
                "message": "حساب کاربری شما قفل شده است. لطفاً بعداً تلاش کنید.",
                "success": False,
                "reset_id": None
            }
        
        # غیرفعال کردن توکن‌های قبلی
        db.query(PasswordResetToken).filter(
            PasswordResetToken.user_id == user.id,
            PasswordResetToken.is_used == False
        ).update({"is_used": True})
        db.commit()
        
        # ایجاد توکن جدید
        reset_token = generate_reset_token()
        expires_at = datetime.utcnow() + timedelta(minutes=15)
        
        token_record = PasswordResetToken(
            user_id=user.id,
            token=reset_token,
            expires_at=expires_at,
            ip_address=client_ip,
            user_agent=user_agent,
            is_used=False
        )
        db.add(token_record)
        db.commit()
        
        # تولید کد تأیید ۶ رقمی
        verification_code = generate_verification_code(6)
        
        # 📱 ارسال کد با پیامک
        try:
            sms_sent = sms_provider.send_reset_password_code(
                phone_number=user.phone_number,
                code=verification_code
            )
        except Exception as e:
            logger.error(f"SMS error: {e}")
            sms_sent = False
        
        # ثبت رویداد امنیتی
        log_security_event(
            db=db,
            event_type="PASSWORD_RESET_REQUEST",
            user_id=user.id,
            ip_address=client_ip,
            user_agent=user_agent,
            endpoint="/auth/forgot-password",
            method="POST",
            details={
                "phone": user.phone_number,
                "sms_sent": sms_sent,
                "reset_token": reset_token[:10] + "..."
            }
        )
        
        # ذخیره کد در دیتابیس (برای تأیید بعدی)
        # برای سادگی، کد را در توکن ذخیره می‌کنیم
        # در محیط تولید، بهتر است از Redis یا جدول جداگانه استفاده کنید
        token_record.token = f"{reset_token}:{verification_code}"
        db.commit()
        
        logger.info(f"✅ Password reset requested for user {user.id}")
        
        return {
            "message": "کد تأیید به شماره تلفن شما ارسال شد. لطفاً کد را وارد کنید.",
            "success": True,
            "reset_id": reset_token[:8]  # برای ردیابی
        }
        
    except Exception as e:
        logger.error(f"Error in forgot_password: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در درخواست فراموشی رمز: {str(e)}"
        )


@auth_router.post("/reset-password", response_model=ResetPasswordResponse)
def reset_password(
    data: ResetPasswordRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    بازنشانی رمز عبور با کد تأیید
    """
    try:
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("User-Agent", "unknown")
        
        # پیدا کردن کاربر
        user = crud.get_user_by_phone(db, data.phone_number)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="کاربر با این شماره تلفن یافت نشد"
            )
        
        # پیدا کردن توکن
        token_record = db.query(PasswordResetToken).filter(
            PasswordResetToken.user_id == user.id,
            PasswordResetToken.is_used == False,
            PasswordResetToken.expires_at > datetime.utcnow()
        ).order_by(PasswordResetToken.created_at.desc()).first()
        
        if not token_record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="کد تأیید نامعتبر یا منقضی شده است. درخواست جدید ارسال کنید."
            )
        
        # استخراج کد از توکن
        stored_code = token_record.token.split(":")[1] if ":" in token_record.token else None
        
        if not stored_code or stored_code != data.code:
            # ثبت رویداد امنیتی
            log_security_event(
                db=db,
                event_type="PASSWORD_RESET_FAILED",
                user_id=user.id,
                ip_address=client_ip,
                user_agent=user_agent,
                endpoint="/auth/reset-password",
                method="POST",
                details={"reason": "Invalid code"},
                severity="WARNING"
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="کد تأیید نامعتبر است"
            )
        
        # اعتبارسنجی رمز جدید
        is_valid, password_message = validate_password_strength(data.new_password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=password_message
            )
        
        # به‌روزرسانی رمز عبور
        user.password_hash = get_password_hash(data.new_password)
        
        # غیرفعال کردن توکن
        token_record.is_used = True
        
        # بازنشانی تلاش‌های ناموفق
        reset_failed_attempts(user, db)
        
        # غیرفعال کردن تمام نشست‌های قبلی
        delete_user_sessions(user.id, db)
        
        db.commit()
        
        # ثبت رویداد امنیتی
        log_security_event(
            db=db,
            event_type="PASSWORD_RESET_SUCCESS",
            user_id=user.id,
            ip_address=client_ip,
            user_agent=user_agent,
            endpoint="/auth/reset-password",
            method="POST"
        )
        
        logger.info(f"✅ Password reset successful for user {user.id}")
        
        return {
            "message": "رمز عبور با موفقیت بازنشانی شد. لطفاً با رمز جدید وارد شوید.",
            "success": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in reset_password: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در بازنشانی رمز عبور: {str(e)}"
        )


# ============================================================
# 🔐 تأیید دو مرحله‌ای (2FA)
# ============================================================

@auth_router.post("/enable-2fa", response_model=Enable2FAResponse)
def enable_2fa(
    data: Enable2FARequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    فعال‌سازی تأیید دو مرحله‌ای
    """
    try:
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("User-Agent", "unknown")
        
        # بررسی اینکه شماره تلفن مطابقت دارد
        if current_user.phone_number != data.phone_number:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="شماره تلفن وارد شده با حساب کاربری شما مطابقت ندارد"
            )
        
        # اگر 2FA قبلاً فعال است
        if current_user.is_2fa_enabled:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="تأیید دو مرحله‌ای قبلاً فعال شده است"
            )
        
        # تولید کلید مخفی
        secret = generate_totp_secret()
        
        # تولید کدهای پشتیبان
        backup_codes = generate_backup_codes(10)
        
        # ذخیره در دیتابیس
        current_user.totp_secret = secret
        current_user.backup_codes = backup_codes
        current_user.is_2fa_enabled = True
        db.commit()
        
        # ثبت رویداد امنیتی
        log_security_event(
            db=db,
            event_type="2FA_ENABLED",
            user_id=current_user.id,
            ip_address=client_ip,
            user_agent=user_agent,
            endpoint="/auth/enable-2fa",
            method="POST"
        )
        
        logger.info(f"✅ 2FA enabled for user {current_user.id}")
        
        return {
            "secret": secret,
            "backup_codes": backup_codes,
            "qr_code_url": None,
            "message": "تأیید دو مرحله‌ای با موفقیت فعال شد. کدهای پشتیبان را ذخیره کنید.",
            "success": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error enabling 2FA: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در فعال‌سازی 2FA: {str(e)}"
        )


@auth_router.post("/verify-2fa", response_model=Verify2FAResponse)
def verify_2fa(
    data: Verify2FARequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    تأیید کد 2FA
    """
    try:
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("User-Agent", "unknown")
        
        if not current_user.is_2fa_enabled:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="تأیید دو مرحله‌ای فعال نیست"
            )
        
        # بررسی کد
        is_valid = False
        if current_user.totp_secret:
            is_valid = verify_totp(current_user.totp_secret, data.code)
        
        # اگر کد TOTP معتبر نبود، کدهای پشتیبان را بررسی کن
        if not is_valid:
            is_valid = verify_backup_code(current_user, data.code)
            if is_valid:
                db.commit()
        
        if not is_valid:
            # ثبت رویداد امنیتی
            log_security_event(
                db=db,
                event_type="2FA_VERIFY_FAILED",
                user_id=current_user.id,
                ip_address=client_ip,
                user_agent=user_agent,
                endpoint="/auth/verify-2fa",
                method="POST",
                details={"reason": "Invalid code"},
                severity="WARNING"
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="کد تأیید نامعتبر است"
            )
        
        # ثبت رویداد امنیتی
        log_security_event(
            db=db,
            event_type="2FA_VERIFIED",
            user_id=current_user.id,
            ip_address=client_ip,
            user_agent=user_agent,
            endpoint="/auth/verify-2fa",
            method="POST"
        )
        
        logger.info(f"✅ 2FA verified for user {current_user.id}")
        
        return {
            "message": "کد تأیید صحیح است.",
            "success": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error verifying 2FA: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در تأیید 2FA: {str(e)}"
        )


@auth_router.post("/disable-2fa", response_model=Disable2FAResponse)
def disable_2fa(
    data: Disable2FARequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    غیرفعال‌سازی تأیید دو مرحله‌ای
    """
    try:
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("User-Agent", "unknown")
        
        if not current_user.is_2fa_enabled:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="تأیید دو مرحله‌ای فعال نیست"
            )
        
        # بررسی کد
        is_valid = False
        if current_user.totp_secret:
            is_valid = verify_totp(current_user.totp_secret, data.code)
        
        if not is_valid:
            is_valid = verify_backup_code(current_user, data.code)
            if is_valid:
                db.commit()
        
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="کد تأیید نامعتبر است"
            )
        
        # غیرفعال‌سازی 2FA
        current_user.is_2fa_enabled = False
        current_user.totp_secret = None
        current_user.backup_codes = None
        db.commit()
        
        # ثبت رویداد امنیتی
        log_security_event(
            db=db,
            event_type="2FA_DISABLED",
            user_id=current_user.id,
            ip_address=client_ip,
            user_agent=user_agent,
            endpoint="/auth/disable-2fa",
            method="POST"
        )
        
        logger.info(f"✅ 2FA disabled for user {current_user.id}")
        
        return {
            "message": "تأیید دو مرحله‌ای با موفقیت غیرفعال شد.",
            "success": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error disabling 2FA: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطا در غیرفعال‌سازی 2FA: {str(e)}"
        )