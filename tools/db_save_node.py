from database import save_review

async def save_node(state: dict) -> dict:
    try:
        await save_review(state)
    except Exception as e:
        print(f"DB save failed: {e}")
    return state
