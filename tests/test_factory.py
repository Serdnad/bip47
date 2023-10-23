import unittest

from bip47 import Factory

from .test_vectors import *


class TestFactory(unittest.TestCase):
    def test_from_base58(self):
        pc = Factory.from_base58(PC1["pcBase58"])  # should not raise
        self.assertEqual(pc.toBase58(), PC1["pcBase58"])

    def test_from_buffer(self):
        buf = bytes.fromhex(PC1["pc"])
        pc = Factory.from_buffer(buf)  # should not raise
        self.assertEqual(pc.toBase58(), PC1["pcBase58"])

    def test_from_seed(self):
        seed = bytes.fromhex(PC2["seed"])
        pc = Factory.from_seed(seed, 0)
        self.assertEqual(pc.toBase58(), PC2["pcBase58"])


if __name__ == "__main__":
    unittest.main()
