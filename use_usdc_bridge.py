import time
import asyncio

from web3 import Account
from utils import random_sycle_time
from bridge.usdc_bridge import swap_usdc_fantom_to_polygon, swap_usdc_polygon_to_fantom, get_balance_usdc_fantom, get_balance_usdc_polygon


async def main(tr):
    with open('keys.txt', 'r') as keys_file:
        accounts = [Account.from_key(line.replace("\n", "")) for line in keys_file.readlines()]
        for _ in range(0, tr):
            for account in accounts:

                try:
                    fantom_balance = get_balance_usdc_fantom(account.address)
                    polygon_balance = get_balance_usdc_polygon(account.address)

                    if fantom_balance + polygon_balance < 10 * (10 ** 6):
                        continue

                    if fantom_balance > polygon_balance:
                        print("Swapping USDC from Fantom to Polygon...")
                        await fantom_to_polygon_txn_hash = swap_usdc_fantom_to_polygon(account=account, amount=fantom_balance)
                        print(f"Transaction: https://ftmscan.com/tx/{fantom_to_polygon_txn_hash.hex()}")
                    else:
                        print("Swapping USDC from Polygon to Fantom...")
                        await polygon_to_fantom_txn_hash = swap_usdc_polygon_to_fantom(account=account, amount=polygon_balance)
                        print(f"Transaction: https://polygonscan.com/tx/{polygon_to_fantom_txn_hash.hex()}")

                    print("Sleeping for the next account")
                    time.sleep(random_sycle_time(30))
                
                except:
                    pass

            print("Sleeping for the next cycle")
            time.sleep(random_sycle_time(600))


if __name__ == '__main__':
    total_rounds = 10
    asyncio.run(main(total_rounds))
