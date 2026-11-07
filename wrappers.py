import io
import contextlib
import importlib

def run_tool_capture(tool_module_name, func_name, *args):
    """
    خروجی پرینت ابزارها رو به دام میندازه و با فیلترهای سخت‌گیرانه،
    از False Positive (باگ‌های کاذب) جلوگیری می‌کنه.
    """
    try:
        module = importlib.import_module(tool_module_name)
        func = getattr(module, func_name)
        
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            func(*args)
        
        output = f.getvalue().strip()
        output_lower = output.lower()
        
        if not output:
            return []

        # ۱. فیلترهای منفی (اگر اینا باشن، یعنی قطعاً باگ نیست)
        hard_negatives = [
            "method not allowed", "405", "400 bad", "401", "403", "500",
            "not found", "connection refused", "timeout", "failed to", 
            "[-]", "no sql", "no xss", "not vulnerable", "not detected", 
            "no path", "no ssti", "error:", "clean", 
            "no numeric id", "no obvious vulnerabilities" # اضافه شده برای IDOR
        ]
        if any(neg in output_lower for neg in hard_negatives):
            return [{"severity": "Info", "detail": output}]
            
        # ۲. فیلتر ضد صفحه اصلی سایت (Soft 404)
        if "[+]" in output and ("<!doctype html>" in output_lower or "<html" in output_lower):
            if tool_module_name != "xss_scanner":
                return [{"severity": "Info", "detail": "False Positive (Received standard HTML page instead of vulnerable response)\n\n" + output}]

        # ۳. فیلتر مخصوص SSTI
        if tool_module_name == "ssti_scanner" and "expected result: 49" in output_lower:
            return [{"severity": "Info", "detail": "False Positive Suspected: Scanner found '49' in the page, but it might be a coincidence. Manual verification required.\n\n" + output}]

        # ۴. فیلترهای مثبت قطعی (اگر اینا باشن، یعنی صد در صد باگه)
        hard_positives = [
            "root:x:0:0",           # LFI موفق
            "<script>alert",        # XSS موفق
            "sql syntax",           # خطای SQL
            "successfully bypassed",# دور زدن احراز هویت
            "potential idor found"  # IDOR موفق (اضافه شده)
        ]
        if any(pos in output_lower for pos in hard_positives):
            return [{"severity": "High", "detail": output}]

        # ۵. فیلترهای مثبت نسبی
        soft_positives = ["vulnerable", "found!", "evaluated our code"]
        if any(pos in output_lower for pos in soft_positives):
            return [{"severity": "High", "detail": output}]

        # ۶. بقیه موارد به عنوان اطلاعات (Info)
        return [{"severity": "Info", "detail": output}]

    except Exception as e:
        return [{"severity": "Error", "detail": f"Failed to run {tool_module_name}: {str(e)}"}]


# ==========================================
# Wrappers برای ابزارهای واقعی
# ==========================================

def run_xss_scanner(target: str, engine) -> dict:
    return {"module": "xss_scanner", "status": "success", "findings": run_tool_capture("xss_scanner", "scan_xss", target)}

def run_cors_scanner(target: str, engine) -> dict:
    return {"module": "cors_scanner", "status": "success", "findings": run_tool_capture("cors_scanner", "check_cors", target)}

def run_sqli_scanner(target: str, engine) -> dict:
    return {"module": "sqli_scanner", "status": "success", "findings": run_tool_capture("sqli_scanner", "scan_sqli", target, "id")}

def run_lfi_scanner(target: str, engine) -> dict:
    return {"module": "lfi_scanner", "status": "success", "findings": run_tool_capture("lfi_scanner", "scan_lfi", target, "file")}

def run_ssti_scanner(target: str, engine) -> dict:
    return {"module": "ssti_scanner", "status": "success", "findings": run_tool_capture("ssti_scanner", "test_ssti", target, "name")}

def run_jwt_scanner(target: str, engine) -> dict:
    return {"module": "jwt_bypass", "status": "success", "findings": run_tool_capture("jwt_bypass_scanner", "test_bypass", target)}

def run_ssrf_scanner(target: str, engine) -> dict:
    return {"module": "ssrf_scanner", "status": "success", "findings": run_tool_capture("ssrf_scanner", "test_ssrf", target, "url")}

def run_backup_finder(target: str, engine) -> dict:
    return {"module": "backup_finder", "status": "success", "findings": run_tool_capture("backup_finder", "scan_backups", target)}

def run_param_fuzzer(target: str, engine) -> dict:
    return {"module": "param_fuzzer", "status": "success", "findings": run_tool_capture("param_fuzzer", "fuzz_params", target)}

def run_api_fuzzer(target: str, engine) -> dict:
    return {"module": "api_fuzzer", "status": "success", "findings": run_tool_capture("api_fuzzer", "fuzz_api", target)}

def run_xxe_scanner(target: str, engine) -> dict:
    return {"module": "xxe_scanner", "status": "success", "findings": run_tool_capture("xxe_scanner", "test_xxe", target)}

def run_api_version_scanner(target: str, engine) -> dict:
    return {"module": "api_version_scanner", "status": "success", "findings": run_tool_capture("api_version_scanner", "scan_api_versions", target)}

def run_security_header_checker(target: str, engine) -> dict:
    return {"module": "security_header_checker", "status": "success", "findings": run_tool_capture("security_header_checker", "check_headers", target)}

def run_tech_fingerprinter(target: str, engine) -> dict:
    return {"module": "tech_fingerprinter", "status": "success", "findings": [{"severity": "Info", "detail": "Technology check needs manual integration"}]}

# --- ابزار جدید ما برای IDOR ---
def run_idor_scanner(target: str, engine) -> dict:
    return {"module": "idor_scanner", "status": "success", "findings": run_tool_capture("idor_scanner", "scan_idor", target, engine)}


# ==========================================
# ثبت تمام ماژول‌ها برای نمایش در UI
# ==========================================
AVAILABLE_MODULES = {
    "xss_scanner": run_xss_scanner,
    "sqli_scanner": run_sqli_scanner,
    "lfi_scanner": run_lfi_scanner,
    "ssti_scanner": run_ssti_scanner,
    "cors_scanner": run_cors_scanner,
    "jwt_bypass": run_jwt_scanner,
    "ssrf_scanner": run_ssrf_scanner,
    "backup_finder": run_backup_finder,
    "param_fuzzer": run_param_fuzzer,
    "api_fuzzer": run_api_fuzzer,
    "xxe_scanner": run_xxe_scanner,
    "api_version_scanner": run_api_version_scanner,
    "security_header_checker": run_security_header_checker,
    "tech_fingerprinter": run_tech_fingerprinter,
    "idor_scanner": run_idor_scanner, # <--- ماژول جدید
}
