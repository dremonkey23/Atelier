FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY atelier_faq_bot ./atelier_faq_bot
CMD ["python", "-m", "atelier_faq_bot"]
