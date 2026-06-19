import time
import requests
import threading

def generate_load(url):
    session = requests.Session()
    while True:
        try:
            session.get(url, timeout=2)
        except Exception:
            pass
        time.sleep(0.1) # ~10 req/s per thread

urls = [
    "http://localhost:8080/",
    "http://localhost:8081/",
    "http://localhost:8082/",
    "http://localhost:8083/",
    "http://localhost:8084/"
]

threads = []
for url in urls:
    for _ in range(4):  # 4 threads per service
        t = threading.Thread(target=generate_load, args=(url,), daemon=True)
        t.start()
        threads.append(t)

print("Starting traffic generator on all mock services...")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping traffic generator.")
