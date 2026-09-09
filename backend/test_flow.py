import urllib.request, urllib.parse, json

# 1. Register
email = "testflow@example.com"
pwd = "Password123"
data = json.dumps({
    "email": email,
    "password": pwd,
    "full_name": "Test Flow",
    "role": "patient",
    "phone_number": "+1234567890"
}).encode("utf-8")
req = urllib.request.Request("http://127.0.0.1:8000/api/v1/auth/register", data=data, headers={"Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req) as f:
        res = json.loads(f.read().decode())
        print("Register:", res)
except Exception as e:
    print("Register failed, maybe already exists")

# 2. Login
data = urllib.parse.urlencode({"username": email, "password": pwd}).encode("utf-8")
req = urllib.request.Request("http://127.0.0.1:8000/api/v1/auth/login", data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
try:
    with urllib.request.urlopen(req) as f:
        token_data = json.loads(f.read().decode())
        token = token_data["access_token"]
        print("Logged in")
except Exception as e:
    print("Login failed:", e)
    exit(1)

# 3. Get Symptoms
req = urllib.request.Request("http://127.0.0.1:8000/api/v1/symptoms")
with urllib.request.urlopen(req) as f:
    syms = json.loads(f.read().decode())
    s_id = syms[0]["id"]
    print("Got symptom:", s_id)

# 4. Submit
data = json.dumps({
    "symptoms": [{"symptom_id": s_id}],
    "free_text_notes": "Test"
}).encode("utf-8")
req = urllib.request.Request("http://127.0.0.1:8000/api/v1/symptoms/submit", data=data, headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})
try:
    with urllib.request.urlopen(req) as f:
        res = json.loads(f.read().decode())
        print("Submit success:", res)
except urllib.error.HTTPError as e:
    print("Submit failed:", e.code, e.read().decode())

