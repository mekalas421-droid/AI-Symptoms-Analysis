import urllib.request, json

base_url = 'http://127.0.0.1:8000'
email = 'testflow3@example.com'
pwd = 'Password123'

# Register
req = urllib.request.Request(f'{base_url}/api/v1/auth/register', json.dumps({
    'email': email, 'password': pwd, 'full_name': 'Test Flow3', 'role': 'patient', 'phone_number': '+1234567890'
}).encode('utf-8'), {'Content-Type': 'application/json'})
try:
    urllib.request.urlopen(req)
except Exception:
    pass

# Login
req = urllib.request.Request(f'{base_url}/api/v1/auth/login', json.dumps({
    'email': email, 'password': pwd
}).encode('utf-8'), {'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req) as f:
        token = json.loads(f.read().decode())['access_token']
except Exception as e:
    print('Login failed:', e.read().decode())
    exit(1)

# Get Symptom
req = urllib.request.Request(f'{base_url}/api/v1/symptoms')
with urllib.request.urlopen(req) as f:
    syms = json.loads(f.read().decode())
    s_id = syms[0]['id']

# Submit
submit_req = urllib.request.Request(
    f'{base_url}/api/v1/symptoms/submit',
    json.dumps({
        'symptoms': [{'symptom_id': s_id, 'severity': 'mild', 'duration_value': 1, 'duration_unit': 'days'}],
        'free_text_notes': 'Test notes'
    }).encode('utf-8'),
    {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
)
try:
    with urllib.request.urlopen(submit_req) as f:
        res = json.loads(f.read().decode())
        print('Submit success:', res)
        sub_id = res['id']
except urllib.error.HTTPError as e:
    print('Submit failed:', e.code, e.read().decode())
    exit(1)

# Predict
pred_req = urllib.request.Request(f'{base_url}/api/v1/diagnostics/predict/{sub_id}', method='POST', headers={'Authorization': f'Bearer {token}'})
try:
    with urllib.request.urlopen(pred_req) as f:
        res = json.loads(f.read().decode())
        print('Predict success:', res)
except urllib.error.HTTPError as e:
    print('Predict failed:', e.code, e.read().decode())
