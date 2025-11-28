from wallet import Wallet
from credential import Credential
from blockchain import Blockchain
from util_crypto import verify_signature, compute_hash



def issue_credential_flow(blockchain: Blockchain, issuer: Wallet):
    """
    CLI flow to issue a new academic credential.
    """
    print("\n--- ISSUE NEW CREDENTIAL ---")

    student_id = input("Student ID: ")
    student_name = input("Student Name: ")
    program = input("Program (e.g., MITS): ")
    specialization = input("Specialization (e.g., AI): ")
    credential_type = input("Credential type (Degree/Micro-cert): ")

    # Create Credential object (computes its hash internally)
    credential = Credential(
        student_id=student_id,
        student_name=student_name,
        program=program,
        specialization=specialization,
        credential_type=credential_type,
        issuer_name=issuer.name,
    )

    # Sign the credential hash with issuer's private key (digital signature)
    credential.signature = issuer.sign(credential.hash)

    # Add to blockchain and mine block
    blockchain.add_credential(credential)
    new_block = blockchain.mine_block()

    print("\nCredential issued and added to block:")
    print(f"  Block index: {new_block.index}")
    print(f"  Credential hash: {credential.hash}")
    print(f"  Digital signature (truncated): {credential.signature[:60]}...")
    print("---------------------------------------------------------")


def verify_credential_flow(blockchain: Blockchain, issuer: Wallet):
    """
    CLI flow to verify an existing credential using:
    - credential hash
    - issuer's digital signature
    - blockchain integrity
    """
    print("\n--- VERIFY CREDENTIAL ---")
    student_id = input("Enter Student ID to verify: ")

    stored = blockchain.find_credential_by_student(student_id)

    if stored is None:
        print("❌ Credential not found on blockchain.")
        return

    print("\nCredential found on chain:")
    for k, v in stored.items():
        if k in ("hash", "signature"):
            print(f"  {k}: {v[:60]}...")  # truncate long values
        else:
            print(f"  {k}: {v}")

    # 1) Recompute hash from fields to detect tampering with data
    recomputed_hash = compute_hash(
        f"{stored['student_id']}|{stored['student_name']}|"
        f"{stored['program']}|{stored['specialization']}|"
        f"{stored['credential_type']}|{stored['issuer_name']}"
    )

    if recomputed_hash != stored["hash"]:
        print("\n❌ INVALID: Credential data has been modified (hash mismatch).")
        return

    # 2) Verify digital signature using issuer's public key
    sig_valid = verify_signature(
        issuer.public_key,
        stored["hash"],
        stored["signature"],
    )

    if not sig_valid:
        print("\n❌ INVALID: Digital signature does not match issuer.")
        return

    # 3) Optionally verify blockchain integrity
    if not blockchain.is_chain_valid():
        print("\n⚠️ WARNING: Blockchain structure invalid (tampering suspected).")
        return

    print("\n✅ CREDENTIAL IS VALID")
    print(" - Data matches stored hash")
    print(" - Digital signature verified with issuer's public key")
    print(" - Blockchain links are consistent")


def main():
    """
    Entry point for CLI testing of BlockAcademia backend.
    """
    # Create blockchain
    blockchain = Blockchain()

    # Hard-coded issuer wallet (Ontario Tech)
    issuer = Wallet("Ontario Tech University")

    print("BlockAcademia – Blockchain-based Academic Credential & Micro-Cert Verification")
    print("Issuer wallet created for:", issuer.name)

    while True:
        print("\n=========== MENU ===========")
        print("1. Issue new credential")
        print("2. Verify credential")
        print("3. Check chain validity")
        print("4. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            issue_credential_flow(blockchain, issuer)
        elif choice == "2":
            verify_credential_flow(blockchain, issuer)
        elif choice == "3":
            print("\nBlockchain valid?", blockchain.is_chain_valid())
        elif choice == "4":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Please enter 1–4.")


if __name__ == "__main__":
    main()
