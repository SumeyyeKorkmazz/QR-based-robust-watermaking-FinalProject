FROM node:20-alpine

WORKDIR /app

# Paket dosyalarını kopyala ve kurulum yap
COPY package.json package-lock.json* ./
RUN npm install

# Kalan tüm dosyaları kopyala
COPY . .

# Vite'ı herkesin erişimine aç
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
