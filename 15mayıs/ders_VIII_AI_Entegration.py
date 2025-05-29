import requests

api_key = "Your Google Gemini Key is here from https://aistudio.google.com/apikey"
api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

def gemini_soru_sor(soru):
    headers ={
        'Content-Type' : 'application/json'
    }
    data = {
        "contents": [{
           "parts": [{ "text": soru }] }]
    }

    try:
        response = requests.post(api_url,json=data,headers=headers)
        response.raise_for_status()
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except requests.exceptions.RequestException as e:
        print(f"Hata Oluştu : {e}")


soru = input("İstediğini sorabilirsin: :")
yanit = gemini_soru_sor(soru)

print()
print(yanit)
