from src import create_app

# Starts the service
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
