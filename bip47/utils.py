from enum import Enum

import bip32
from base58 import b58encode_check
from bech32 import bech32_encode, convertbits
from Crypto.Hash import RIPEMD160, SHA256

PC_VERSION = 0x47

NETWORKS = {
    "bitcoin": {
        "pubKeyHash": 0x00,
        "scriptHash": 0x05,
        "bech32": "bc",
    },
    "testnet": {
        "pubKeyHash": 0x6F,
        "scriptHash": 0xC4,
        "bech32": "tb",
    },
    "regtest": {
        "pubKeyHash": 0x6F,
        "scriptHash": 0xC4,
        "bech32": "bcrt",
    },
}


class Network(Enum):
    main = "main"  # TODO: why is this not "bitcoin"?
    bitcoin = "bitcoin"
    testnet = "testnet"
    regtest = "regtest"


class AddressType(Enum):
    P2PKH = "p2pkh"
    P2SH = "p2sh"
    P2WPKH = "p2wpkh"


class Bip32:
    def __init__(self, public: int, private: int) -> None:
        self.public = public
        self.private = private


def sha256(buffer: bytes) -> bytes:
    """Compute the SHA256 hash of the given buffer."""
    return SHA256.new(buffer).digest()


def hash160(buffer: bytes) -> bytes:
    """Compute the RIPEMD160 hash of the SHA256 hash of the given buffer."""
    return RIPEMD160.new(sha256(buffer)).digest()


def to_base58_check(hash: bytes, version: int) -> str:
    """Convert a 20 byte hash to a base58-check encoded string,
    with the given version prepended as the first byte."""
    payload = bytearray(21)

    payload[0] = version
    payload[1:] = hash

    return b58encode_check(payload).decode("utf-8")


def get_p2pkh_address(pubkey: bytes, network: Network) -> str:
    """Get a P2PKH address from a public key."""
    return to_base58_check(hash160(pubkey), NETWORKS[network.value]["pubKeyHash"])


def get_p2sh_address(pubkey: bytes, network: dict) -> str:
    """Get a P2SH address from a public key."""
    push20_opcode = bytes([0, 0x14])
    hash_result = hash160(pubkey)
    script_sig = push20_opcode + hash_result

    return to_base58_check(hash160(script_sig), NETWORKS[network.value]["scriptHash"])


def get_p2wpkh_address(pubkey: bytes, network: Network) -> str:
    """Get a P2WPKH address from a public key."""
    hash_result = hash160(pubkey)

    # Convert the hash to bech32 format words
    words = convertbits(hash_result, 8, 5)

    # Add the SegWit version (0x00 for P2WPKH) to the beginning of the words list
    words.insert(0, 0)

    return bech32_encode(NETWORKS[network.value]["bech32"], words)


#  TODO: write unit tests
def is_valid_pub_key(key: bytes) -> bool:
    """Check if a public key is valid."""
    return bip32.utils._pubkey_is_valid(key)


#  TODO: write unit tests
def is_valid_priv_key(key: bytes) -> bool:
    return bip32.utils._privkey_is_valid(key)
