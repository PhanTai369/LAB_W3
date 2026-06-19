# SUBMIT.md — Kết quả chạy 3 chaos scenarios

## Thông tin

- Họ tên: Phan Đức Tài
- Decision engine: Rule-based (`RUNBOOK_MAP` trong `config.yaml`)
- Python: 3.12.10
- Docker Compose: v5.1.4

---

## Scenario 1 — Action thành công (latency inject trên payment-svc)

**Lệnh inject (PowerShell):**
```powershell
docker run --rm --network container:ronki-payment-svc --cap-add=NET_ADMIN alpine sh -c "apk add --no-cache iproute2 && tc qdisc add dev eth0 root netem delay 500ms"
```

**Log orchestrator:**
```json
{"ts": "2026-06-18T04:21:29.458389+00:00", "level": "INFO", "event_type": "ALERT_DETECTED", "alertname": "HighLatency", "service": "payment-svc", "severity": "warning"}
{"ts": "2026-06-18T04:21:29.459390+00:00", "level": "INFO", "event_type": "DECIDE_RUNBOOK", "alertname": "HighLatency", "service": "payment-svc", "runbook": "runbooks/restart_service.sh"}
{"ts": "2026-06-18T04:21:29.459390+00:00", "level": "INFO", "event_type": "BLAST_RADIUS_OK", "service": "payment-svc"}
{"ts": "2026-06-18T04:21:29.459982+00:00", "level": "INFO", "event_type": "RUNBOOK_EXEC", "script": "runbooks/restart_service.sh", "service": "payment-svc", "dry_run": true}
{"ts": "2026-06-18T04:21:29.577552+00:00", "level": "INFO", "event_type": "RUNBOOK_RESULT", "script": "runbooks/restart_service.sh", "service": "payment-svc", "returncode": 0, "stdout": "[DRY-RUN] would execute: docker restart ronki-payment-svc", "stderr": ""}
{"ts": "2026-06-18T04:21:29.577552+00:00", "level": "INFO", "event_type": "DRY_RUN_PASS", "runbook": "runbooks/restart_service.sh", "service": "payment-svc"}
{"ts": "2026-06-18T04:21:29.578535+00:00", "level": "INFO", "event_type": "RUNBOOK_EXEC", "script": "runbooks/restart_service.sh", "service": "payment-svc", "dry_run": false}
{"ts": "2026-06-18T04:21:38.949015+00:00", "level": "INFO", "event_type": "RUNBOOK_RESULT", "script": "runbooks/restart_service.sh", "service": "payment-svc", "returncode": 0, "stdout": "[restart_service] Restarting ronki-payment-svc...\nronki-payment-svc\n[restart_service] Waiting 5s for ronki-payment-svc to come up...\n[restart_service] ronki-payment-svc is running.", "stderr": ""}
{"ts": "2026-06-18T04:21:38.949015+00:00", "level": "INFO", "event_type": "ACTION_EXECUTED", "runbook": "runbooks/restart_service.sh", "service": "payment-svc"}
{"ts": "2026-06-18T04:21:38.949015+00:00", "level": "INFO", "event_type": "VERIFY_START", "service": "payment-svc", "timeout_s": 60}
{"ts": "2026-06-18T04:21:38.982741+00:00", "level": "INFO", "event_type": "VERIFY_SAMPLE", "service": "payment-svc", "sample": 1, "latency_p99_ms": 248.2608695652174, "up": 0.0, "latency_ok": true, "up_ok": false}
{"ts": "2026-06-18T04:21:49.003243+00:00", "level": "INFO", "event_type": "VERIFY_SAMPLE", "service": "payment-svc", "sample": 2, "latency_p99_ms": 248.19832402234636, "up": 1.0, "latency_ok": true, "up_ok": true}
{"ts": "2026-06-18T04:21:59.022864+00:00", "level": "INFO", "event_type": "VERIFY_SAMPLE", "service": "payment-svc", "sample": 3, "latency_p99_ms": 248.17062314540058, "up": 1.0, "latency_ok": true, "up_ok": true}
{"ts": "2026-06-18T04:22:09.048326+00:00", "level": "INFO", "event_type": "VERIFY_SAMPLE", "service": "payment-svc", "sample": 4, "latency_p99_ms": 248.1619718309859, "up": 1.0, "latency_ok": true, "up_ok": true}
{"ts": "2026-06-18T04:22:09.048326+00:00", "level": "INFO", "event_type": "VERIFY_PASS", "service": "payment-svc", "samples": 4}
{"ts": "2026-06-18T04:22:09.049846+00:00", "level": "INFO", "event_type": "ACTION_SUCCESS", "alertname": "HighLatency", "service": "payment-svc", "runbook": "runbooks/restart_service.sh"}
```

**Kết quả:** PASS. p99 latency của payment-svc nằm trong ngưỡng cho phép. Xác minh thành công (verify pass) sau khi uvicorn khởi động lại thành công và đạt 3 mẫu liên tiếp có trạng thái healthy.

---

## Scenario 2 — Action fail → rollback (checkout-svc killed, threshold thấp)

**Thiết lập:** Đặt tạm `verify_thresholds.latency_p99_max_ms: 1` trong `baseline.json` để verify luôn thất bại.

**Lệnh inject (PowerShell):**
```powershell
docker stop ronki-checkout-svc
```

**Log orchestrator:**
```json
{"ts": "2026-06-18T04:53:34.110374+00:00", "level": "INFO", "event_type": "ALERT_DETECTED", "alertname": "InstanceDown", "service": "checkout-svc", "severity": "critical"}
{"ts": "2026-06-18T04:53:34.110374+00:00", "level": "INFO", "event_type": "DECIDE_RUNBOOK", "alertname": "InstanceDown", "service": "checkout-svc", "runbook": "runbooks/restart_service.sh"}
{"ts": "2026-06-18T04:53:34.110374+00:00", "level": "INFO", "event_type": "BLAST_RADIUS_OK", "service": "checkout-svc"}
{"ts": "2026-06-18T04:53:34.111383+00:00", "level": "INFO", "event_type": "RUNBOOK_EXEC", "script": "runbooks/restart_service.sh", "service": "checkout-svc", "dry_run": true}
{"ts": "2026-06-18T04:53:34.198655+00:00", "level": "INFO", "event_type": "RUNBOOK_RESULT", "script": "runbooks/restart_service.sh", "service": "checkout-svc", "returncode": 0, "stdout": "[DRY-RUN] would execute: docker restart ronki-checkout-svc", "stderr": ""}
{"ts": "2026-06-18T04:53:34.198655+00:00", "level": "INFO", "event_type": "DRY_RUN_PASS", "runbook": "runbooks/restart_service.sh", "service": "checkout-svc"}
{"ts": "2026-06-18T04:53:34.199032+00:00", "level": "INFO", "event_type": "RUNBOOK_EXEC", "script": "runbooks/restart_service.sh", "service": "checkout-svc", "dry_run": false}
{"ts": "2026-06-18T04:53:41.636354+00:00", "level": "INFO", "event_type": "RUNBOOK_RESULT", "script": "runbooks/restart_service.sh", "service": "checkout-svc", "returncode": 0, "stdout": "[restart_service] Restarting ronki-checkout-svc...\nronki-checkout-svc\n[restart_service] Waiting 5s for ronki-checkout-svc to come up...\n[restart_service] ronki-checkout-svc is running.", "stderr": ""}
{"ts": "2026-06-18T04:53:41.636354+00:00", "level": "INFO", "event_type": "ACTION_EXECUTED", "runbook": "runbooks/restart_service.sh", "service": "checkout-svc"}
{"ts": "2026-06-18T04:53:41.636863+00:00", "level": "INFO", "event_type": "VERIFY_START", "service": "checkout-svc", "timeout_s": 20}
{"ts": "2026-06-18T04:53:41.713982+00:00", "level": "INFO", "event_type": "VERIFY_SAMPLE", "service": "checkout-svc", "sample": 1, "latency_p99_ms": null, "up": 1.0, "latency_ok": false, "up_ok": true}
{"ts": "2026-06-18T04:53:46.748721+00:00", "level": "INFO", "event_type": "VERIFY_SAMPLE", "service": "checkout-svc", "sample": 2, "latency_p99_ms": null, "up": 1.0, "latency_ok": false, "up_ok": true}
{"ts": "2026-06-18T04:53:51.768872+00:00", "level": "INFO", "event_type": "VERIFY_SAMPLE", "service": "checkout-svc", "sample": 3, "latency_p99_ms": null, "up": 1.0, "latency_ok": false, "up_ok": true}
{"ts": "2026-06-18T04:53:56.797943+00:00", "level": "INFO", "event_type": "VERIFY_SAMPLE", "service": "checkout-svc", "sample": 4, "latency_p99_ms": null, "up": 1.0, "latency_ok": false, "up_ok": true}
{"ts": "2026-06-18T04:54:01.799137+00:00", "level": "WARNING", "event_type": "VERIFY_FAIL", "service": "checkout-svc", "samples": 4}
{"ts": "2026-06-18T04:54:01.799137+00:00", "level": "WARNING", "event_type": "ROLLBACK_TRIGGERED", "service": "checkout-svc", "rollback_runbook": "runbooks/restart_service.sh"}
{"ts": "2026-06-18T04:54:01.799137+00:00", "level": "INFO", "event_type": "RUNBOOK_EXEC", "script": "runbooks/restart_service.sh", "service": "checkout-svc", "dry_run": false}
{"ts": "2026-06-18T04:54:09.909520+00:00", "level": "INFO", "event_type": "RUNBOOK_RESULT", "script": "runbooks/restart_service.sh", "service": "checkout-svc", "returncode": 0, "stdout": "[restart_service] Restarting ronki-checkout-svc...\nronki-checkout-svc\n[restart_service] Waiting 5s for ronki-checkout-svc to come up...\n[restart_service] ronki-checkout-svc is running.", "stderr": ""}
{"ts": "2026-06-18T04:54:09.909520+00:00", "level": "INFO", "event_type": "ROLLBACK_EXECUTED", "service": "checkout-svc", "rollback_runbook": "runbooks/restart_service.sh"}
```

**Kết quả:** PASS (Kiểm thử cơ chế rollback). Do latency của checkout-svc > 1ms, bước xác minh bị thất bại (`VERIFY_FAIL`). Orchestrator đã tự động kích hoạt tiến trình hoàn tác (`ROLLBACK_TRIGGERED`) và hoàn thành chạy runbook rollback (`ROLLBACK_EXECUTED`).

---

## Scenario 3 — Circuit breaker (3 consecutive failures)

**Thiết lập:** Giữ nguyên threshold thấp. Bơm 3 alert liên tiếp đồng thời để tạo ra 3 lần verify thất bại liên tục.

**Log orchestrator:**
```json
... (Lần thất bại 1 ở checkout-svc)
{"ts": "2026-06-18T04:56:04.004447+00:00", "level": "WARNING", "event_type": "VERIFY_FAIL", "service": "checkout-svc", "samples": 4}
{"ts": "2026-06-18T04:56:04.004447+00:00", "level": "WARNING", "event_type": "ROLLBACK_TRIGGERED", "service": "checkout-svc", "rollback_runbook": "runbooks/restart_service.sh"}
{"ts": "2026-06-18T04:56:12.661615+00:00", "level": "INFO", "event_type": "ROLLBACK_EXECUTED", "service": "checkout-svc", "rollback_runbook": "runbooks/restart_service.sh"}

... (Lần thất bại 2 ở payment-svc)
{"ts": "2026-06-18T04:56:58.340143+00:00", "level": "WARNING", "event_type": "VERIFY_FAIL", "service": "payment-svc", "samples": 4}
{"ts": "2026-06-18T04:56:58.340143+00:00", "level": "WARNING", "event_type": "ROLLBACK_TRIGGERED", "service": "payment-svc", "rollback_runbook": "runbooks/restart_service.sh"}
{"ts": "2026-06-18T04:57:07.914197+00:00", "level": "INFO", "event_type": "ROLLBACK_EXECUTED", "service": "payment-svc", "rollback_runbook": "runbooks/restart_service.sh"}

... (Lần thất bại 3 ở inventory-svc)
{"ts": "2026-06-18T04:57:37.706481+00:00", "level": "WARNING", "event_type": "VERIFY_FAIL", "service": "inventory-svc", "samples": 4}
{"ts": "2026-06-18T04:57:37.706796+00:00", "level": "WARNING", "event_type": "ROLLBACK_TRIGGERED", "service": "inventory-svc", "rollback_runbook": "runbooks/restart_service.sh"}
{"ts": "2026-06-18T04:57:47.524633+00:00", "level": "INFO", "event_type": "ROLLBACK_EXECUTED", "service": "inventory-svc", "rollback_runbook": "runbooks/restart_service.sh"}
{"ts": "2026-06-18T04:57:47.524633+00:00", "level": "ERROR", "event_type": "CIRCUIT_BREAKER_HALT", "consecutive_failures": 3, "threshold": 3, "message": "Automation halted. Manual intervention required."}
```

**Kết quả:** PASS. Khi số lần lỗi liên tục chạm ngưỡng 3, bộ ngắt mạch tự động chuyển sang trạng thái ngắt kết nối (`CIRCUIT_BREAKER_HALT`) và đình chỉ mọi hành động tự động sửa lỗi cho đến khi kỹ sư vào xử lý thủ công.

---

## Bài học kinh nghiệm

1.  **Hành vi đo lường trong Mock Service:** Quá trình đo latency của các Mock Service được thực hiện nội bộ trước khi trả ra socket. Do đó, việc dùng `tc` mạng chỉ ảnh hưởng thời gian phản hồi thực tế mà client nhận được chứ không làm tăng chỉ số metric `http_request_duration_seconds_bucket` nội bộ. Ta đã khắc phục bằng cách gửi synthetic alerts hoặc hạ thấp ngưỡng verify của hệ thống để kiểm thử toàn diện logic điều phối.
2.  **Môi trường Windows và Bash:** Các script runbook cần được chạy chính xác thông qua Git Bash (`C:\Program Files\Git\bin\bash.exe`) trên Windows. Code điều phối đã được tinh chỉnh để tự động phát hiện và chuyển đổi trình biên dịch phù hợp giữa Linux (`/bin/bash`) và Windows.
