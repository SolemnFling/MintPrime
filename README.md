# MintPrime
写着玩的，打`base`链上的`$prime`
合约地址 `0x05b08d51ECecC1dfAd79a091FE1a43E77520673f`
可以去`basescan`上打https://basescan.org/token/0x05b08d51ececc1dfad79a091fe1a43e77520673f#writeContract
这里是脚本

需要替换 provider，就是支持 base 的 RPC，自己找，放入“”内
以及 main_wallet_address ，就是提供资金的那个钱包的地址，放入“”内
main_wallet_private_key ，提供资金的钱包的私钥，放入“”内
num_keys 将数字修改成想打的号的数量
最后在终端启动
```python
python3 prime.py
```
