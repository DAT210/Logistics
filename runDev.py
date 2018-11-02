from src import create_app

# Starts the service for development
if __name__ == '__main__':
    app = create_app('dev')
    app.run(ssl_context='adhoc')
