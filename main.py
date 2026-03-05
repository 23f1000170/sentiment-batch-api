from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class SentimentRequest(BaseModel):
    sentences: List[str]

class SentimentResult(BaseModel):
    sentence: str
    sentiment: str

class SentimentResponse(BaseModel):
    results: List[SentimentResult]

def analyze_sentiment(sentence: str) -> str:
    text = sentence.lower()

    happy_words = [
        "love", "great", "amazing", "fantastic", "wonderful", "excellent",
        "happy", "joy", "excited", "awesome", "good", "best", "brilliant",
        "delightful", "pleased", "glad", "positive", "superb", "like",
        "enjoy", "beautiful", "perfect", "incredible", "outstanding",
        "yay", "wow", "thanks", "thank", "appreciate", "adore",
        "cheerful", "thrilled", "ecstatic", "grateful", "blessed",
        "fun", "smile", "laugh", "win", "winning", "success", "successful",
        "celebrate", "congratulations", "congrats", "proud",
        "hope", "hopeful", "optimistic", "inspiring", "inspired",
        "friendly", "kind", "generous", "warm", "caring", "sweet",
        "nice", "delight", "pleasure", "content", "satisfied",
        "peaceful", "calm", "relaxed", "refreshed", "energized",
        "relief", "relieved", "better", "improve"
    ]

    sad_words = [
        "hate", "terrible", "awful", "horrible", "bad", "worst", "sad",
        "upset", "angry", "disappointed", "depressed", "miserable", "crying",
        "poor", "unfortunate", "disgusting", "pathetic", "dreadful", "unhappy",
        "failure", "fail", "broken", "wrong", "problem", "hurt",
        "pain", "suffer", "loss", "lost", "difficult", "struggle",
        "worried", "anxious", "fear", "scared", "frustrated", "annoyed",
        "sorry", "regret", "shame", "embarrassed", "useless", "hopeless",
        "lonely", "alone", "empty", "numb", "tired", "exhausted", "sick",
        "weak", "helpless", "powerless", "stuck", "trapped",
        "despise", "resent", "bitter", "jealous",
        "rage", "furious", "mad", "irritated",
        "grief", "devastated", "heartbroken",
        "cry", "tears", "weep", "sorrow", "misery", "agony",
        "nightmare", "waste", "pointless", "meaningless"
    ]

    happy_count = sum(1 for word in happy_words if word in text)
    sad_count = sum(1 for word in sad_words if word in text)

    if happy_count > sad_count:
        return "happy"
    elif sad_count > happy_count:
        return "sad"
    else:
        return "neutral"

@app.post("/sentiment", response_model=SentimentResponse)
def sentiment_analysis(request: SentimentRequest):
    results = []
    for sentence in request.sentences:
        sentiment = analyze_sentiment(sentence)
        results.append(SentimentResult(sentence=sentence, sentiment=sentiment))
    return SentimentResponse(results=results)