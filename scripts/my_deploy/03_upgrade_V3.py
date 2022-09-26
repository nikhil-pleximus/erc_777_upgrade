from brownie import network, Contract, MyTokenV3, web3, ProxyAdmin, TransparentUpgradeableProxy, config, Contract

from scripts.helpful_scripts import get_account, encode_function_data, upgrade

def main():
    account = get_account()
    print(f"Deploying to {network.show_active()}")

    my_token_v3 = MyTokenV3.deploy({"from": account}, publish_source=config["networks"][network.show_active()].get("verify"))

    proxy = TransparentUpgradeableProxy[-1]
    proxy_admin = ProxyAdmin[-1]

    # Upgrade method calls upgrade method from proxy admin like following
    # proxy_admin.upgrade(proxy.address, my_token_v2.address, {"from": account})
    # upgrade(account, proxy, my_token_v2, proxy_admin_contract=proxy_admin) # this upgrade method is imported from helpful scripts

    proxy_admin.upgrade(proxy.address, my_token_v3.address, {"from": account})

    print("Proxy has been upgraded!")

    proxy_new_contract = Contract.from_abi("TokenV3", proxy.address, my_token_v3.abi)

    print("New implementation method", proxy_new_contract.my_version())