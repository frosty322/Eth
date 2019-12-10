from web3 import Web3 
import statistics
import matplotlib.pyplot as plt
web3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/e2a97e56c9dc4fa0a2a6eedb6caad75d"))


firstBlock = 8961400 - 1000*(34-2)
blocksGasUsed = []
blocksGasPrice = []
blocksContracts = []
blockUncles = []


for i in range(100):
  gasUsed = []
  gasPrice = []
  uncles = []
  contracts = 0
  for trans in web3.eth.getBlock(firstBlock + i)['transactions']:
    tran = web3.eth.getTransaction(trans)
    tranRec = web3.eth.getTransactionReceipt(trans)
    gasUsed.append(tranRec['gasUsed'])
    gasPrice.append(tran['gasPrice'])
    if tran['input'] != '0x':
      contracts+=1
    
  blocksGasUsed.append(gasUsed)
  blocksGasPrice.append(gasPrice)
  blocksContracts.append(contracts)
  blockUncles.append(web3.eth.getBlock(firstBlock + i).uncles)
  

file = open('Blocks_info.txt', 'w')
blocksCom = []
blocksRel = []
blocksNum = []
transCount = []
for i in range (100):
  com = 0
  trans_c = len(blocksGasUsed[i])
  for j in range(len(blocksGasUsed[i])):
    com += (blocksGasUsed[i][j]*blocksGasPrice[i][j])/(10**18)
  blocksNum.append(firstBlock+i)
  blocksRel.append(float("{0:.2f}".format(com*100/(com + 2+len(blockUncles[i])/16))))
  blocksCom.append(float ("{0:.2f}".format(com + 2+len(blockUncles[i])/16)))
  transCount.append(trans_c)
  file.write(str(i + firstBlock) + ',' + str(com + 2) + ',' + str(com*100/(com + 2)) + ',' + str(blocksContracts[i]) + '\n')  
file.close()
 
plt.scatter(blocksCom, transCount, color = 'r')
plt.xlabel('Комиссия ')
plt.ylabel('Количество транзакций')
plt.ylim(0, 500)
#plt.xlim(0, )
plt.grid()
plt.show()

plt.scatter(blocksRel, transCount, color = 'g')
plt.xlabel('Комиссия относительная')
plt.ylabel('Количество транзакций')
plt.ylim(0, 500)
#plt.xlim(0, )
plt.grid()
plt.show()

print("Абсолютная комиссия:")
print(str(statistics.median(blocksCom)) + '  - Медиана')
print(str(max(blocksCom) - min(blocksCom)) + '  - Размах')
average = statistics.mean(blocksCom) 
print(("{0:.3f}".format(average)) + ' - Среднее значение')
var = statistics.variance(blocksCom)
print(("{0:.3f}".format(var)) + ' - Дисперсия')
std = statistics.stdev(blocksCom)
print(("{0:.3f}".format(std)) + ' - Среднеквадратическое отклонение\n')

print("Относительная комиссия:")
print(str(statistics.median(blocksRel)) + '   - Медиана')
print(str(max(blocksRel) - min(blocksRel)) + ' - Размах')
average = statistics.mean(blocksRel) 
print(("{0:.3f}".format(average)) + ' - Среднее значение')
var = statistics.variance(blocksRel)
print(("{0:.3f}".format(var)) + ' - Дисперсия')
std = statistics.stdev(blocksRel)
print(("{0:.3f}".format(std)) + ' - Среднеквадратическое отклонение')