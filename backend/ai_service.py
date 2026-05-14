import os
import requests
import uuid
from dotenv import load_dotenv
from openai import OpenAI
from fastapi import HTTPException

# Load environment variables
load_dotenv()

class AIGenerator:
    def __init__(self, upload_dir: str):
        self.upload_dir = upload_dir
        self.openai_client = None
        
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key and openai_key != "your_openai_api_key_here":
            self.openai_client = OpenAI(api_key=openai_key)
            
        self.hf_key = os.getenv("HUGGINGFACE_API_KEY")

    def download_image(self, url: str, filename: str) -> str:
        filepath = os.path.join(self.upload_dir, filename)
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return filepath
        raise Exception(f"Görsel indirilemedi. Hata kodu: {response.status_code}")

    def generate_dalle(self, prompt: str) -> str:
        if not self.openai_client:
            raise HTTPException(status_code=500, detail="OpenAI API anahtarı ayarlanmamış. Lütfen .env dosyasını kontrol edin.")
            
        try:
            response = self.openai_client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            image_url = response.data[0].url
            filename = f"temp_dalle_{uuid.uuid4().hex[:8]}.png"
            return self.download_image(image_url, filename)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"DALL-E üretimi başarısız: {str(e)}")

    def generate_stable_diffusion(self, prompt: str) -> str:
        if not self.hf_key or self.hf_key == "your_huggingface_api_key_here":
            raise HTTPException(status_code=500, detail="HuggingFace API anahtarı ayarlanmamış. Lütfen .env dosyasını kontrol edin.")
            
        API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
        headers = {"Authorization": f"Bearer {self.hf_key}"}
        
        try:
            response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
            if response.status_code != 200:
                raise Exception(f"API Hatası: {response.text}")
                
            filename = f"temp_sd_{uuid.uuid4().hex[:8]}.png"
            filepath = os.path.join(self.upload_dir, filename)
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return filepath
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Stable Diffusion üretimi başarısız: {str(e)}")

    def generate_image(self, prompt: str, model_name: str) -> str:
        """
        Model ismine göre uygun API'yi çağırır ve indirilen dosyanın yolunu döner.
        """
        model_lower = model_name.lower()
        if "dall-e" in model_lower or "dalle" in model_lower:
            return self.generate_dalle(prompt)
        elif "stable diffusion" in model_lower or "sd" in model_lower:
            return self.generate_stable_diffusion(prompt)
        else:
            raise HTTPException(status_code=400, detail=f"Desteklenmeyen model: {model_name}. Lütfen 'DALL-E' veya 'Stable Diffusion' seçin.")
