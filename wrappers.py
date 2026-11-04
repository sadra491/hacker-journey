import io
import contextlib
import importlib

def run_tool_capture(tool_module_name, func_name, *args):
    """
    ابزارهای تو خروجی رو Print میکنن. این تابع خروجی پرینت رو به دام میندازه 
    تا ما بتونیم توی رابط کاربری نشونش بدیم.
    """
    try:
        # داینامیک ماژول رو ایمپورت میکنیم
        module = importlib.import_module(tool_module_name)
        func = getattr(module, func_name)
        
        # دام انداختن خروجی پرینت
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            func(*args)
        
        # گرفتن متن خروجی
        output = f.getvalue().strip()
        
        # اگر خروجی داشت، یعنی احتمالا باگ پیدا شده
        if output:
            return [{"severity": "High", "detail": output}]
        return []
    except Exception as e:
        return [{"severity": "Error", "detail": f"Failed to run {tool_module_name}: {str(e)}"}]

# ==========================================
# Wrappers برای ابزارهای واقعی تو
# ==========================================

def run_xss_scanner(target: str, engine) -> dict:
    # فرض: xss_scanner.py تابع scan_xss(url) داره
    findings = run_tool_capture("xss_scanner", "scan_xss", target)
    return {"module": "xss_scanner", "status": "success", "findings": findings}

def run_cors_scanner(target: str, engine) -> dict:
    # فرض: cors_scanner.py تابع check_cors(url) داره
    findings = run_tool_capture("cors_scanner", "check_cors", target)
    return {"module": "cors_scanner", "status": "success", "findings": findings}

def run_sqli_scanner(target: str, engine) -> dict:
    # فرض: sqli_scanner.py تابع scan_sqli(url, param) داره
    # فعلا پارامتر رو 'id' میذاریم (چون نمیدونیم سایت چه پارامتری داره)
    findings = run_tool_capture("sqli_scanner", "scan_sqli", target, "id")
    return {"module": "sqli_scanner", "status": "success", "findings": findings}

def run_lfi_scanner(target: str, engine) -> dict:
    findings = run_tool_capture("lfi_scanner", "scan_lfi", target, "file")
    return {"module": "lfi_scanner", "status": "success", "findings": findings}

def run_ssti_scanner(target: str, engine) -> dict:
    findings = run_tool_capture("ssti_scanner", "test_ssti", target, "name")
    return {"module": "ssti_scanner", "status": "success", "findings": findings}

def run_tech_fingerprinter(target: str, engine) -> dict:
    # اگر ابزارت print نمیکنه و فقط برمیگردونه، اینجا باید فرق کنه. 
    # فعلا این رو فیک میذاریم تا مطمئن بشیم بقیه کار میکنن.
    return {"module": "tech_fingerprinter", "status": "success", "findings": [{"severity": "Info", "detail": "Technology check needs manual integration"}]}


# ==========================================
# ثبت ماژول‌ها
# ==========================================
AVAILABLE_MODULES = {
    "xss_scanner": run_xss_scanner,
    "cors_scanner": run_cors_scanner,
    "sqli_scanner": run_sqli_scanner,
    "lfi_scanner": run_lfi_scanner,
    "ssti_scanner": run_ssti_scanner,
    "tech_fingerprinter": run_tech_fingerprinter,
}
