"""Central application configuration for the Groq clinical documentation MVP."""
from __future__ import annotations
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

def get_secret(key: str, default: str = "") -> str:
    """Retrieve secret from environment variable or Streamlit secrets."""
    val = os.getenv(key)
    if val:
        return val
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass
    return default

@dataclass(frozen=True)
class Settings:
    groq_api_key: str = "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"
    reasoning_model: str = "openai/gpt-oss-120b"
    fallback_model: str = "openai/gpt-oss-20b"
    stt_model: str = "whisper-large-v3-turbo"
    vision_model: str = "qwen/qwen3.8-27b"
    tts_model: str = "canopylabs/orpheus-v1-english"
    safety_model: str = "openai/gpt-oss-safeguard-20b"
    db_path: str = "database/app.db"
    groq_base_url: str = "https://api.groq.com/openai/v1"

    def __getattribute__(self, name: str):
        val = object.__getattribute__(self, name)
        env_map = {
            "groq_api_key": ("GROQ_API_KEY", "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"),
            "reasoning_model": ("GROQ_REASONING_MODEL", "openai/gpt-oss-120b"),
            "fallback_model": ("GROQ_FALLBACK_MODEL", "openai/gpt-oss-20b"),
            "stt_model": ("GROQ_STT_MODEL", "whisper-large-v3-turbo"),
            "vision_model": ("GROQ_VISION_MODEL", "qwen/qwen3.8-27b"),
            "tts_model": ("GROQ_TTS_MODEL", "canopylabs/orpheus-v1-english"),
            "safety_model": ("GROQ_SAFETY_MODEL", "openai/gpt-oss-safeguard-20b"),
            "db_path": ("DB_PATH", "database/app.db"),
        }
        if name in env_map:
            env_key, default_val = env_map[name]
            if val != default_val:
                return val
            return get_secret(env_key, default_val)
        return val

settings = Settings()


