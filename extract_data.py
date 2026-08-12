import easyocr
import re

reader = easyocr.Reader(['th', 'en'])

# Specify your slip image file path here
image_path = 'Slip_test1.png' 

print("Analyzing and extracting data from the slip...")
results = reader.readtext(image_path, detail=0)

# Merge all extracted text into a single string for easier pattern matching
full_text = " ".join(results)

# ─── 🤖 Extract Key Information using Regular Expressions (Regex) ───

# 1. Extract Amount: Find a number with 2 decimal places (e.g., 843.00)
amount_match = re.search(r'\d+\.\d{2}', full_text)
amount = amount_match.group(0) if amount_match else "Amount not found"

# 2. Extract Reference ID or Transaction Code (if available)
# Matches alphanumeric strings with at least 10 characters (e.g., kps004k...)
ref_match = re.search(r'[A-Za-z0-9]{10,}', full_text)
ref_id = ref_match.group(0) if ref_match else "Transaction ID not found"

# ─── 📊 Display Results for Backend Processing ───
print("\n======================================")
print("🤖 [Backend Data Extraction Results]")
print("======================================")
print(f"💰 Extracted Amount: {amount} THB")
print(f"🆔 Reference ID:      {ref_id}")
print("======================================")
print("📌 Status: Ready to send these values to Bank API or Mule Account Database for verification.")