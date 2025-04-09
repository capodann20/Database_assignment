from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel, Field
import motor.motor_asyncio
from fastapi.responses import JSONResponse

# Initialize the FastAPI app
app = FastAPI()

# MongoDB connection
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://<michelequispe15>:<margoux1926>@cluster.mongodb.net/databaseAssignment?retryWrites=true&w=majority")
db = client.databaseAssignment

# Pydantic models for input validation
class PlayerScore(BaseModel):
    player_name: str = Field(..., min_length=1, max_length=50, description="name of the player")
    score: int = Field(..., gt=0, description="The player's score")

# Endpoint: Upload a Sprite
@app.post("/upload_sprite")
async def upload_sprite(file: UploadFile = File(...)):
    try:
        content = await file.read()
        sprite_doc = {"filename": file.filename, "content": content}
        result = await db.sprites.insert_one(sprite_doc)
        return {"message": "Sprite uploaded", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to upload sprite. Error: " + str(e))

# Endpoint: Upload an Audio File
@app.post("/upload_audio")
async def upload_audio(file: UploadFile = File(...)):
    try:
        content = await file.read()
        audio_doc = {"filename": file.filename, "content": content}
        result = await db.audio_files.insert_one(audio_doc)
        return {"message": "Audio file uploaded successfully", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to upload audio file. Error: " + str(e))

# Endpoint: Add Player Score
@app.post("/player_score")
async def add_score(score: PlayerScore):
    try:
        score_doc = score.dict()
        result = await db.player_scores.insert_one(score_doc)
        return {"message": "Score recorded successfully", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to record player score. Error: " + str(e))

# Endpoint: Get All Scores
@app.get("/player_scores")
async def get_scores():
    try:
        scores = await db.player_scores.find().to_list(100)
        return {"scores": scores}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch player scores. Error: " + str(e))

# Endpoint: Health Check (Optional)
@app.get("/")
async def root():
    return {"message": "Testing API."}