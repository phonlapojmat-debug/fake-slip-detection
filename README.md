# fake-slip-detection
# Fake Slip & Mule Account Risk Checker

A prototype that reads bank transfer slips (images) using OCR, pulls out the amount and reference ID, and checks them against a blacklist to flag suspicious transactions.

This is a demo/experimental project, not production-ready. The blacklist is hardcoded mock data.

## Files

- `app.py` — Streamlit web app. Upload a slip image, get amount/ref ID + risk score.
- `check_security.py` — CLI script, same logic as app.py but prints a report to terminal.
- `extract_data.py` — CLI script that just extracts amount + ref ID, no risk scoring.
- `test_ocr.py` — quick script to dump raw OCR text from an image, useful for debugging.
- `Slip_test1.png` — sample slip image for testing.

## Setup

```bash
pip install streamlit easyocr pillow
```

First run of easyocr will download the Thai/English models, takes a bit and needs disk space.

## Usage

Web app:
```bash
streamlit run app.py
```

CLI scripts (make sure `Slip_test1.png` is in the same folder, or edit the path in the script):
```bash
python test_ocr.py        # see raw OCR output
python extract_data.py    # extract amount + ref ID only
python check_security.py  # full check with risk score
```

## How it works

1. OCR (EasyOCR, th+en) reads text off the slip image.
2. Regex pulls out:
   - amount — number with 2 decimal places, e.g. `843.00`
   - ref ID — alphanumeric string, 10+ chars
3. Risk score:
   - amount is 0 or missing → +50
   - ref ID matches blacklist → +100
   - ref ID shorter than 15 chars (and not blacklisted) → +30
4. Score ≥80 = high risk, ≥30 = medium, below that = low.

## What I got out of building this

- Got hands-on with OCR (EasyOCR) on real Thai text, which turned out to be noticeably trickier than English — fonts, tone marks, and inconsistent spacing across different banks' slip formats all trip it up.
- Learned how fragile pure regex-based extraction is. The rules I wrote (must have 2 decimal places, ref ID must be 10+ chars) only really hold for the slip formats I tested against — different banks/apps break them easily.
- Got a clearer picture of how rule-based fraud scoring works in practice — fast to build and easy to reason about, but doesn't scale well once you hit edge cases you didn't anticipate.
- Practiced building an actual end-to-end pipeline: image in, processing, result out on a web UI (Streamlit) — a workflow pattern that's reusable across other projects.

## Where this could go next

- Hook up to a real blacklist source (bank or relevant authority data) instead of the hardcoded mock list.
- Make extraction more robust — per-bank template matching, or an NER model instead of plain regex.
- Add deeper image forensics (detecting signs of editing/tampering), not just reading text off the slip.
- Connect to a bank API to verify transaction status in real time, instead of relying on OCR alone.
- Add logging and a feedback loop for cases the system gets wrong, to refine the rules over time.
- Clean up the temp file created during processing (`temp_uploaded_slip.jpg`) after use, and tighten up input validation.
