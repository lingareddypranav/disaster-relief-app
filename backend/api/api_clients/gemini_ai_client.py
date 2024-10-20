# api/api_clients/gemini_ai_client.py

import google.generativeai as genai
from django.conf import settings

class GeminiAIClient:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_AI_API_KEY)

    def generate_resource_allocation(self, prompt):
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.2,
                max_output_tokens=1024,
                candidate_count=1,
            ),
        )

        # Print the raw response for debugging
        print("Gemini AI API Response:")
        print(response.text)

        return response.text
