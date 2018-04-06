import datetime
class Data(object):
    def __init__(self, oriData, n=10):
        # self.trainFname = '.\\初赛文档\\用例示例\\TrainData_2015.1.1_2015.2.19.txt'
        # self.trainFname = '.\\初赛文档\\用例示例\\data_total.txt'
        # self.trainFname = filename
        self.data = {
            'flavor1': [], 'flavor2': [], 'flavor3': [],
            'flavor4': [], 'flavor5': [], 'flavor6': [],
            'flavor7': [], 'flavor8': [], 'flavor9': [],
            'flavor10': [], 'flavor11': [], 'flavor12': [],
            'flavor13': [], 'flavor14': [], 'flavor15': []
        }
        self.n = n
        self.oriData = oriData
        self.divData = {
            'flavor1': [], 'flavor2': [], 'flavor3': [],
            'flavor4': [], 'flavor5': [], 'flavor6': [],
            'flavor7': [], 'flavor8': [], 'flavor9': [],
            'flavor10': [], 'flavor11': [], 'flavor12': [],
            'flavor13': [], 'flavor14': [], 'flavor15': []
        }
        self.divLabel = {
            'flavor1': [], 'flavor2': [], 'flavor3': [],
            'flavor4': [], 'flavor5': [], 'flavor6': [],
            'flavor7': [], 'flavor8': [], 'flavor9': [],
            'flavor10': [], 'flavor11': [], 'flavor12': [],
            'flavor13': [], 'flavor14': [], 'flavor15': []
        }
        self._readOriData()
        self._initData()
        self._countData()
        self.adjustData()

    def _readOriData(self):
        # with open(self.trainFname, 'r') as f:
        #     line = f.readline()
        #     while line:
        #         self.oriData.append(line)
        #         line = f.readline()
        for i in range(len(self.oriData)):
            self.oriData[i] = self.oriData[i].split('\t')[1:]
            self.oriData[i][1] = self.oriData[i][1].split(' ')[0]
            if i == 0:
                temp0 = self.oriData[0][1].split('-')
                temp0 = [int(j) for j in temp0]
                d0 = datetime.datetime(temp0[0], temp0[1], temp0[2])
            temp = self.oriData[i][1].split('-')
            temp = [int(j) for j in temp]
            d1 = datetime.datetime(temp[0], temp[1], temp[2])
            self.oriData[i][1] = (d1 - d0).days

    def _initData(self):
        num = self.oriData[-1][1] + 1
        for elem in self.data:
            self.data[elem] = [0] * num

    def _countData(self):
        for elem in self.oriData:
            t = int(elem[0].split('r')[1])
            if t <= 15:
                self.data[elem[0]][elem[1]] += 1

    def _divideData(self, vector):
        dataLen = len(vector)
        i = 0
        j = 0
        temp = []
        x = []
        label = []
        while i != dataLen:
            if (i - j) != self.n:
                temp.append(vector[i])
                i = i + 1
            else:
                x.append(temp)
                label.append(vector[i])
                j = j + 1
                i = j
                temp = []
        return x, label

    def adjustData(self):
        for elem in self.data:
            self.divData[elem] = self._divideData(self.data[elem])[0]
            self.divLabel[elem] = self._divideData(self.data[elem])[1]

class InputMessage(object):
    def __init__(self, inputArray):
        self.serverCPU = int(inputArray[0].split(' ')[0])
        self.serverMEM = int(inputArray[0].split(' ')[1])
        self.serverDisk = int(inputArray[0].split(' ')[2])
        self.flavorNum = int(inputArray[2])
        self.flavor = []
        for item in inputArray[3:self.flavorNum+3]:
            self.flavor.append(item.split(' ')[0])
        self.CPUorMEM = inputArray[-4].strip()
        self.startTime = inputArray[-2].split(' ')[0].strip()
        self.endTime = inputArray[-1].split(' ')[0].strip()


if __name__ == '__main__':
    data = Data('.\\初赛文档\\用例示例\\TrainData_2015.1.1_2015.2.19.txt', 9)
    # data._readOriData()
    # data._initData()
    # data._countData()
    # data.adjustData()
    a = data.divData
    b = data.divLabel

