from src import create_app, create_api

app = create_app()
api = create_api(app)

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
