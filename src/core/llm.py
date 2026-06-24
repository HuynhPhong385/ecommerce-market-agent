# src/core/llm.py

import os
import logging
from typing import Optional, Dict, Any, List

from src.core.config import Config

logger = logging.getLogger(__name__)


class LLMManager:
    """
    Quản lý Google Gemini LLM
    """
    
    def __init__(self):
        self.config = Config()
        self._llm = None
        
        # Kiểm tra API Key
        if not self.config.validate_api_key():
            logger.warning("⚠️ GOOGLE_API_KEY chưa được cấu hình")
    
    def get_llm(self, **kwargs):
        """
        Lấy instance của Gemini LLM
        """
        if self._llm is None:
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI
                
                api_key = self.config.GOOGLE_API_KEY
                if not api_key:
                    raise ValueError("GOOGLE_API_KEY không tồn tại")
                
                model = kwargs.get('model') or self.config.GEMINI_MODEL
                
                logger.info(f"🤖 Khởi tạo Gemini với model: {model}")
                
                self._llm = ChatGoogleGenerativeAI(
                    model=model,
                    google_api_key=api_key,
                    temperature=kwargs.get('temperature', 0.7),
                    max_output_tokens=kwargs.get('max_tokens', 2000),
                    timeout=kwargs.get('timeout', 60),
                )
                
                logger.info(f"✅ Khởi tạo Gemini thành công")
                
            except ImportError:
                logger.error("❌ Chưa cài langchain-google-genai")
                logger.error("   pip install langchain-google-genai google-generativeai")
                raise
            except Exception as e:
                logger.error(f"❌ Lỗi: {str(e)}")
                raise
        
        return self._llm
    
    def test_connection(self) -> bool:
        """
        Kiểm tra kết nối với Gemini API
        """
        try:
            logger.info("⏳ Đang test kết nối Gemini...")
            
            llm = self.get_llm()
            response = llm.invoke("Hello! Respond with 'OK' only.")
            
            # Lấy nội dung response
            if hasattr(response, 'content'):
                content = response.content
            else:
                content = str(response)
            
            logger.info(f"✅ Kết nối thành công: {content}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Lỗi: {str(e)}")
            return False
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """
        Tạo nội dung với prompt
        """
        try:
            from langchain_core.prompts import ChatPromptTemplate
            
            llm = self.get_llm(**kwargs)
            
            messages = []
            if system_prompt:
                messages.append(("system", system_prompt))
            messages.append(("human", prompt))
            
            chat_prompt = ChatPromptTemplate.from_messages(messages)
            chain = chat_prompt | llm
            
            response = chain.invoke({})
            
            if hasattr(response, 'content'):
                content = response.content
                # Ensure we always return a string
                try:
                    from json import dumps
                    if isinstance(content, str):
                        return content
                    return dumps(content, ensure_ascii=False)
                except Exception:
                    return str(content)
            return str(response)
            
        except Exception as e:
            logger.error(f"❌ Lỗi generate: {str(e)}")
            raise
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Lấy thông tin model
        """
        return {
            'provider': 'Google Gemini',
            'model': self.config.GEMINI_MODEL,
            'api_key_set': bool(self.config.GOOGLE_API_KEY),
            'max_tokens': 2000,
        }


# ==================== FUNCTIONS ====================

_llm_manager = None


def get_llm_manager() -> LLMManager:
    """Lấy instance của LLMManager"""
    global _llm_manager
    if _llm_manager is None:
        _llm_manager = LLMManager()
    return _llm_manager


def get_llm(**kwargs):
    """Lấy Gemini LLM instance"""
    return get_llm_manager().get_llm(**kwargs)


def test_connection() -> bool:
    """Kiểm tra kết nối"""
    return get_llm_manager().test_connection()


def generate_text(prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
    """Tạo text với Gemini"""
    return get_llm_manager().generate(prompt, system_prompt, **kwargs)


def get_model_info() -> Dict[str, Any]:
    """Lấy thông tin model"""
    return get_llm_manager().get_model_info()


# ==================== TEST ====================

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 TEST GEMINI")
    print("=" * 60)
    
    # Kiểm tra API Key
    manager = get_llm_manager()
    api_key = manager.config.GOOGLE_API_KEY
    api_key_preview = f"***{api_key[-4:]}" if api_key else "Not set"
    print(f"\n🔑 API Key: {api_key_preview}")
    print(f"🤖 Model: {manager.config.GEMINI_MODEL}")
    
    # Test kết nối
    print("\n⏳ Test kết nối...")
    success = test_connection()
    
    if success:
        print("✅ Kết nối thành công!")
        
        # Test generate
        print("\n⏳ Test generate...")
        try:
            result = generate_text(
                prompt="Giới thiệu về Google Gemini trong 1 câu.",
                system_prompt="Bạn là trợ lý AI."
            )
            print(f"✅ Response: {result}")
        except Exception as e:
            print(f"❌ Lỗi: {str(e)}")
    else:
        print("❌ Kết nối thất bại!")
        print("\n💡 Kiểm tra:")
        print("1. GOOGLE_API_KEY trong .env")
        print("2. pip install langchain-google-genai google-generativeai")
    
    print("\n" + "=" * 60)