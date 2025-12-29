from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

app = FastAPI(title="Darija Sentiment API")

MODEL_NAME = "BenhamdaneNawfal/sentiment-analysis-darija"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

LABELS = {
    0: "Negative",
    1: "Positive"
}

class TextInput(BaseModel):
    text: str

@app.post("/sentiment/darija")
def analyze_sentiment(data: TextInput):

    inputs = tokenizer(
        data.text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    with torch.no_grad():
        outputs = model(**inputs)

    predicted_class = outputs.logits.argmax(dim=1).item()

    return {
        "text": data.text,
        "sentiment": LABELS[predicted_class],
        "class_id": predicted_class
    }
