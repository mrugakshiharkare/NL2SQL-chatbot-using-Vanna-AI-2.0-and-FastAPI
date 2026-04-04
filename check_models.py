import google.generativeai as genai

#Use the same API key as in vanna_setup.py
genai.configure(api_key='AIzaSyB-no9NumYuHYvxSTTqtGn6MYhJsU4aiVE')
print("Listing available Gemini models for API key...")

try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Model: {m.name}")
except Exception as e:
    print(f"Error: {e}")