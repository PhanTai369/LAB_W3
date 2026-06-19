import requests

alert = [
    {
        "labels": {
            "alertname": "InstanceDown",
            "service": "checkout-svc",
            "severity": "critical"
        },
        "annotations": {
            "summary": "Instance down: checkout-svc",
            "description": "Service checkout-svc has been unreachable for more than 30 seconds."
        }
    }
]

try:
    resp = requests.post("http://localhost:9093/api/v2/alerts", json=alert)
    if resp.status_code == 200:
        print("[SUCCESS] Da gui canh bao InstanceDown (checkout-svc) gia lap thanh cong!")
        print("Hay quan sat cua so terminal chay closed_loop.py de xem no tu dong rollback!")
    else:
        print(f"[FAIL] Khong the gui canh bao. Status code: {resp.status_code}")
except Exception as e:
    print(f"[ERROR] Loi ket noi toi Alertmanager: {e}")
