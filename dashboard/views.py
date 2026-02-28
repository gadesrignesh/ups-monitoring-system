from django.shortcuts import render
import requests
from datetime import datetime

# Lab allowed timing (24-hour format)
LAB_SCHEDULE = {
    "start": 9,   # 9 AM
    "end": 16     # 4 PM
}

def splash(request):
    return render(request, 'splash.html')

def home(request):
    return render(request, 'home.html')


# -----------------------------
# SAFE API FUNCTION
# -----------------------------
def fetch_thingspeak_data(channel_id, api_key):
    url = f"https://api.thingspeak.com/channels/{channel_id}/feeds/last.json?api_key={api_key}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        # Ensure it is always dictionary
        if isinstance(data, dict):
            return data
        else:
            return {}
    except:
        return {}


def ups1(request):

    GRID_ID = "3281912"
    GRID_KEY = "X3D4GSC2HB7Z5PWF"

    UPS_ID = "3281915"
    UPS_KEY = "LR0RTGQE4TC77OZA"

    # Fetch data safely
    g = fetch_thingspeak_data(GRID_ID, GRID_KEY)
    u = fetch_thingspeak_data(UPS_ID, UPS_KEY)

    # Safe float conversion
    def safe(value):
        try:
            return float(value)
        except:
            return 0.0

    # ---------------- GRID DATA ----------------
    g_voltage = safe(g.get("field1"))
    g_current = safe(g.get("field2"))
    g_power   = safe(g.get("field3"))
    g_energy  = safe(g.get("field4"))
    g_freq    = safe(g.get("field5"))
    g_pf      = safe(g.get("field6"))

    # ---------------- UPS DATA ----------------
    u_voltage = safe(u.get("field1"))
    u_current = safe(u.get("field2"))
    u_power   = safe(u.get("field3"))
    u_energy  = safe(u.get("field4"))
    u_freq    = safe(u.get("field5"))
    u_pf      = safe(u.get("field6"))

    battery = u_energy  # if energy represents battery %

    # ---------------- STATUS LOGIC ----------------
    if g_voltage > 10:
        status = "🟢 RUNNING ON GRID"
    elif u_voltage > 10:
        status = "🟠 RUNNING ON UPS"
    else:
        status = "🔴 POWER FAIL"

    # ---------------- CONTEXT ----------------
    context = {
        "g_voltage": round(g_voltage, 2),
        "g_current": round(g_current, 2),
        "g_power": round(g_power, 2),
        "g_energy": round(g_energy, 2),
        "g_frequency": round(g_freq, 1),
        "g_pf": round(g_pf, 2),

        "u_voltage": round(u_voltage, 2),
        "u_current": round(u_current, 2),
        "u_power": round(u_power, 2),
        "u_energy": round(u_energy, 2),
        "u_frequency": round(u_freq, 1),
        "u_pf": round(u_pf, 2),

        "battery": round(battery, 1),
        "status": status,
        "now": datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")
    }

    return render(request, "ups1.html", context)