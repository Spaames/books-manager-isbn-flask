from dotenv import dotenv_values
from src import create_app

app = create_app()
config_env = dotenv_values('.env')

if __name__ == '__main__':
    app.run(host=config_env.get("HOST"), port=config_env.get("PORT"), debug=config_env.get("DEBUG"))
