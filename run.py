from src import create_app

# Starts the service
if __name__ == '__main__':
    app = create_app('prod')
    app.run(host='0.0.0.0', ssl_context=('cert.pem', 'key.pem'))
