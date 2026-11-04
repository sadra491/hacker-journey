import random
import time
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class BlockDetected(Exception):
    pass

def normalize_target(target: str) -> str:
    target = target.strip()
    if not target:
        raise ValueError("Target is empty")
    if target.startswith("http://") or target.startswith("https://"):
        return target.rstrip("/")
    return f"https://{target}"

def load_proxies(proxy_text: str) -> list:
    proxies = []
    for line in proxy_text.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if not line.startswith(("http://", "https://", "socks5://", "socks4://")):
            line = f"http://{line}"
        proxies.append(line)
    return proxies

class RequestEngine:
    def __init__(self, jitter_min=1.0, jitter_max=3.0, timeout=10,
                 use_proxy_rotation=False, proxies=None, max_retries=2,
                 block_wait_seconds=0):
        self.jitter_min = jitter_min
        self.jitter_max = jitter_max
        self.timeout = timeout
        self.use_proxy_rotation = use_proxy_rotation
        self.proxies = proxies or []
        self.proxy_index = 0
        self.max_retries = max_retries
        self.block_wait_seconds = block_wait_seconds
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "AutoHunter/1.0"})

    def _current_proxies(self):
        if not self.use_proxy_rotation or not self.proxies:
            return None
        proxy = self.proxies[self.proxy_index % len(self.proxies)]
        return {"http": proxy, "https": proxy}

    def _rotate_proxy(self):
        if self.proxies:
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)

    def _jitter(self):
        time.sleep(random.uniform(self.jitter_min, self.jitter_max))

    def request(self, method, url, **kwargs):
        self._jitter()
        kwargs.setdefault("timeout", self.timeout)
        kwargs.setdefault("proxies", self._current_proxies())
        kwargs.setdefault("verify", False)

        last_exc = None
        for attempt in range(self.max_retries + 1):
            try:
                resp = self.session.request(method, url, **kwargs)
                if resp.status_code in (429, 403):
                    if self.block_wait_seconds > 0:
                        time.sleep(self.block_wait_seconds)
                        self.block_wait_seconds = 0
                        continue
                    if self.use_proxy_rotation and len(self.proxies) > 1:
                        self._rotate_proxy()
                        continue
                    raise BlockDetected(f"Blocked with status {resp.status_code} at {url}")
                return resp
            except BlockDetected:
                raise
            except requests.RequestException as e:
                last_exc = e
                if self.use_proxy_rotation and len(self.proxies) > 1:
                    self._rotate_proxy()
                    continue
                time.sleep(1)
        if last_exc:
            raise last_exc
        raise RuntimeError("Request failed after retries")
