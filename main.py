from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from database import SessionLocal, engine
from models import Base
from crud import get_items, create_item, delete_item, update_item

app = FastAPI()

# 👉 Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 👉 Создание таблиц при старте
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# 👉 Зависимость для получения сессии
async def get_db():
    async with SessionLocal() as session:
        yield session

@app.get("/items")
async def read_items(db: AsyncSession = Depends(get_db)):
    return await get_items(db)

@app.post("/items")
async def add_item(name: str, db: AsyncSession = Depends(get_db)):
    return await create_item(db, name)

@app.delete("/items/{item_id}")
async def remove_item(item_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_item(db, item_id)

@app.put("/items/{item_id}")
async def update_item_handler(item_id: int, name: str, db: AsyncSession = Depends(get_db)):
    return await update_item(db, item_id, name)