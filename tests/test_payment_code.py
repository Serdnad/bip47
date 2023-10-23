import unittest

from bip47 import Factory

from .test_vectors import *


class TestPaymentCodes(unittest.TestCase):
    def test_get_notification_address(self):
        for code in [PC1, PC2]:
            pc = Factory.from_base58(code["pcBase58"])
            self.assertEqual(pc.getNotificationAddress(), code["notifAddress"])

    def test_get_notification_private_key(self):
        seed = bytes.fromhex(PC2["seed"])
        pc = Factory.from_seed(seed, 0)
        self.assertEqual(pc.getNotificationPrivateKey().hex(), PC2["notifPrivKey"])

        # should raise for payment codes that don't have private keys
        pc = Factory.from_base58(PC1["pcBase58"])
        with self.assertRaises(ValueError):
            pc.getNotificationPrivateKey()

    

    # def test_derive_payment_pub_key(self):
    #     priv_key = bytes.fromhex(PC1["notifPrivKey"])
    #     pc = Factory.from_base58(PC2["pcBase58"])

    #     payment_pub_key = pc.derive_payment_public_key(priv_key, 0)
    #     print(payment_pub_key)
    #     self.assertEqual(payment_pub_key.hex(), PC2_PAYMENT_ADDRESSES[0]["pubkey"])



    # def test_derive_payment_priv_key(self):
    #     pub_key = bytes.fromhex(PC1["notifPubKey"])
    #     seed = bytes.fromhex(PC2["seed"])
    #     pc = Factory.from_seed(seed, 0)

    #     for i in range(len(PC2_PAYMENT_ADDRESSES)):
    #         payment_priv_key = pc.derive_payment_private_key(pub_key, i)
    #         self.assertEqual(payment_priv_key.hex(), PC2_PAYMENT_ADDRESSES[i]["privkey"])
    #     # payment_pub_key = pc.derive_payment_private_key(priv_key, 0)
    #     # print(payment_pub_key)
    #     # self.assertEqual(payment_pub_key.hex(), PC2_PAYMENT_ADDRESSES[0]["pubkey"])


    def test_get_payment_address(self):
        priv_key = bytes.fromhex(PC1["notifPrivKey"])
        pc2 = Factory.from_base58(PC2["pcBase58"])

        for i in range(10):
            payment_addr = pc2.get_payment_address(priv_key, i, "p2pkh")
            self.assertEqual(payment_addr, PC2_PAYMENT_ADDRESSES[i]["p2pkh"])

            # payment_addr = pc2.get_payment_address(privkey1, i, "p2sh")
            # self.assertEqual(payment_addr, PC2_PAYMENT_ADDRESSES[i]["p2sh"])

            # payment_addr = pc2.get_payment_address(privkey1, i, "p2sh")
            # self.assertEqual(payment_addr, PC2_PAYMENT_ADDRESSES[i]["p2sh"])

    #     # pc = Factory.from_base58(PC2["pcBase58"])
    #     # self.assertEqual(
    #     #     pc.derive_payment_public_key(bytes.fromhex(PC2["seed"]), 0),
    #     #     bytes.fromhex(PC2["notifPubKey"]),
    #     # )
