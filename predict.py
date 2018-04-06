
import random
import time

class Train(object):
    def __init__(self, trainData, trainLabel, n, flavor='flavor1'):
        self.x = trainData[flavor]
        self.y = trainLabel[flavor]
        self.learnRate = 0.01
        self.n = n
        self.m = len(self.y)
        self.W = []
        self._initW()
        self.flavor = flavor
        self.y_ = [0] * len(self.y)
        self.loss = 0
        self.dw = [0] * len(self.W)

    def _initW(self):
        random.seed(time.time())
        for i in range(self.n):
            self.W.append(random.random())

    def dotProduct(self, x, y):
        z = 0
        for i in range(len(x)):
            z = z + x[i]*y[i]
        return z

    def vectorMinus(self, x, y):
        z = []
        for i in range(len(y)):
            z.append(x[i]-y[i])
        return z


    def forwardPropagation(self, x):
        for i in range(self.m):
            self.y_[i] = round(self.dotProduct(self.W, x[i]))

    def backwardPropagation(self):
        diff = self.vectorMinus(self.y_, self.y)
        diffSquare = [i ** 2 for i in diff]
        self.loss = sum(diffSquare) / (2 * self.m)
        xij = []
        temp = []
        for j in range(self.n):
            for elem in self.x:
                temp.append(elem[j])
            xij.append(temp)
            temp = []
        for j in range(len(self.dw)):
            self.dw[j] = 1/self.m * (self.dotProduct(diff, xij[j]))
        product = [self.learnRate * i for i in self.dw]
        self.W = self.vectorMinus(self.W, product)

class Packing(object):
    def __init__(self, preDict, inputData):
        self.preDict = preDict
        self.goods = []
        self.packType = inputData.CPUorMEM
        self.flavorsNum = inputData.flavorNum
        self.flavors = inputData.flavor
        self.serverCPU = inputData.serverCPU
        self.serverMEM = inputData.serverMEM
        self.boxes = []
        self.flavorType = {
            'flavor1': [1, 1], 'flavor2': [1, 2], 'flavor3': [1, 4],
            'flavor4': [2, 2], 'flavor5': [2, 4], 'flavor6': [2, 8],
            'flavor7': [4, 4], 'flavor8': [4, 8], 'flavor9': [4, 16],
            'flavor10': [8, 8], 'flavor11': [8, 16], 'flavor12': [8, 32],
            'flavor13': [16, 16], 'flavor14': [16, 32], 'flavor15': [16, 64]
        }
        self.initGoods()
        self.sortGoods()

    def initGoods(self):
        if self.packType == 'CPU':
            for elem in self.preDict:
                for i in range(self.preDict[elem]):
                    self.goods.append((int(elem.split('r')[1]), self.flavorType[elem][0]))
        if self.packType == 'MEM':
            for elem in self.preDict:
                for i in range(self.preDict[elem]):
                    self.goods.append((int(elem.split('r')[1]), self.flavorType[elem][1]))

    def sortGoods(self):
        self.goods = sorted(self.goods, key=lambda s: s[1], reverse=True)

    def packing(self):
        sign = 0
        while self.goods:
            if self.boxes == []:
                if self.packType == 'CPU':
                    self.boxes.append([[self.goods[0]], self.serverCPU - self.goods[0][1]])
                    del(self.goods[0])
                    continue
                if self.packType == 'MEM':
                    self.boxes.append([[self.goods[0]], self.serverMEM - self.goods[0][1]])
                    del (self.goods[0])
                    continue
            for elem in self.boxes:
                if elem[1] >= self.goods[0][1]:
                    elem[0].append(self.goods[0])
                    elem[1] = elem[1] - self.goods[0][1]
                    del(self.goods[0])
                    sign = 1
                    break
            if sign == 0:
                if self.packType == 'CPU':
                    self.boxes.append([[self.goods[0]], self.serverCPU - self.goods[0][1]])
                    del(self.goods[0])
                if self.packType == 'MEM':
                    self.boxes.append([[self.goods[0]], self.serverMEM - self.goods[0][1]])
            sign = 0









# def main():
#     n = 9
#     m = 7
#     W = {
#         'flavor1': [], 'flavor2': [], 'flavor3': [],
#         'flavor4': [], 'flavor5': [], 'flavor6': [],
#         'flavor7': [], 'flavor8': [], 'flavor9': [],
#         'flavor10': [], 'flavor11': [], 'flavor12': [],
#         'flavor13': [], 'flavor14': [], 'flavor15': []
#     }
#     preData = {}
#     # trainFileName = '.\\初赛文档\\用例示例\\data_total.txt'
#     testFileName = '.\\初赛文档\\用例示例\\testData_2015.2.20_2015.2.27.txt'
#     testData = prepareData.Data(testFileName, n)
#     trainFileName = '.\\初赛文档\\用例示例\\TrainData_2015.1.1_2015.2.19.txt'
#     trainData = prepareData.Data(trainFileName, n)
#     for k in range(15):
#         flavor = 'flavor' + str(k+1)
#         train = Train(trainData.divData, trainData.divLabel, n, flavor)
#         preData[flavor] = trainData.data[flavor][-n:]
#         loop_max = 10000
#         for i in range(loop_max):
#             train.forwardPropagation(train.x)
#             # temp = train.loss
#             train.backwardPropagation()
#             # if abs(temp - train.loss) < 1e-10:
#             #     break
#             # if i % 100 == 0:
#             #     print(train.loss)
#         W[flavor] = train.W
#         # print(W[flavor])
#         count = sum([train.y[j] == train.y_[j] for j in range(len(train.y))])
#         trainAccuracy = count/len(train.y)
#         # print('train ' + flavor + ' ' + 'Accuracy:', trainAccuracy)
#         t = 0
#         for p in range(m):
#             preData[flavor].append(round(train.dotProduct(preData[flavor][t: t+n-1], W[flavor])))
#             t = t + 1
#         preData[flavor] = preData[flavor][-m:]
#         # count = sum([preData[flavor][j] == testData.data[flavor][j] for j in range(len(preData[flavor]))])
#         # testAccuracy = count/len(preData[flavor])
#         # print(flavor + ' test accuracy: ', testAccuracy)
#
#     outputFname = 'output.txt'
#     totalSum = 0
#     for elem in preData:
#         totalSum += sum(preData[elem])
#     with open('output.txt', 'w') as f:
#         f.write(str(totalSum))
#         for elem in preData:
#             f.write('\n' + elem + ' ' + str(sum(preData[elem])))

# if __name__ == '__main__':
#     # main()


