import nacl.signing
import nacl.exceptions
import pickle


class Signature:
    def __init__(self):
        self.client_verify_keys = None
        self.replica_verify_keys = None
        self.olympus_verify_key = None

    @staticmethod
    def generate_keys(count):
        signing_keys = {}
        verifying_keys = {}
        for id_ in range(1, count + 1):
            signing_keys[id_] = nacl.signing.SigningKey.generate()
            verifying_keys[id_] = signing_keys[id_].verify_key
        return signing_keys, verifying_keys

    def generate_client_keys(self, client_count):
        sign_keys, verify_keys = self.generate_keys(client_count)
        self.client_verify_keys = verify_keys
        return sign_keys

    def generate_replica_keys(self, replica_count):
        sign_keys, verify_keys = self.generate_keys(replica_count)
        self.replica_verify_keys = verify_keys
        return sign_keys

    def generate_olympus_keys(self):
        sign_key = nacl.signing.SigningKey.generate()
        verify_key = sign_key.verify_key
        self.olympus_verify_key = verify_key
        return sign_key

    # TODO: refactor
    def verify_replica(self, replica_id, signed_payload):
        try:
            if replica_id in self.replica_verify_keys:
                serialized_payload = self.replica_verify_keys[replica_id].verify(signed_payload)
                deserialized_payload = pickle.loads(serialized_payload)
                return True, deserialized_payload
            return False, None
        except nacl.exceptions.BadSignatureError:
            return False, None

    def verify_client(self, client_id, signed_payload):
        try:
            if client_id in self.client_verify_keys:
                serialized_payload = self.client_verify_keys[client_id].verify(signed_payload)
                deserialized_payload = pickle.loads(serialized_payload)
                return True, deserialized_payload  # TODO: fix naming inconsistency
            return False, None
        except nacl.exceptions.BadSignatureError:
            return False, None
