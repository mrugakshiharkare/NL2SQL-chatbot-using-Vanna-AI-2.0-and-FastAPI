import google.generativeai as genai

#Use the same API key as in vanna_setup.py
genai.configure(api_key='AIzaSyD_ZzUpMANuya4DzANN_K3KYh6wCnk7HZ8')
print("Listing available Gemini models for API key...")

try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Model: {m.name}")
except Exception as e:
    print(f"Error: {e}")