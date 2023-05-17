import time
import asyncio

from web3 import Account, Web3
from utils import random_sycle_time
from bridge.eth_bridge import swap_eth_arbitrum_optimism, swap_eth_optimism_arbitrum, get_balance_eth_arbitrum, get_balance_eth_optimism

async def main(tr):
    with open('keys.txt', 'r') as keys_file:
        accounts = [Account.from_key(line.replace("\n", "")) for line in keys_file.readlines()]
        for _ in range(0, tr):
            for account in accounts:
                
                try: 
                    arbitrum_balance = get_balance_eth_arbitrum(account.address)
                    optimism_balance = get_balance_eth_optimism(account.address)

                    if arbitrum_balance + optimism_balance < Web3.to_wei(0.02, 'ether'):
                        continue

                    if arbitrum_balance > optimism_balance:
                        print("Swapping ETH from Arbitrum to Optimism...")
                        await arbitrum_to_optimism_txs_hash = swap_eth_arbitrum_optimism(account=account, amount=arbitrum_balance - Web3.to_wei(0.01, 'ether'))
                        print(f"Transaction: https://arbiscan.io/tx/{arbitrum_to_optimism_txs_hash.hex()}")
                    else:
                        print("Swapping ETH from Optimism to Arbitrum...")
                        await optimism_to_arbitrum_txs_hash = swap_eth_optimism_arbitrum(account=account, amount=optimism_balance - Web3.to_wei(0.01, 'ether'))
                        print(f"Transaction: https://optimistic.etherscan.io/tx{optimism_to_arbitrum_txs_hash.hex()}")

                    print("Sleeping for the next account")
                    time.sleep(random_sycle_time(30))
                
                except:
                    pass

            print("Sleeping for the next cycle")
            time.sleep(random_sycle_time(600))


if __name__ == '__main__':
    total_rounds = 10
    asyncio.run(main(total_rounds))
