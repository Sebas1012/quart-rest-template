from tortoise import Tortoise
from tortoise.contrib.quart import register_tortoise

tortoise_configured = False

def init_db(app, db_url: str):
    global tortoise_configured
    if not tortoise_configured:
        register_tortoise(
            app,
            db_url=db_url,
            modules={"models": ["app.models.login"]},
            generate_schemas=True,
        )
        tortoise_configured = True