from util_crypto import compute_hash



class Credential:
    """
    Academic credential or micro-certification issued to a student.

    This object knows:
    - who the student is
    - what program / specialization
    - what type of credential (degree / micro-cert)
    - who issued it
    - the SHA-256 hash of those fields
    - the issuer's digital signature over that hash
    """

    def __init__(
        self,
        student_id: str,
        student_name: str,
        program: str,
        specialization: str,
        credential_type: str,   # e.g. "Degree" or "Micro-cert"
        issuer_name: str        # e.g. "Ontario Tech University"
    ):
        self.student_id = student_id
        self.student_name = student_name
        self.program = program
        self.specialization = specialization
        self.credential_type = credential_type
        self.issuer_name = issuer_name

        # Compute deterministic hash for this credential
        # (this is what we will sign with the issuer's private key)
        self.hash = compute_hash(
            f"{student_id}|{student_name}|{program}|{specialization}|{credential_type}|{issuer_name}"
        )

        # Will be set later when the issuer wallet signs the hash
        self.signature: str | None = None

    def to_dict(self) -> dict:
        """
        Convert credential to a plain dictionary so it can be stored
        inside blocks on the blockchain or returned via the interface.
        """
        return {
            "student_id": self.student_id,
            "student_name": self.student_name,
            "program": self.program,
            "specialization": self.specialization,
            "credential_type": self.credential_type,
            "issuer_name": self.issuer_name,
            "hash": self.hash,
            "signature": self.signature,
        }
