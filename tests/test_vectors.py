# we use test vectors from https://gist.github.com/SamouraiDev/6aad669604c5930864bd,
# the reference test vectors from the BIP: https://github.com/spsina/bip47

PC1 = {
    "pc": "010002b85034fb08a8bfefd22848238257b252721454bbbfba2c3667f168837ea2cdad671af9f65904632e2dcc0c6ad314e11d53fc82fa4c4ea27a4a14eccecc478fee00000000000000000000000000",
    "pcBase58": "PM8TJTLJbPRGxSbc8EJi42Wrr6QbNSaSSVJ5Y3E4pbCYiTHUskHg13935Ubb7q8tx9GVbh2UuRnBc3WSyJHhUrw8KhprKnn9eDznYGieTzFcwQRya4GA",
    "notifAddress": "1JDdmqFLhpzcUwPeinhJbUPw4Co3aWLyzW",
    "notifPrivKey": "8d6a8ecd8ee5e0042ad0cb56e3a971c760b5145c3917a8e7beaf0ed92d7a520c",
    "notifPubKey": "0353883a146a23f988e0f381a9507cbdb3e3130cd81b3ce26daf2af088724ce683",
}


PC2 = {
    "seed": "87eaaac5a539ab028df44d9110defbef3797ddb805ca309f61a69ff96dbaa7ab5b24038cf029edec5235d933110f0aea8aeecf939ed14fc20730bba71e4b1110",
    "pcBase58": "PM8TJS2JxQ5ztXUpBBRnpTbcUXbUHy2T1abfrb3KkAAtMEGNbey4oumH7Hc578WgQJhPjBxteQ5GHHToTYHE3A1w6p7tU6KSoFmWBVbFGjKPisZDbP97",
    "notifAddress": "1ChvUUvht2hUQufHBXF8NgLhW8SwE2ecGV",
    "notifPrivKey": "04448fd1be0c9c13a5ca0b530e464b619dc091b299b98c5cab9978b32b4a1b8b",
    "notifPubKey": "024ce8e3b04ea205ff49f529950616c3db615b1e37753858cc60c1ce64d17e2ad8",
}


PC2_PAYMENT_ADDRESSES = [
    {
        "pubkey": "0344b4795e48df097bd87e6cf87a70e4f0c30b2d847b6e34cddde64af10296952d",
        "p2pkh": "141fi7TY3h936vRUKh1qfUZr8rSBuYbVBK",
        "p2sh": "3QnEFKkpXFYSipn4uqcMNAKWhZq6PD4Gmz",
        "p2wpkh": "bc1qyyytpxv60e6hwh5jqkj2dcenckdsw6ekn2htfq",
    },
    {
        "p2pkh": "12u3Uued2fuko2nY4SoSFGCoGLCBUGPkk6",
        "p2sh": "38mr84Lrer3j1pTEZpTJ1pQTQJweMcc4YC",
        "p2wpkh": "bc1qzn8a8drxv6ln7rztjsw660gzf3hnrfwupzmsfh",
    },
    {
        "p2pkh": "1FsBVhT5dQutGwaPePTYMe5qvYqqjxyftc",
        "p2sh": "37Q2nDn2MGPLR2eCSRRnx3EZUv1bgNJpH3",
        "p2wpkh": "bc1q5v84r4dq2vkdku8h7ewfkj6c00eh20gmf0amr5",
    },
    {
        "p2pkh": "1CZAmrbKL6fJ7wUxb99aETwXhcGeG3CpeA",
        "p2sh": "38KnaMF7yiGnuUxDuM5AYoU7biYaGEfaRg",
        "p2wpkh": "bc1q06ld55yrxrqdfym235h0jvdddvwc72ktsamh7c",
    },
    {
        "p2pkh": "1KQvRShk6NqPfpr4Ehd53XUhpemBXtJPTL",
        "p2sh": "38A9WgnPYfNwDbovo12sSGF4E8Kq67qHvc",
        "p2wpkh": "bc1qe8uxekd8s59szxgnnfd2nxrn3ncnkmxlku83l9",
    },
    {
        "p2pkh": "1KsLV2F47JAe6f8RtwzfqhjVa8mZEnTM7t",
        "p2sh": "3A41gu3kgtqPpiWQwp5fY5VVS5WNgT11nN",
        "p2wpkh": "bc1qemm4xmwr0fxwysry5mur0r5q5kakkw79fpezx0",
    },
    {
        "p2pkh": "1DdK9TknVwvBrJe7urqFmaxEtGF2TMWxzD",
        "p2sh": "33prMnukiGDj4vdwD7r3WV7fDuWxWAFEh5",
        "p2wpkh": "bc1q3fl6rfkg4f600tlfrtkn6jv6kndg9tfu3hr009",
    },
    {
        "p2pkh": "16DpovNuhQJH7JUSZQFLBQgQYS4QB9Wy8e",
        "p2sh": "38qRxEnED8hMVqQMywJydEmK595gBXi6yQ",
        "p2wpkh": "bc1q89zc0ptgrcgsrzkfe4fjrlwcwfvny908976vxh",
    },
    {
        "p2pkh": "17qK2RPGZMDcci2BLQ6Ry2PDGJErrNojT5",
        "p2sh": "3QH8LrqkkTnLNcaq5dsBzcj5LCoo5U8pEz",
        "p2wpkh": "bc1qfteug4efvdlhyek9p9mrgwk0kqsq74y8jm5qw7",
    },
    {
        "p2pkh": "1GxfdfP286uE24qLZ9YRP3EWk2urqXgC4s",
        "p2sh": "3ALkcRwUk1QhkZhcG7t9ooAAu7o12MGQr7",
        "p2wpkh": "bc1q4ugsxkh69aknjvskm8k2susv9c6dq0pp3476y0",
    },
]
