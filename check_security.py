import easyocr
import re

# ─── 🛡️ Step 1: Mock Blacklist Database ───
# In real-world production, this data would be fetched from cloud APIs or law enforcement databases.
blacklist_accounts = [
    "2022121882y36vagkrhak51",  # Example blacklisted transaction ID associated with fraud history
    "1234567890",
    "นายสมชาย หมายจับ"
]

# ─── 🤖 Step 2: Run OCR Model to Scan Slip ───
reader = easyocr.Reader(['th', 'en'])
image_path = 'Slip_test1.png' 

print("Running Cybersecurity Verification System...")
results = reader.readtext(image_path, detail=0)
full_text = " ".join(results)

# Extract amount and reference ID
amount_match = re.search(r'\d+\.\d{2}', full_text)
amount = amount_match.group(0) if amount_match else "0.00"

ref_match = re.search(r'[A-Za-z0-9]{10,}', full_text)
ref_id = ref_match.group(0) if ref_match else "Not_Found"

# ─── 🕵️‍♂️ Step 3: Risk Assessment Engine ───
risk_score = 0
security_alerts = []

# Rule 1: Basic slip validation based on amount (Business Logic)
if float(amount) <= 0:
    risk_score += 50
    security_alerts.append("❌ Invalid or zero amount detected (High risk of fake slip)")

# Rule 2: Check against Blacklist Database (Cybersecurity Rule)
if ref_id in blacklist_accounts:
    risk_score += 100
    security_alerts.append("🚨 Transaction ID matches a known mule account or fraud entry!")
else:
    # Rule 3: Validate reference code integrity (Anomaly Detection)
    if len(ref_id) < 15:
        risk_score += 30
        security_alerts.append("⚠️ Abnormally short Reference ID (Possible image tampering)")

# Evaluate overall security status
if risk_score >= 80:
    status = "🔴 High Risk - Hold order fulfillment immediately"
elif risk_score >= 30:
    status = "🟡 Medium Risk - Manual bank app verification required"
else:
    status = "🟢 Low Risk - Transaction passed all security rules"

# ─── 📊 Executive Risk Assessment Report ───
print("\n==============================================")
print("🛡️ [Financial Threat Assessment Report]")
print("==============================================")
print(f"💰 Extracted Amount: {amount} THB")
print(f"🆔 Reference ID:     {ref_id}")
print(f"📊 Risk Score:       {risk_score} / 100")
print(f"📢 System Status:    {status}")
print("----------------------------------------------")
print("🔍 Detection Details:")
if security_alerts:
    for alert in security_alerts:
        print(f"   {alert}")
else:
    print("   ✅ No anomalies found in threat database")
print("==============================================")