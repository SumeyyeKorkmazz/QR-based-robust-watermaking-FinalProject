import os
from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime
import shutil
import uuid
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from pydantic import BaseModel

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "122858962930-068npvp8mfm1queehm4ouf9ijbga49s2.apps.googleusercontent.com")

from database import engine, get_db, Base
from models import User, GeneratedImage
from services import WatermarkService
from ai_service import AIGenerator
import schemas, auth
from fastapi.security import OAuth2PasswordRequestForm

# Veritabanı oluş
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TraceMark API")

# CORS (React frontend'in erişebilmesi için)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Geliştirme ortamı için hepsine izin ver
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Uploads kalsörü
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

watermark_svc = WatermarkService()
ai_generator = AIGenerator(UPLOAD_DIR)

@app.post("/api/auth/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="E-posta zaten kayıtlı.")
    hashed_password = auth.get_password_hash(user.password)
    db_user = User(email=user.email, full_name=user.full_name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/api/auth/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Hatalı e-posta veya şifre.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/auth/me", response_model=schemas.UserResponse)
def read_users_me(current_user: User = Depends(auth.get_current_user)):
    return current_user

class GoogleAuthRequest(BaseModel):
    credential: str

@app.post("/api/auth/google", response_model=schemas.Token)
def google_auth(payload: GoogleAuthRequest, db: Session = Depends(get_db)):
    """
    Google OAuth2 token'ını doğrular. Kullanıcı yoksa otomatik kayıt eder.
    Her iki durumda da kendi JWT token'ımızı döner.
    """
    try:
        # Google token'ını doğrula
        id_info = id_token.verify_oauth2_token(
            payload.credential,
            google_requests.Request(),
            GOOGLE_CLIENT_ID,
            clock_skew_in_seconds=10
        )
    except ValueError as e:
        raise HTTPException(status_code=401, detail=f"Geçersiz Google token: {str(e)}")

    email = id_info.get("email")
    full_name = id_info.get("name", "")

    if not email:
        raise HTTPException(status_code=400, detail="Google hesabından e-posta alınamadı.")

    # Kullanıcı var mı kontrol et, yoksa oluştur
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email, full_name=full_name, hashed_password=None)
        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/gallery", response_model=list[schemas.ImageResponse])
def get_gallery(current_user: User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    images = db.query(GeneratedImage).filter(GeneratedImage.owner_id == current_user.id).all()
    return images

@app.delete("/api/gallery/{image_id}")
def delete_image(image_id: int, current_user: User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    image = db.query(GeneratedImage).filter(GeneratedImage.id == image_id, GeneratedImage.owner_id == current_user.id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Görsel bulunamadı veya silme yetkiniz yok.")
    
    file_path = os.path.join(UPLOAD_DIR, image.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        
    db.delete(image)
    db.commit()
    return {"status": "success", "message": "Görsel başarıyla silindi."}

@app.post("/api/generate")
async def generate_image(
    prompt: str = Form(...),
    model_version: str = Form(...),
    quality_level: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_user)
):
    """
    Gerçek yapay zeka (DALL-E veya Stable Diffusion) ile resim üretir ve QR watermark gömer.
    JWT token ile korunan endpoint — giriş yapmış kullanıcılar erişebilir.
    """
    try:
        unique_id = str(uuid.uuid4())[:8]
        user_name = current_user.full_name or current_user.email
        date_str = datetime.utcnow().strftime('%d.%m.%Y | %H:%M')
        
        # Gerçek Yapay Zeka ile Görsel Üretimi
        cover_path = ai_generator.generate_image(prompt=prompt, model_name=model_version)
        
        # 1. QR Watermark uretimi
        qr_path = os.path.join(UPLOAD_DIR, f"qr_{unique_id}.png")
        watermark_svc.generate_qr_watermark(user_name, date_str, model_version, qr_path)
        
        # 2. Damgayi Gommek
        output_filename = f"watermarked_{unique_id}.png"
        output_path = os.path.join(UPLOAD_DIR, output_filename)
        
        watermark_svc.embed_watermark(cover_path, qr_path, output_path)
        
        # Yapay zekanın ürettiği orijinal (damgasız) geçici dosyayı silebiliriz
        if os.path.exists(cover_path):
            os.remove(cover_path)
        
        # DB'ye kaydet 
        new_image = GeneratedImage(
            filename=output_filename,
            prompt=prompt,
            ai_model=model_version,
            created_at=datetime.utcnow(),
            owner_id=current_user.id
        )
        db.add(new_image)
        db.commit()
        db.refresh(new_image)
        
        return {
            "status": "success", 
            "message": "Görsel başarıyla üretildi ve damgalandı.",
            "image_url": f"/api/images/{output_filename}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/extract")
async def extract_metadata(file: UploadFile = File(...)):
    """
    Kullanicinin yukledigi gorselden damgayi cozer ve QR bilgisini dondürür.
    """
    try:
        # Temp save uploaded file
        temp_path = os.path.join(UPLOAD_DIR, f"temp_{file.filename}")
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Metadata'yi cikarma islemi
        metadata_str = watermark_svc.extract_and_decode(temp_path)
        
        # Temp dosyayi silebiliriz
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        if metadata_str:
            # ornek QR verisi: "sumeyyekorkmaz|19.02.2026|Stable Diffusion"
            parts = metadata_str.split('|')
            producer = parts[0] if len(parts) > 0 else "Bilinmiyor"
            date = parts[1] if len(parts) > 1 else "Bilinmiyor"
            model = parts[2] if len(parts) > 2 else "Bilinmiyor"
            
            return {
                "status": "success",
                "verified": True,
                "data": {
                    "raw": metadata_str,
                    "creator": producer,
                    "date": date,
                    "model": model
                }
            }
        else:
            return {
                "status": "failed",
                "verified": False,
                "message": "Görselde herhangi bir damga (watermark) veya QR kodu bulunamadı."
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/images/{filename}")
async def get_image(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="Görsel bulunamadı")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
