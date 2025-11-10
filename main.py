import asyncio
from app import create_app

app = asyncio.get_event_loop().run_until_complete(create_app())

# if __name__ == "__main__":
#     app.run(debug=True, use_reloader=True)