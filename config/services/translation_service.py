from django.conf import settings
import requests

class TranslationService:
    def __init__(self):
        self.api_key = settings.GOOGLE_TRANSLATE_API_KEY
        self.url = "https://translation.googleapis.com/language/translate/v2"

    def translate_text(self, text, target_language):
        payload = {
            "q": text,
            "target": target_language,
            "format": "text",
            "key": self.api_key
        }
        response = requests.post(self.url, data=payload)
        result = response.json()
        return result['data']['translations'][0]['translatedText']
