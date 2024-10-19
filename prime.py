import asyncio
import pandas as pd
from web3 import Web3
import time

# 连接到以太坊节点
provider = ""  # 替换为你的 base RPC
w3 = Web3(Web3.HTTPProvider(provider))

# 检查是否连接到以太坊网络
assert w3.is_connected(), "无法连接到以太坊网络"

# 主钱包地址和私钥，用于支付ETH并接收转账
main_wallet_address = w3.to_checksum_address("")  # 替换为你的主钱包地址
main_wallet_private_key = ""  # 替换为你的主钱包私钥

# 数量
num_keys = 1 # 想 mint 的数量

# 合约地址和ABI
contract_address = "0x05b08d51ECecC1dfAd79a091FE1a43E77520673f"  # 替换为合约地址
contract_abi = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"allowance","type":"uint256"},{"internalType":"uint256","name":"needed","type":"uint256"}],"name":"ERC20InsufficientAllowance","type":"error"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"uint256","name":"balance","type":"uint256"},{"internalType":"uint256","name":"needed","type":"uint256"}],"name":"ERC20InsufficientBalance","type":"error"},{"inputs":[{"internalType":"address","name":"approver","type":"address"}],"name":"ERC20InvalidApprover","type":"error"},{"inputs":[{"internalType":"address","name":"receiver","type":"address"}],"name":"ERC20InvalidReceiver","type":"error"},{"inputs":[{"internalType":"address","name":"sender","type":"address"}],"name":"ERC20InvalidSender","type":"error"},{"inputs":[{"internalType":"address","name":"spender","type":"address"}],"name":"ERC20InvalidSpender","type":"error"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"OwnableInvalidOwner","type":"error"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"OwnableUnauthorizedAccount","type":"error"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"spender","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":True,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"MAX_SUPPLY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MINT_AMOUNT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"collect","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_max","type":"uint256"}],"name":"getRandomNumber","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"runs","type":"uint256"}],"name":"mine","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"mint_count","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]

# 合约实例
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Base链的chainId是8453
chain_id = 8453

# 批量创建钱包函数
async def create_wallet():
    account = w3.eth.account.create()
    private_key = account.key.hex()  # 使用 account.key 获取私钥并转换为十六进制格式
    return w3.to_checksum_address(account.address), private_key

# 获取合约生成的随机数
async def get_contract_random_number():
    return contract.functions.getRandomNumber(100).call()

# 从主钱包支付 0.0005 ETH
async def fund_wallet_from_main(wallet_address):
    nonce = w3.eth.get_transaction_count(main_wallet_address)
    tx = {
        'nonce': nonce,
        'to': wallet_address,
        'value': w3.to_wei(0.0005, 'ether'),
        'gas': 21000,  # 固定的gas限制用于转账
        'gasPrice': w3.to_wei('0.009', 'gwei'),
        'chainId': chain_id
    }
    signed_tx = w3.eth.account.sign_transaction(tx, main_wallet_private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt

# 执行 mint 操作
async def mint_token(account_address, account_private_key):
    nonce = w3.eth.get_transaction_count(account_address)
    tx = contract.functions.mint().build_transaction({
        'from': account_address,
        'nonce': nonce,
        'gas': 31000000,
        'gasPrice': w3.to_wei('0.015', 'gwei'),
        'chainId': chain_id
    })
    signed_tx = w3.eth.account.sign_transaction(tx, account_private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt

# 转移代币到主钱包
async def transfer_tokens_to_main(account_address, account_private_key):
    # 查询钱包中代币的余额
    token_balance = contract.functions.balanceOf(account_address).call()
    
    if token_balance > 0:
        print(f"钱包 {account_address} 代币余额: {token_balance}，开始转移到主钱包")

        # 构建代币转账交易
        nonce = w3.eth.get_transaction_count(account_address)
        tx = contract.functions.transfer(main_wallet_address, token_balance).build_transaction({
            'from': account_address,
            'nonce': nonce,
            'gas': 55000,  # Gas limit for token transfer
            'gasPrice': w3.to_wei('0.008', 'gwei'),
            'chainId': chain_id
        })

        # 签名并发送交易
        signed_tx = w3.eth.account.sign_transaction(tx, account_private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"代币转账成功，交易哈希: {receipt.transactionHash.hex()}")
        return receipt
    else:
        print(f"钱包 {account_address} 没有足够的代币余额")

# 读取 yes.csv 文件中的数据
def load_yes_csv():
    try:
        return pd.read_csv("yes.csv")
    except FileNotFoundError:
        # 如果 yes.csv 不存在，返回空的DataFrame
        return pd.DataFrame(columns=["private", "address", "balance"])

# 将新的记录追加到 yes.csv 文件
def append_to_yes_csv(private_key, address, balance):
    new_data = pd.DataFrame([[private_key, address, balance]], columns=["private", "address", "balance"])
    new_data.to_csv("yes.csv", mode='a', header=False, index=False)

# 主函数，批量执行操作
async def main():
    yes_data = load_yes_csv()

    for _ in range(num_keys):
        # 创建钱包地址
        address, private_key = await create_wallet()

        # 检查该私钥是否已在 yes.csv 中
        if private_key in yes_data['private'].values:
            print(f"私钥 {private_key} 已存在于yes.csv中，跳过...")
            continue

        print(f"创建了钱包 {address} {private_key}")

        # 从主钱包向新创建的钱包转账 0.0005 ETH
        try:
            print(f"从主钱包向 {address} 转账 0.0005 ETH")
            receipt = await fund_wallet_from_main(address)
            print(f"转账成功，交易哈希: {receipt.transactionHash.hex()}")
        except Exception as e:
            print(f"ETH 转账失败: {e}")
            continue

        while True:
            lucky_number = await get_contract_random_number()
            print(f"合约返回的幸运随机数: {lucky_number}")
            if lucky_number > 8:
                try:
                    print(f"钱包 {address} 符合条件，执行mint")
                    receipt = await mint_token(address, private_key)
                    print(f"Mint成功，交易哈希: {receipt.transactionHash.hex()}")

                    # 获取代币余额
                    token_balance = (contract.functions.balanceOf(address).call())//(10**18)

                    # 获取合约代币余额并转移到主钱包
                    await transfer_tokens_to_main(address, private_key)

                    # 将成功的私钥、地址和余额写入 yes.csv
                    append_to_yes_csv(private_key, address, token_balance)
                    print(f"记录成功写入 yes.csv，地址: {address}, 余额: {token_balance}")
                    
                except Exception as e:
                    print(f"交易失败，重新构建交易: {e}")
                break
            else:
                print(f"随机数太低，重新尝试")
                time.sleep(2)  # 等待片刻再尝试

if __name__ == "__main__":
    asyncio.run(main())
