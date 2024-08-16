"""
These are functions that just simply return properly
formatted javascript to inject into streamlit
"""

from datetime import datetime, timedelta


def set_cookie(name: str, value: str, days: int):
    expiry_date = datetime.now() + timedelta(days=days)
    expiry_date_formatted = expiry_date.strftime("%a, %d %b %Y %H:%M:%S GMT")
    js = f'document.cookie = "{name}={value}; {expiry_date_formatted}; path=/";'
    return f"<script>\n{js}\n</script>"


# print(datetime.now())

# print(set_cookie("hello", "test", 2))
