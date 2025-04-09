from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import motor.motor_asyncio

app = FastAPI()

# Connect to Mongo Atlas
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://michelequispe15:italia@cluster.mongodb.net/databaseAssignment?retryWrites=true&w=majority")
db = client.databaseAssignment

class PlayerScore(BaseModel):
    player_name: str
    score: int

# POST: Upload Sprite
@app.post("/upload_sprite")
async def upload_sprite(file: UploadFile = File(...)):
    content = await file.read()
    sprite_doc = {"filename": file.filename, "content": content}
    result = await db.sprites.insert_one(sprite_doc)
    return {"message": "Sprite uploaded", "id": str(result.inserted_id)}

# POST: Upload Audio
@app.post("/upload_audio")
async def upload_audio(file: UploadFile = File(...)):
    content = await file.read()
    audio_doc = {"filename": file.filename, "content": content}
    result = await db.audio_files.insert_one(audio_doc)
    return {"message": "Audio file uploaded", "id": str(result.inserted_id)}

# POST: Add Player Score
@app.post("/player_score")
async def add_score(score: PlayerScore):
    score_doc = score.model_dump()
    result = await db.player_scores.insert_one(score_doc)
    return {"message": "Score recorded", "id": str(result.inserted_id)}

# GET: Retrieve All Sprites
@app.get("/sprites")
async def get_sprites():
    sprites = await db.sprites.find().to_list(100)
    return {"sprites": sprites}

# GET: Retrieve a Sprite by Filename
@app.get("/sprite/{filename}")
async def get_sprite(filename: str):
    sprite = await db.sprites.find_one({"filename": filename})
    if sprite:
        return {"sprite": sprite}
    raise HTTPException(status_code=404, detail="Sprite not found")

# PUT: Update Player Score
@app.put("/player_score/{player_name}")
async def update_score(player_name: str, score: int):
    result = await db.player_scores.update_one(
        {"player_name": player_name},
        {"$set": {"score": score}}
    )
    if result.modified_count == 1:
        return {"message": "Score updated"}
    raise HTTPException(status_code=404, detail="Player not found")

# DELETE: Remove a Sprite by Filename
@app.delete("/sprite/{filename}")
async def delete_sprite(filename: str):
    result = await db.sprites.delete_one({"filename": filename})
    if result.deleted_count == 1:
        return {"message": "Sprite deleted"}
    raise HTTPException(status_code=404, detail="Sprite not found")

@app.get("/")
async def root():
    return {"message": "Welcome to the Multimedia API! Use /docs to explore the endpoints."}
