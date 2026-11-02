from web3 import Web3
import eth_account
from eth_account.messages import encode_defunct


def sign(m):
    w3 = Web3()

    # Create a new Ethereum account
    account_object = w3.eth.account.create()
    public_key = account_object.address
    private_key = account_object.key

    # Encode and sign the message
    message = encode_defunct(text=m)
    signed_message = w3.eth.account.sign_message(
        message,
        private_key=private_key
    )

    print('Account created:\n'
          f'private key={w3.to_hex(private_key)}\naccount={public_key}\n')

    assert isinstance(
        signed_message,
        eth_account.datastructures.SignedMessage
    )

    return public_key, signed_message


def verify(m, public_key, signed_message):
    w3 = Web3()

    # Encode the original message
    message = encode_defunct(text=m)

    # Recover the signer from the signature
    signer = w3.eth.account.recover_message(
        message,
        signature=signed_message.signature
    )

    # Compare the recovered address with the expected address
    valid_signature = signer == public_key

    assert isinstance(valid_signature, bool)
    return valid_signature


if __name__ == "__main__":
    import random
    import string

    for i in range(10):
        m = "".join([random.choice(string.ascii_letters) for _ in range(20)])

        pub_key, signature = sign(m)

        # Modifies every other message so that the signature fails to verify
        if i % 2 == 0:
            m = m + 'a'

        if verify(m, pub_key, signature):
            print("Signed Message Verified")
        else:
            print("Signed Message Failed to Verify")
