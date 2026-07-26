#fa_func.py


try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    _RTL_FIX_AVAILABLE = True
except ImportError:
    _RTL_FIX_AVAILABLE = False

def fa(text):
    """متن فارسی را برای نمایش صحیح در ترمینال‌های بدون پشتیبانی bidi آماده می‌کند.
    """
    if not _RTL_FIX_AVAILABLE:
        return text
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)



if not _RTL_FIX_AVAILABLE:
    print(
        "توجه: برای نمایش صحیح متن فارسی در ترمینال، این دستور را اجرا کنید:\n"
        "pip install arabic-reshaper python-bidi"
    )

