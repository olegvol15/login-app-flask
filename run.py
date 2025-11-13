from dotenv import load_dotenv

load_dotenv()  # загружаем .env в os.environ

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()

