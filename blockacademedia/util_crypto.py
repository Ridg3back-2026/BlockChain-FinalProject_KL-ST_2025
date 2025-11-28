from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
import base64


def generate_keys():
    """
    Generate an RSA private/public key pair.
    Used for Ontario Tech (issuer) and any wallet.
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    return private_key, public_key


def sign_message(private_key, message: str) -> str:
    """
    Create a digital signature over `message` using the private key.
    Returns the signature as a base64 string.
    """
    signature = private_key.sign(
        message.encode("utf-8"),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return base64.b64encode(signature).decode("utf-8")


def verify_signature(public_key, message: str, signature: str) -> bool:
    """
    Verify that `signature` was created by the private key
    corresponding to `public_key` over `message`.
    """
    try:
        public_key.verify(
            base64.b64decode(signature.encode("utf-8")),
            message.encode("utf-8"),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False


def compute_hash(message: str) -> str:
    """
    Compute SHA-256 hash of a string and return it as hex.
    Used for credential hashes and block hashes.
    """
    digest = hashes.Hash(hashes.SHA256())
    digest.update(message.encode("utf-8"))
    return digest.finalize().hex()
