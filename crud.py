from models import Item
from sqlalchemy.future import select

async def get_items(db):
    result = await db.execute(select(Item))
    return result.scalars().all()

async def create_item(db, name: str):
    item = Item(name=name)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item

async def delete_item(db, item_id: int):
    item = await db.get(Item, item_id)
    if item:
        await db.delete(item)
        await db.commit()
    return item

async def update_item(db, item_id: int, name: str):
    item = await db.get(Item, item_id)
    if item:
        item.name = name
        await db.commit()
        await db.refresh(item)
    return item