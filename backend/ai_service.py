import os
import uuid
from dotenv import load_dotenv
from fastapi import HTTPException
from huggingface_hub import InferenceClient

# Load environment variables
load_dotenv()

class AIGenerator:
    def __init__(self, upload_dir: str):
        self.upload_dir = upload_dir
        self.hf_key = os.getenv("HUGGINGFACE_API_KEY")

    def generate_stable_diffusion(self, prompt: str) -> str:
        if not self.hf_key or self.hf_key == "your_huggingface_api_key_here":
            raise HTTPException(status_code=500,
                                detail="HuggingFace API anahtarı ayarlanmamış. Lütfen .env dosyasını kontrol edin.")

        try:
            # HuggingFace Inference API ile Stable Diffusion XL kullan
            client = InferenceClient(
                api_key=self.hf_key
            )

            # Gerçek Stable Diffusion XL modeli
            image = client.text_to_image(
                prompt,
                model="stabilityai/stable-diffusion-xl-base-1.0"
            )

            filename = f"temp_sd_{uuid.uuid4().hex[:8]}.png"
            filepath = os.path.join(self.upload_dir, filename)
            image.save(filepath)
            return filepath

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Stable Diffusion üretimi başarısız: {str(e)}")

    def generate_flux(self, prompt: str) -> str:
        if not self.hf_key or self.hf_key == "your_huggingface_api_key_here":
            raise HTTPException(status_code=500,
                                detail="HuggingFace API anahtarı ayarlanmamış. Lütfen .env dosyasını kontrol edin.")

        try:
            # HuggingFace Inference API ile FLUX.1-schnell kullan
            client = InferenceClient(
                provider="nscale",
                api_key=self.hf_key
            )

            image = client.text_to_image(
                prompt,
                model="black-forest-labs/FLUX.1-schnell"
            )

            filename = f"temp_flux_{uuid.uuid4().hex[:8]}.png"
            filepath = os.path.join(self.upload_dir, filename)
            image.save(filepath)
            return filepath

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"FLUX üretimi başarısız: {str(e)}")

    def generate_image(self, prompt: str, model_name: str) -> str:
        """
        Model ismine göre uygun API'yi çağırır ve indirilen dosyanın yolunu döner.
        """
        model_lower = model_name.lower()
        if "flux" in model_lower:
            return self.generate_flux(prompt)
        elif "stable diffusion" in model_lower or "sd" in model_lower:
            return self.generate_stable_diffusion(prompt)
        else:
            raise HTTPException(status_code=400, detail=f"Desteklenmeyen model: {model_name}. Lütfen 'Stable Diffusion' veya 'FLUX' seçin.")
