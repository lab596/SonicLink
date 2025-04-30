from fastapi import FastAPI
from src.api import account, carts, catalog, bottler, barrels, info, inventory
from starlette.middleware.cors import CORSMiddleware

description = """
Central Coast Cauldrons is the premier ecommerce site for all your alchemical desires.
"""
tags_metadata = [
    {"name": "account", "description": "Create and get account information."},
    {"name": "tags", "description": "Create a tag for a user."},
    {"name": "users", "description": "User management interactions."},
    {"name": "lyrical-moments", "description": "Create a lyrical moment for a song."},
    {
        "name": "challenges",
        "description": "Create and manage challenges.",
    },
]

app = FastAPI(
    title="Sonic Link",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Lucas Pierce",
        "email": "lupierce@calpoly.edu",
    },
    openapi_tags=tags_metadata,
)

origins = ["https://potion-exchange.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(inventory.router)
app.include_router(carts.router)
app.include_router(catalog.router)
app.include_router(bottler.router)
app.include_router(barrels.router)
app.include_router(account.router)
app.include_router(info.router)


@app.get("/")
async def root():
    return {"message": "Are you ready to have a Sonic good time!"}
