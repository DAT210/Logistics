from src import create_app

app = create_app('prod')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')