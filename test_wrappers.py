from wrappers import AVAILABLE_MODULES
from autohunter_core import RequestEngine

def test_wrappers():
    engine = RequestEngine()
    target = "http://127.0.0.1:8001"
    
    print("Testing wrappers with modules:", list(AVAILABLE_MODULES.keys()))
    
    for module_name, func in AVAILABLE_MODULES.items():
        result = func(target, engine)
        print(f"[*] Ran {module_name}: {result['status']}")
        if result['findings']:
            for finding in result['findings']:
                print(f"    - [{finding['severity']}] {finding['detail']}")

if __name__ == "__main__":
    test_wrappers()
