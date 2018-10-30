from src import create_app

app = create_app('prod')
# Starts the service
if __name__ == '__main__':
    app.run(host='0.0.0.0', ssl_context=('cert.pem', 'key.pem'))
