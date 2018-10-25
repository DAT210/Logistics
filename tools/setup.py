from OpenSSL import crypto, SSL
from os.path import join, exists
import random

# Creates ssl certificate to files, runs when run.py is called.
pubkey = 'cert.pem'
privkey = 'key.pem'
def create_ssl_certificate():
    if not exists(join('../', pubkey)) or not exists(join('../', privkey)):
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 2048)
        serialnumber = random.getrandbits(64)

        cert = crypto.X509()
        cert.get_subject().C = 'NO'
        cert.get_subject().ST = 'Rogaland'
        cert.get_subject().L = 'Stavanger'
        cert.get_subject().O = 'Dat210'
        cert.get_subject().OU = 'Group 5'
        cert.get_subject().CN = 'inventory'
        cert.set_serial_number(serialnumber)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(31536000)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, 'sha512')
        pub = crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
        priv = crypto.dump_privatekey(crypto.FILETYPE_PEM, k)
        open(join('../', pubkey), 'wt').write(pub.decode('utf-8'))
        open(join('../', privkey), 'wt').write(priv.decode('utf-8'))
