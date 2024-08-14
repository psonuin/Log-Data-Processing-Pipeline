import json
import random
from datetime import datetime, timedelta

# Generate 100 logs
log_entries = []
start_time = datetime.utcnow()

for i in range(100):
    log_entry = {
        "timestamp": (start_time - timedelta(minutes=i)).strftime('%Y-%m-%dT%H:%M:%SZ'),
        "log_level": random.choice(["INFO", "WARN", "ERROR"]),
        "user_id": str(random.randint(10000, 99999)),
        "request": random.choice([
            "GET /api/product/67890",
            "POST /api/order",
            "GET /api/user/12345",
            "DELETE /api/cart/45678",
            "PUT /api/review/98765"
        ]),
        "status_code": random.choice([200, 201, 400, 401, 403, 404, 500, 502, 503]),
        "response_time": random.randint(100, 1000)
    }
    log_entries.append(log_entry)

# Write the logs to a JSON file
with open('server_logs.json', 'w') as f:
    json.dump(log_entries, f, indent=4)
