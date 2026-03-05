# ---------- Base Image ----------
FROM python:3.10-slim

# ---------- Set Working Directory ----------
WORKDIR /app

# ---------- Install System Dependencies ----------
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ---------- Copy Project ----------
COPY . .

# ---------- Install Dependencies ----------
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# ---------- Expose Port ----------
EXPOSE 8501

# ---------- Run Backend ----------
CMD ["python", "app/main.py"]