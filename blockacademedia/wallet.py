from util_crypto import generate_keys, sign_message



class Wallet:
    """
    Simple wallet that holds an RSA key pair.
    We will use one Wallet instance for Ontario Tech (issuer),
    and we could create others for students if needed.
    """

    def __init__(self, name: str):
        # Human-readable name (e.g., "Ontario Tech University")
        self.name = name

        # Generate private/public RSA keys
        self.private_key, self.public_key = generate_keys()

    def sign(self, message: str) -> str:
        """
        Sign an arbitrary string using this wallet's private key.
        Used to produce digital signatures over credential hashes.
        """
        return sign_message(self.private_key, message)
