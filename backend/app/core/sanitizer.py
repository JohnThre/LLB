"""
Security sanitization utilities
"""
import re
import html
from pathlib import Path
from typing import Any, Dict, Optional


def sanitize_log_input(value: Any) -> str:
    """Sanitize input for logging to prevent log injection"""
    if value is None:
        return "None"
    
    # Convert to string
    text = str(value)
    
    # Remove newlines and carriage returns
    text = text.replace('\n', '\\n').replace('\r', '\\r')
    
    # Remove control characters
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    
    # Limit length
    if len(text) > 200:
        text = text[:200] + "..."
    
    return text


def sanitize_path(path: str, base_path: Optional[str] = None) -> str:
    """Sanitize file path to prevent path traversal"""
    # Remove null bytes
    path = path.replace('\x00', '')
    
    # Resolve path
    resolved_path = Path(path).resolve()
    
    # Check against base path if provided
    if base_path:
        base_resolved = Path(base_path).resolve()
        try:
            resolved_path.relative_to(base_resolved)
        except ValueError:
            raise ValueError("Path traversal attempt detected")
    
    return str(resolved_path)


def sanitize_html(text: str) -> str:
    """Sanitize HTML to prevent XSS"""
    return html.escape(text, quote=True)


def sanitize_dict_for_logging(data: Dict[str, Any]) -> Dict[str, str]:
    """Sanitize dictionary values for safe logging"""
    return {k: sanitize_log_input(v) for k, v in data.items()}