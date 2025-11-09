import asyncio
from app import create_app

app = asyncio.run(create_app())

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)