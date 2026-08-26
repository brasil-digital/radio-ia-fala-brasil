"""Narração via ElevenLabs — porta direta da chamada usada em
gerar-boletim.ps1 / gerar-programa.ps1 (voz clonada "Voz do Ronny").
"""
import json
import os

import requests

VOICE_ID = "EY32nkT8HLbeyhhUFVlv"  # Voz do Ronny
MODEL_ID = "eleven_multilingual_v2"
TTS_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}?output_format=mp3_44100_128"


def narrate_block(text: str, output_path: str) -> None:
    api_key = os.environ["ELEVENLABS_API_KEY"]

    body = {
        "text": text,
        "model_id": MODEL_ID,
        # Mesmos valores do gerar-programa.ps1 (blocos de programa longo,
        # não do gerar-boletim.ps1 que usa style mais alto pra boletins curtos).
        "voice_settings": {"stability": 0.7, "similarity_boost": 0.8, "style": 0.1},
    }

    dictionary_path = os.path.join(os.path.dirname(__file__), "dicionario-pronuncia.json")
    if os.path.exists(dictionary_path):
        with open(dictionary_path, "r", encoding="utf-8") as f:
            dic = json.load(f)
        body["pronunciation_dictionary_locators"] = [{
            "pronunciation_dictionary_id": dic["pronunciation_dictionary_id"],
            "version_id": dic["version_id"],
        }]

    resp = requests.post(
        TTS_URL,
        headers={"xi-api-key": api_key, "Content-Type": "application/json; charset=utf-8"},
        json=body,
        timeout=120,
    )
    resp.raise_for_status()

    with open(output_path, "wb") as f:
        f.write(resp.content)
