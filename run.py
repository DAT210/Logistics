from src import create_app
from tools.setup import create_ssl_certificate

# Starts the service
if __name__ == '__main__':
    create_ssl_certificate()
    app = create_app('prod')
    app.run(host='0.0.0.0', ssl_context=('cert.pem', 'key.pem'))
