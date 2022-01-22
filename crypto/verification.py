from OpenSSL import SSL
from twisted.internet import ssl


class VerificationFactory(ssl.DefaultOpenSSLContextFactory):

    def __init__(self, private_key_file_name, certificate_file_name):
        super().__init__(private_key_file_name, certificate_file_name)


def verify(connection, x509, err_num, err_depth, ok):
    if not ok:
        print(err_depth, err_num)
        print('invalid cert from subject:', x509.get_subject())
        return False
    return True


def init_verification(factory):
    vrt_check = VerificationFactory(
        'server_data/{}.key'.format(factory.key_name),
        'server_data/{}.crt'.format(factory.key_name)
    )

    certificate = vrt_check.getContext()

    certificate.set_verify(
        SSL.VERIFY_PEER | SSL.VERIFY_FAIL_IF_NO_PEER_CERT,
        verify
        )

    certificate.load_verify_locations(
        'KeysModule/server_data/{}_ca.crt'.format(factory.key_name)
        )
    return vrt_check
