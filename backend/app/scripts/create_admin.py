# backend/app/scripts/create_admin.py
"""
ساخت/ارتقای ادمین از ترمینال
------------------------------------------------------------
  # ارتقای کاربر موجود به ادمین
  python -m app.scripts.create_admin 09120000000

  # ساخت ادمین جدید (اگر شماره وجود نداشته باشد)
  python -m app.scripts.create_admin 09120000000 --first علی --last رضایی --password 'Str0ng!Pass'

  # برگرداندن به کاربر معمولی
  python -m app.scripts.create_admin 09120000000 --demote
"""
import argparse
import getpass
import sys

from app.database import SessionLocal
from app.models import User
from app.schemas.base import validate_phone_number
from app.security import get_password_hash, validate_password_strength


def main() -> int:
    ap = argparse.ArgumentParser(description="ساخت/ارتقای ادمین")
    ap.add_argument("phone")
    ap.add_argument("--first", default=None)
    ap.add_argument("--last", default=None)
    ap.add_argument("--password", default=None)
    ap.add_argument("--demote", action="store_true", help="برگرداندن به کاربر معمولی")
    a = ap.parse_args()

    try:
        phone = validate_phone_number(a.phone)
    except ValueError as e:
        print(f"❌ {e}")
        return 1

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.phone_number == phone).first()
        if a.demote:
            if not user:
                print("❌ کاربر پیدا نشد")
                return 1
            user.role = "user"
            db.commit()
            print(f"✅ {user.full_name} اکنون کاربر معمولی است")
            return 0

        if user is None:
            first = a.first or input("نام: ").strip()
            last = a.last or input("نام خانوادگی: ").strip()
            pw = a.password or getpass.getpass("رمز عبور: ")
            ok, msg = validate_password_strength(pw)
            if not ok:
                print(f"❌ {msg}")
                return 1
            user = User(first_name=first, last_name=last, phone_number=phone,
                        password_hash=get_password_hash(pw), role="admin", status="active", is_active=True)
            db.add(user)
            print("🆕 کاربر جدید ساخته شد")
        else:
            user.role = "admin"
            user.status, user.is_active = "active", True
        db.commit()
        print(f"✅ {user.full_name} ({phone}) اکنون ادمین است")
        return 0
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())
