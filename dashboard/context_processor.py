import requests
from datetime import datetime

LAB_SCHEDULE = {
    "start": 9,
    "end": 16
}

def global_violation(request):

    GRID_ID="3253852"
    GRID_KEY="XXAUYZ6KWYFA4HW0"

    UPS_ID="3253853"
    UPS_KEY="YYYJG1N08XMA7FSE"

    try:
        u=requests.get(
            f"https://api.thingspeak.com/channels/{UPS_ID}/feeds/last.json?api_key={UPS_KEY}",
            timeout=5
        ).json()
    except:
        u={}

    def safe(x):
        try:
            return float(x)
        except:
            return 0.0

    u_power = safe(u.get("field3"))

    current_hour = datetime.now().hour
    violation = False

    if current_hour < LAB_SCHEDULE["start"] or current_hour >= LAB_SCHEDULE["end"]:
        if u_power > 5:
            violation = True

    return {
        "violation": violation
    }