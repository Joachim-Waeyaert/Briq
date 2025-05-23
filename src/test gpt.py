import openai
import random

# API-sleutel voor OpenAI
openai.api_key = 'YOUR_API_KEY'

# Functie om een willekeurige vraag te genereren
def genereer_vraag(onderwerp="algemene kennis"):
    prompt = f"Genereer een vraag over {onderwerp}."
    response = openai.Completion.create(
        engine="text-davinci-003",  # Gebruik de GPT-3 of GPT-4 engine
        prompt=prompt,
        max_tokens=50,
        temperature=0.7
    )
    vraag = response.choices[0].text.strip()
    return vraag

# Voorbeeldvraag genereren
vraag = genereer_vraag("sport")
print("Vraag:", vraag)
