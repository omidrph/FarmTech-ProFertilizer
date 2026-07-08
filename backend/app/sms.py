# backend/app/sms.py
"""سیستم ارسال پیامک FarmTech - برای فعال‌سازی بعدی"""

import logging
import json
from typing import Optional, Dict, Any
from datetime import datetime

from app.config import settings

logger = logging.getLogger(__name__)


class SMSProvider:
    """کلاس پایه برای ارائه‌دهندگان پیامک"""
    
    def __init__(self, provider: str = "kavenegar"):
        self.provider = provider
        self.api_key = settings.SMS_API_KEY
        self.sender = settings.SMS_SENDER_NUMBER
    
    def send_verification_code(self, phone_number: str, code: str) -> bool:
        """
        ارسال کد تأیید
        
        Args:
            phone_number: شماره تلفن گیرنده
            code: کد تأیید
        
        Returns:
            bool: آیا ارسال موفق بود
        """
        template = settings.SMS_VERIFICATION_TEMPLATE
        message = f"کد تأیید شما: {code}\nFarmTech - سیستم هوشمند نسخه‌نویسی کود"
        return self.send(phone_number, message, template)
    
    def send_reset_password_code(self, phone_number: str, code: str) -> bool:
        """
        ارسال کد فراموشی رمز عبور
        
        Args:
            phone_number: شماره تلفن گیرنده
            code: کد تأیید
        
        Returns:
            bool: آیا ارسال موفق بود
        """
        template = settings.SMS_RESET_PASSWORD_TEMPLATE
        message = f"کد بازیابی رمز عبور: {code}\nاین کد به مدت ۱۵ دقیقه معتبر است.\nFarmTech"
        return self.send(phone_number, message, template)
    
    def send_2fa_code(self, phone_number: str, code: str) -> bool:
        """
        ارسال کد 2FA
        
        Args:
            phone_number: شماره تلفن گیرنده
            code: کد تأیید
        
        Returns:
            bool: آیا ارسال موفق بود
        """
        template = settings.SMS_2FA_TEMPLATE
        message = f"کد تأیید دو مرحله‌ای: {code}\nFarmTech"
        return self.send(phone_number, message, template)
    
    def send(self, phone_number: str, message: str, template: Optional[str] = None) -> bool:
        """
        ارسال پیامک اصلی
        
        Args:
            phone_number: شماره تلفن گیرنده
            message: متن پیام
            template: قالب پیام (اختیاری)
        
        Returns:
            bool: آیا ارسال موفق بود
        """
        # اگر API Key تنظیم نشده باشد، فقط لاگ کن
        if not self.api_key or self.api_key == "your-sms-api-key":
            logger.info(f"📱 [SMS SIMULATION] To: {phone_number}")
            logger.info(f"📱 [SMS SIMULATION] Message: {message}")
            logger.info(f"📱 [SMS SIMULATION] Template: {template}")
            return True
        
        # پیاده‌سازی واقعی برای Kavenegar
        if self.provider == "kavenegar":
            return self._send_kavenegar(phone_number, message)
        
        # پیاده‌سازی واقعی برای دیگر ارائه‌دهندگان
        elif self.provider == "sms_ir":
            return self._send_sms_ir(phone_number, message)
        
        else:
            logger.error(f"Unknown SMS provider: {self.provider}")
            return False
    
    def _send_kavenegar(self, phone_number: str, message: str) -> bool:
        """
        ارسال پیامک از طریق Kavenegar
        
        Args:
            phone_number: شماره تلفن گیرنده
            message: متن پیام
        
        Returns:
            bool: آیا ارسال موفق بود
        """
        try:
            import requests
            
            url = f"https://api.kavenegar.com/v1/{self.api_key}/sms/send.json"
            params = {
                "receptor": phone_number,
                "sender": self.sender,
                "message": message
            }
            
            response = requests.post(url, data=params, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            if result.get("return", {}).get("status") == 200:
                logger.info(f"✅ SMS sent via Kavenegar to {phone_number}")
                return True
            else:
                logger.error(f"❌ SMS failed: {result}")
                return False
                
        except ImportError:
            logger.warning("requests not installed. SMS simulation only.")
            return True
        except Exception as e:
            logger.error(f"❌ SMS error: {e}")
            return False
    
    def _send_sms_ir(self, phone_number: str, message: str) -> bool:
        """
        ارسال پیامک از طریق sms.ir
        
        Args:
            phone_number: شماره تلفن گیرنده
            message: متن پیام
        
        Returns:
            bool: آیا ارسال موفق بود
        """
        try:
            import requests
            
            url = "https://api.sms.ir/v1/send"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            data = {
                "receptor": phone_number,
                "sender": self.sender,
                "message": message
            }
            
            response = requests.post(url, json=data, headers=headers, timeout=10)
            response.raise_for_status()
            
            logger.info(f"✅ SMS sent via sms.ir to {phone_number}")
            return True
                
        except ImportError:
            logger.warning("requests not installed. SMS simulation only.")
            return True
        except Exception as e:
            logger.error(f"❌ SMS error: {e}")
            return False


# ایجاد نمونه singleton
sms_provider = SMSProvider(settings.SMS_PROVIDER)


def generate_verification_code(length: int = 6) -> str:
    """
    تولید کد تأیید تصادفی
    
    Args:
        length: طول کد
    
    Returns:
        str: کد تأیید
    """
    import secrets
    return ''.join(secrets.choice('0123456789') for _ in range(length))


def generate_reset_token(length: int = 32) -> str:
    """
    تولید توکن تصادفی برای فراموشی رمز
    
    Args:
        length: طول توکن
    
    Returns:
        str: توکن
    """
    import secrets
    return secrets.token_urlsafe(length)