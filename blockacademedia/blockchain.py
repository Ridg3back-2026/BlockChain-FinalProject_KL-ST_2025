import json
import time
from typing import List, Dict, Optional

from util_crypto import compute_hash
from credential import Credential



class Block:
    """
    A block in the blockchain. Stores a list of credentials.
    """

    def __init__(self, index: int, timestamp: float, data: List[Dict], previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.data = data              # list of credential dicts
        self.previous_hash = previous_hash
        self.hash = self.compute_block_hash()

    def compute_block_hash(self) -> str:
        """
        Compute the hash of the block based on its content.
        """
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True)

        return compute_hash(block_string)


class Blockchain:
    """
    Very simple blockchain to store academic credentials.
    No proof-of-work for simplicity; focus is on immutability + signatures.
    """

    def __init__(self):
        # create genesis block
        genesis_block = Block(
            index=0,
            timestamp=time.time(),
            data=[],
            previous_hash="0"
        )
        self.chain: List[Block] = [genesis_block]
        self.pending_credentials: List[Dict] = []

    # ---------------- CORE OPERATIONS ---------------- #

    def add_credential(self, credential: Credential):
        """
        Add a credential (as dict) to the list of pending credentials.
        """
        self.pending_credentials.append(credential.to_dict())

    def mine_block(self) -> Block:
        """
        Create a new block from all pending credentials and append it to the chain.
        """
        if not self.pending_credentials:
            raise ValueError("No pending credentials to mine")

        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            data=self.pending_credentials,
            previous_hash=self.chain[-1].hash
        )

        self.chain.append(new_block)
        self.pending_credentials = []   # clear the pool
        return new_block

    # ---------------- HELPER / QUERY METHODS ---------------- #

    def find_credential_by_student(self, student_id: str) -> Optional[Dict]:
        """
        Search the entire chain for a credential for a given student_id.
        Returns the first match, or None if not found.
        """
        for block in self.chain:
            for cred in block.data:
                if cred["student_id"] == student_id:
                    return cred
        return None

    def is_chain_valid(self) -> bool:
        """
        Basic verification: ensure each block's hash is correct and
        previous_hash fields link properly.
        """
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # recompute hash and compare
            if current.hash != current.compute_block_hash():
                return False

            # verify link
            if current.previous_hash != previous.hash:
                return False

        return True
