from base58 import b58encode_check
from bip32 import BIP32
from ecdsa import SECP256k1, VerifyingKey, curves
from ecdsa.util import number_to_string, string_to_number

from .utils import *


class PaymentCode:
    """
    BIP47 payment code implementation.

    A BIP47 payment code is a method for creating a reusable payment address
    that can be shared with others without revealing the user's transaction
    history or balance. It is based on the BIP32 hierarchical deterministic
    wallet structure and uses elliptic curve cryptography to derive payment
    addresses from a single master public key.
    """

    buf: bytes
    """The payment code buffer."""

    root: BIP32
    """The root BIP32 object derived from the payment code."""

    network: Network
    """The network with which the payment code is associated."""

    def __init__(
        self,
        buf: bytes,
        root: Bip32 = None,
        network: Network = Network.bitcoin,
    ):
        """
        Note: Unless you know what you're doing, you should use the
        Factory class to create PaymentCode objects.
        """

        if len(buf) != 80:
            raise TypeError("Invalid buffer length: expected 80 bytes")

        self.version = buf[0:1]
        if self.version[0] != 1:
            raise TypeError("Only payment codes version 1 are supported")

        self.buf = buf
        self.network = network

        if root is None:
            root = BIP32(
                pubkey=self.pubKey,
                chaincode=self.chainCode,
                # TODO: network
            )

        self.root = root

    @property
    def features(self) -> bytes:
        return self.buf[1:2]

    @property
    def pubKey(self) -> bytes:
        return self.buf[2:35]

    @property
    def chainCode(self) -> bytes:
        return self.buf[35:67]

    @property
    def paymentCode(self) -> bytes:
        return self.buf

    def toBase58(self) -> str:
        # Assuming PC_VERSION is a global constant and encode is a utility function.
        version = bytes([PC_VERSION])
        combined_buf = version + self.buf
        return b58encode_check(combined_buf).decode("utf-8")

    def _hasPrivKeys(self) -> bool:
        return self.root.privkey is not None

    def derive(self, path: str):
        return (self.derive_pub_key(path), self.derive_payment_private_key(path))

    def derive_pub_key(self, index: int):
        """Derive a child public key from the payment code."""
        return self.root.get_pubkey_from_path(f"m/{index}")

    def derive_priv_key(self, index: int):
        """Derive a child private key from the payment code."""
        return self.root.get_privkey_from_path(f"m/{index}")

    def deriveHardened(self, index: int):
        return self.root.deriveHardened(index)

    def getNotificationAddress(self) -> str:
        pub_key = self.derive_pub_key(0)
        return get_p2pkh_address(pub_key, self.network)

    def getNotificationPrivateKey(self) -> bytes:
        if not self._hasPrivKeys():
            raise ValueError("This payment code does not have private keys")

        return self.derive_priv_key(0)

    def derive_payment_private_key(self, a: bytes, index: int) -> bytes:
        if not is_valid_pub_key(a):
            raise TypeError("Invalid public key")

        # get keys, raising if no private key is available
        b_node_keys = self.derive(index)
        b = b_node_keys[1]  # private key
        # point multiply A by b
        A_point = VerifyingKey.from_string(a, curve=SECP256k1).pubkey.point
        S = A_point.__mul__(string_to_number(b))

        Sx = number_to_string(S.x(), SECP256k1.order)
        s = sha256(Sx)

        if not is_valid_priv_key(s):
            raise TypeError("Invalid derived private key")

        # equivalent of ecc.privateAdd(b, s)
        payment_priv_key = string_to_number(b) + string_to_number(s)
        return number_to_string(payment_priv_key, SECP256k1.order)

    def derive_payment_public_key(self, notif_key: bytes, index: int) -> bytes:
        """
        Derive a payment public key for the payment code, given the
        sender's public or private key, and the index of the payment
        between the sender and the payment code.
        """
        order = SECP256k1.order

        B = None
        S = None

        # Check if key is a private key
        is_private = (len(notif_key) == 32) and (
            1 <= string_to_number(notif_key) < order
        )

        # Check if key is a public key
        is_public = len(notif_key) == 33 and (
            notif_key[0] == 0x02 or notif_key[0] == 0x03
        )

        if not is_private and not is_public:
            raise TypeError("sender_key is neither a valid private key or public key")

        if is_private:
            B = self.derive_pub_key(index)
            # Convert B to point
            B_point = VerifyingKey.from_string(B, curve=SECP256k1).pubkey.point
            # Multiply point B by scalar a
            S = B_point.__mul__(string_to_number(notif_key))
        else:
            if not self._has_priv_keys():
                raise ValueError(
                    "Unable to compute the derivation with a public key provided as argument"
                )

            A_point = VerifyingKey.from_string(notif_key, curve=SECP256k1).pubkey.point
            B = self.derive_pub_key(index)
            b_node_priv_key = self.derive_priv_key(index)
            b_scalar = string_to_number(b_node_priv_key)
            B_point = VerifyingKey.from_string(B, curve=SECP256k1).pubkey.point

            S = A_point.__mul__(b_scalar)

        if not B:  # TODO: add additional public key check (isPoint ?)
            raise TypeError("Invalid derived public key")

        Sx = number_to_string(S.x(), order)
        s = sha256(Sx)
        s_scalar = string_to_number(s)

        # Create a point from scalar s
        ecc_point = s_scalar * SECP256k1.generator

        # Add point B and EccPoint
        from ecdsa.ellipticcurve import PointJacobi

        paymentPublicKey_point: PointJacobi = B_point.__add__(ecc_point)

        # Serialize the point to bytes
        paymentPublicKey = VerifyingKey.from_public_point(
            paymentPublicKey_point, curve=SECP256k1
        ).to_string()

        return paymentPublicKey

    def get_payment_address(
        self, notif_key: bytes, index: int, address_type: str = "p2pkh"
    ) -> str:
        pubkey = self.derive_payment_public_key(notif_key, index)

        if not pubkey:
            raise TypeError("Unable to derive public key")

        if address_type == "p2pkh":
            return get_p2pkh_address(pubkey, self.network)
        elif address_type == "p2sh":
            return get_p2sh_address(pubkey, self.network)
        elif address_type == "p2wpkh":
            return get_p2wpkh_address(pubkey, self.network)
        else:
            raise ValueError("Unknown address type. Expected: p2pkh, p2sh, or p2wpkh")
