import unittest

from blockchain import Blockchain
from wallet import Wallet
from credential import Credential
from util_crypto import verify_signature, compute_hash


class TestBlockAcademia(unittest.TestCase):

    def setUp(self):
        # Fresh blockchain + issuer for each test
        self.blockchain = Blockchain()
        self.issuer = Wallet("Ontario Tech University")

        # Common test credential
        self.credential = Credential(
            student_id="2001",
            student_name="Test Student",
            program="MITS",
            specialization="AI",
            credential_type="Micro-cert",
            issuer_name=self.issuer.name,
        )
        # Sign + push to chain
        self.credential.signature = self.issuer.sign(self.credential.hash)
        self.blockchain.add_credential(self.credential)
        self.blockchain.mine_block()

    def test_credential_is_on_chain(self):
        """Credential should be retrievable by student_id."""
        found = self.blockchain.find_credential_by_student("2001")
        self.assertIsNotNone(found)
        self.assertEqual(found["student_name"], "Test Student")

    def test_signature_is_valid(self):
        """Digital signature should verify with issuer public key."""
        stored = self.blockchain.find_credential_by_student("2001")
        valid = verify_signature(
            self.issuer.public_key,
            stored["hash"],
            stored["signature"]
        )
        self.assertTrue(valid)

    def test_hash_mismatch_detects_tampering(self):
        """If data is changed, recomputed hash should not match stored hash."""
        stored = self.blockchain.find_credential_by_student("2001")
        # Simulate tampering – someone changes the student name
        stored["student_name"] = "Evil Hacker"
        recomputed_hash = compute_hash(
            f"{stored['student_id']}|{stored['student_name']}|"
            f"{stored['program']}|{stored['specialization']}|"
            f"{stored['credential_type']}|{stored['issuer_name']}"
        )
        self.assertNotEqual(recomputed_hash, stored["hash"])

    def test_chain_validity(self):
        """Blockchain should be valid initially, and invalid after tampering."""
        # Initially valid
        self.assertTrue(self.blockchain.is_chain_valid())

        # Tamper with a block hash
        self.blockchain.chain[1].data[0]["student_name"] = "Tampered"
        # Force mismatch by NOT updating block hash
        self.assertFalse(self.blockchain.is_chain_valid())


if __name__ == "__main__":
    unittest.main()
