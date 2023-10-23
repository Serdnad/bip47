from typing import Union

from base58 import b58decode_check
from bip32 import BIP32

from .payment_code import PaymentCode
from .utils import PC_VERSION, Network


class Factory:
    """A factory class for creating PaymentCode objects."""

    @staticmethod
    def from_base58(base58: str, network: Network = Network.bitcoin):
        """
        Create a PaymentCode object from a base58-encoded string.

        Raises:
            TypeError: If the version code in the decoded string is not 0x47.
        """
        buf = b58decode_check(base58)

        version = buf[0]
        if version != PC_VERSION:
            raise TypeError(f"Invalid version code: expected 0x47, got {version}")

        return PaymentCode(buf[1:], network=network)

    @staticmethod
    def from_buffer(buf: bytes, network: Network = Network.bitcoin):
        """Create a PaymentCode object from a byte buffer."""
        return PaymentCode(buf, network)

    @staticmethod
    def from_seed(
        seed: bytes, id: Union[int, str], network: Network = Network.bitcoin
    ) -> PaymentCode:
        """Create a Payment Code from a given seed, id, and optional network."""

        # derive root BIP47 node
        root = BIP32.from_seed(seed)
        coin_type = "0" if network == Network.bitcoin else "1"
        chaincode, priv_key = root.get_extended_privkey_from_path(
            f"m/47'/{coin_type}'/{id}'"
        )
        root_bip47 = BIP32(chaincode=chaincode, privkey=priv_key)

        # construct payment code
        pc = bytearray(80)
        pc[0:2] = [1, 0]  # set version + options

        if len(root_bip47.pubkey) != 33:
            raise TypeError("Missing or invalid publicKey")
        pc[2:35] = root_bip47.pubkey

        if len(root_bip47.chaincode) != 32:
            raise TypeError("Missing or invalid chainCode")
        pc[35:67] = root_bip47.chaincode

        pc = bytes(pc)  # convert bytearray to bytes
        return PaymentCode(pc, root_bip47, network=network)
