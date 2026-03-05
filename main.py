from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

# Add this block ↓
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Step A: Define what the incoming data looks like ---
class SentimentRequest(BaseModel):
    sentences: List[str]

# --- Step B: Define what each result looks like ---
class SentimentResult(BaseModel):
    sentence: str
    sentiment: str

# --- Step C: Define what the full response looks like ---
class SentimentResponse(BaseModel):
    results: List[SentimentResult]

# --- Step D: The brain — keyword-based sentiment detection ---
def analyze_sentiment(sentence: str) -> str:
    text = sentence.lower()

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
        "celebrate", "celebration", "congratulations", "congrats", "proud",
        "hope", "hopeful", "optimistic", "inspiring", "inspired",
        "friendly", "kind", "generous", "warm", "caring", "sweet",
        "nice", "delight", "pleasure", "content", "satisfied", "comfortable",
        "peaceful", "calm", "relaxed", "refreshed", "energized", "alive",
        "free", "relief", "relieved", "better", "improve", "improving"
    ]
        sad_words = [
        "hate", "terrible", "awful", "horrible", "bad", "worst", "sad",
        "upset", "angry", "disappointed", "depressed", "miserable", "crying",
        "poor", "unfortunate", "disgusting", "pathetic", "dreadful", "unhappy",
        "failure", "fail", "broken", "wrong", "problem", "issue", "hurt",
        "pain", "suffer", "loss", "lost", "difficult", "hard", "struggle",
        "worried", "anxious", "fear", "scared", "frustrated", "annoyed",
        "sorry", "regret", "shame", "embarrassed", "useless", "hopeless",
        "lonely", "alone", "empty", "numb", "tired", "exhausted", "sick",
        "ill", "weak", "helpless", "powerless", "stuck", "trapped", "burden",
        "hate", "despise", "resent", "bitter", "jealous", "envy",
        "angry", "rage", "furious", "mad", "irritated", "annoyed",
        "grief", "grieve", "mourn", "mourning", "devastated", "heartbroken",
        "cry", "tears", "weep", "sorrow", "misery", "agony", "disaster",
        "horrible", "dreadful", "nightmare", "waste", "pointless", "meaningless"
    ]
        happy_count = sum(1 for word in happy_words if word in text)
        sad_count = sum(1 for word in sad_words if word in text)

        if happy_count > sad_count:
            return "happy"
        elif sad_count > happy_count:
            return "sad"
        else:
            return "neutral"

# --- Step E: The actual POST endpoint ---
@app.post("/sentiment", response_model=SentimentResponse)
def sentiment_analysis(request: SentimentRequest):
    results = []
    for sentence in request.sentences:
        sentiment = analyze_sentiment(sentence)
        results.append(SentimentResult(sentence=sentence, sentiment=sentiment))
    return SentimentResponse(results=results)