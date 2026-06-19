import requests

alert = [
    {
        "labels": {
            "alertname": "HighLatency",
            "service": "payment-svc",
            "severity": "warning"
        },
        "annotations": {
            "summary": "High latency on payment-svc",
            "description": "p99 latency is 600ms on service payment-svc"
        }
    }
]

try:
    resp = requests.post("http://localhost:9093/api/v2/alerts", json=alert)
    if resp.status_code == 200:
        print("[SUCCESS] Da gui canh bao HighLatency (payment-svc) gia lap thanh cong!")
        print("Hay quan sat cua so terminal chay closed_loop.py de xem no tu dong restart!")
    else:
        print(f"[FAIL] Khong the gui canh bao. Status code: {resp.status_code}")
except Exception as e:
    print(f"[ERROR] Loi ket noi toi Alertmanager: {e}")
