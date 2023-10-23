import unittest

from bip47 import utils

PUBKEYS = {
    "026477115981fe981a6918a6297d9803c4dc04f328f22041bedff886bbc2962e01": {
        "p2pkh": "1ByEkML4fWUSVCZaRFffnv8GRPoNCpTPD3",
        "p2sh": "38XyUfqF4yZGHFpNA1XPas6ximJAxdVT1G",
        "p2wpkh": "bc1q0p2qwzpgz74686uslpwxps2rhnq20cu2tmk4xc",
    },
    "02c96db2302d19b43d4c69368babace7854cc84eb9e061cde51cfa77ca4a22b8b9": {
        "p2pkh": "18XCoMKgHyKc4MHuQsohbCFDSRE9U4Fnfc",
        "p2sh": "3KAC1ti6xTTwXvB5L2VimrbDbVby3Q3Udt",
        "p2wpkh": "bc1q2fln2u0jq2law0gg0dcjcswy4v29rmqlr97tpp",
    },
    "03c6103b3b83e4a24a0e33a4df246ef11772f9992663db0c35759a5e2ebf68d8e9": {
        "p2pkh": "1NXyR8CAcwja7dEreBhuc8qpAMgvwDQDFj",
        "p2sh": "3PcKB1iFX2ZwGg61L8s2wrFVsm85B2Sytr",
        "p2wpkh": "bc1qasmrd33pnhs040p7ug53ycrldmyqxm97j29slp",
    },
}


class TestUtils(unittest.TestCase):
    def test_get_p2pkh_address(self):
        for pubkey in PUBKEYS:
            self.assertEqual(
                utils.get_p2pkh_address(bytes.fromhex(pubkey), utils.Network.bitcoin),
                PUBKEYS[pubkey]["p2pkh"],
            )

    def test_get_p2wpkh_address(self):
        for pubkey in PUBKEYS:
            self.assertEqual(
                utils.get_p2wpkh_address(bytes.fromhex(pubkey), utils.Network.bitcoin),
                PUBKEYS[pubkey]["p2wpkh"],
            )

    def test_get_p2sh_address(self):
        for pubkey in PUBKEYS:
            self.assertEqual(
                utils.get_p2sh_address(bytes.fromhex(pubkey), utils.Network.bitcoin),
                PUBKEYS[pubkey]["p2sh"],
            )


if __name__ == "__main__":
    unittest.main()
