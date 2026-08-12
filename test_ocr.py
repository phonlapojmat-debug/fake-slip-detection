import easyocr

# 1. Load Thai and English AI models into memory (it will be slow on the first run due to downloading).
reader = easyocr.Reader(['th', 'en'])

# 2. Put your slip image file name here (must be saved in the same folder as this code).
image_path = 'Slip_test1.png' 

print("AI is processing the slip image... Please wait a moment.")

# 3. Instruct the AI to extract all text from the image.
results = reader.readtext(image_path, detail=0)

# 4. Display the extracted text on the screen.
print("\n--- Text extracted by AI from the slip ---")
for text in results:
    print(text)