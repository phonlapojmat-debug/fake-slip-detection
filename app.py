import streamlit as st
import easyocr
import re
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="Anti-Fraud Slip Dashboard", page_icon="🛡️", layout="wide")

st.title("🛡️ Fake Slip & Mule Account Risk Management Platform")
st.write("An intelligent AI system for enterprise financial threat verification.")

# 2. Mock Blacklist Database (Normalized to lowercase)
blacklist_accounts = ["2022121882y36vagkrhgk5l", "1234567890"]

# Load AI model (Cached to prevent reloading on every rerun)
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['th', 'en'])

reader = load_ocr()

# 3. File Upload UI
uploaded_file = st.file_uploader("📂 Upload bank slip image for verification (.jpg, .jpeg, .png)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.image(image, caption="Uploaded Slip Image", use_container_width=True)
        
    with col2:
        with st.spinner("🤖 AI is analyzing image structure and threat database..."):
            # Save temporary file and convert to RGB to prevent RGBA channel bugs
            temp_path = "temp_uploaded_slip.jpg"
            image.convert('RGB').save(temp_path)
            
            results = reader.readtext(temp_path, detail=0)
            full_text = " ".join(results)
            
            # Extract data using Regular Expressions (Regex)
            amount_match = re.search(r'\d+\.\d{2}', full_text)
            amount = amount_match.group(0) if amount_match else "0.00"
            
            ref_match = re.search(r'[A-Za-z0-9]{10,}', full_text)
            ref_id = ref_match.group(0) if ref_match else "Not_Found"
            
            # 🛡️ Improved Risk Assessment Engine (String Normalization)
            risk_score = 0
            security_alerts = []
            
            if float(amount) <= 0:
                risk_score += 50
                security_alerts.append("❌ Invalid or zero amount detected")
            
            # Convert extracted text to lowercase before matching
            ref_id_clean = ref_id.lower()
            
            is_blacklisted = False
            for black_id in blacklist_accounts:
                # Check only the first 15 characters to bypass trailing OCR noise
                if black_id[:15] in ref_id_clean:
                    is_blacklisted = True
                    break
            
            if is_blacklisted:
                risk_score += 100
                security_alerts.append("🚨 Transaction ID matches a known mule account database!")
            else:
                if len(ref_id) < 15:
                    risk_score += 30
                    security_alerts.append("⚠️ Abnormally short Reference ID (Possible image manipulation)")
            
            # 📊 Display Summary Metrics based on Risk Score
            st.subheader("📊 Deep Analytics Results")
            
            if risk_score >= 80:
                st.error(f"🔴 High Risk | Risk Score: {risk_score}/100")
                st.metric(label="System Recommendation", value="❌ Hold Transaction Immediately")
            elif risk_score >= 30:
                st.warning(f"🟡 Medium Risk | Risk Score: {risk_score}/100")
                st.metric(label="System Recommendation", value="🔍 Verify with Mobile Banking App")
            else:
                st.success(f"🟢 Low Risk | Risk Score: {risk_score}/100")
                st.metric(label="System Recommendation", value="✅ Passed Security Standards")
                
            st.markdown("---")
            c1, c2 = st.columns(2)
            c1.metric(label="💰 Extracted Amount", value=f"{amount} THB")
            c2.metric(label="🆔 Extracted Reference ID (Ref ID)", value=ref_id)
            
            if security_alerts:
                st.write("🔎 **Security Audit Findings:**")
                for alert in security_alerts:
                    st.write(alert)