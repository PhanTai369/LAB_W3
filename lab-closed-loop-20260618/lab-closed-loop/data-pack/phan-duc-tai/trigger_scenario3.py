import requests

alert = [
    {
        "labels": {
            "alertname": "InstanceDown",
            "service": "checkout-svc",
            "severity": "critical"
        },
        "annotations": {
            "summary": "Instance down: checkout-svc"
        }
    },
    {
        "labels": {
            "alertname": "InstanceDown",
            "service": "payment-svc",
            "severity": "critical"
        },
        "annotations": {
            "summary": "Instance down: payment-svc"
        }
    },
    {
        "labels": {
            "alertname": "InstanceDown",
            "service": "inventory-svc",
            "severity": "critical"
        },
        "annotations": {
            "summary": "Instance down: inventory-svc"
        }
    }
]

try:
    resp = requests.post("http://localhost:9093/api/v2/alerts", json=alert)
    if resp.status_code == 200:
        print("[SUCCESS] Da gui 3 canh bao InstanceDown gia lap de ngat mach (Circuit Breaker) thanh cong!")
        print("Hay quan sat cua so terminal chay closed_loop.py de xem thong bao CIRCUIT_BREAKER_HALT!")
    else:
        print(f"[FAIL] Khong the gui canh bao. Status code: {resp.status_code}")
except Exception as e:
    print(f"[ERROR] Loi ket noi toi Alertmanager: {e}")
