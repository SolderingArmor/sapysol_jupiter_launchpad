# sapysol_jupiter_launchpad

`sapysol` Jupiter LFG Launchpad Claim implementation. Based on JavaScript from [Jupiter LFG Website](https://lfg.jup.ag) _(from Chrome developer tools)_, written from scratch with the help of [AnchorPy](https://github.com/kevinheavey/anchorpy).

# Installation

```sh
pip install sapysol
```

Note: Requires Python >= 3.10.

# Usage

```py
# LFG Claiming (ZEUS example)
# Automatically claims tokens for a list of wallets/keypairs.
# Can use multiple parallel threads.
#
from solana.rpc.api            import Client
from sapysol                   import *
from sapysol.token_cache       import *
from typing                    import List
from sapysol_jupiter_launchpad import SapysolJupiterDistributorBatcher

SetupLogging()

connection: Client = Client("https://api.mainnet-beta.solana.com")

# Prepare a list of keypairs to claim tokens
keypairsList: List[Keypair] = [
    MakeKeypair("/path/to/keypair1.json"),
    MakeKeypair("/path/to/keypair2.json"),
    MakeKeypair("/path/to/keypair3.json"),
    MakeKeypair("/path/to/keypair4.json"),
]

# Prepare batcher that automatically performs claims for all keypairs using 
# `numThreads` number of threads.
batcher = SapysolJupiterDistributorBatcher(connection   = connection,
                                           tokenMint    = "ZEUS1aR7aX8DFFJf5QjWj2ftDDdNTroMNGo8YoQm3Gq",
                                           keypairsList = keypairsList,
                                           numThreads   = 10)

# Start claiming
batcher.Start()

```

TODO

# Contributing

TODO

# Tests

TODO

# Contact

[Telegram](https://t.me/sapysol)

Donations: `SAxxD7JGPQWqDihYDfD6mFp7JWz5xGrf9RXmE4BJWTS`

# Disclaimer

### Intended Purpose and Use
The Content is provided solely for educational, informational, and general purposes. It is not intended for use in making any business, investment, or legal decisions. Although every effort has been made to keep the information up-to-date and accurate, no representations or warranties, express or implied, are made regarding the completeness, accuracy, reliability, suitability, or availability of the Content.

### Opinions and Views
The views and opinions expressed herein are those of Anton Platonov and do not necessarily reflect the official policy, position, or views of any other agency, organization, employer, or company. These views are subject to change, revision, and rethinking at any time.

### Third-Party Content and Intellectual Property
Some Content may include or link to third-party materials. The User agrees to respect all applicable intellectual property laws, including copyrights and trademarks, when engaging with this Content.

### Amendments
Chintan Gurjar reserves the right to update or change this disclaimer at any time without notice. Continued use of the Content following modifications to this disclaimer will constitute acceptance of the revised terms.