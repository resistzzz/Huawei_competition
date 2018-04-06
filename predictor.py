import prepareData
import predict
import datetime

def predict_vm(ecs_lines, input_lines):
    # Do your work from here#
    n = 9
    result = []
    if ecs_lines is None:
        print ('ecs information is none')
        return result
    if input_lines is None:
        print ('input file information is none')
        return result

    trainData = prepareData.Data(ecs_lines, n)

    inputData = prepareData.InputMessage(input_lines)

    start = inputData.startTime.split('-')
    end = inputData.endTime.split('-')
    start = datetime.datetime(int(start[0]), int(start[1]), int(start[2]))
    end = datetime.datetime(int(end[0]), int(end[1]), int(end[2]))
    m = (end - start).days
    loop_max = 10000
    preResult = {}
    W = {}
    for elem in inputData.flavor:
        train = predict.Train(trainData.divData, trainData.divLabel, n, elem)
        preResult[elem] = trainData.data[elem][-n:]
        for i in range(loop_max):
            train.forwardPropagation(train.x)
            train.backwardPropagation()
            # if i % 100 == 0:
            #     print(elem + ':' , train.loss)
        W[elem] = train.W
        t = 0
        for p in range(m):
            preResult[elem].append(round(train.dotProduct(preResult[elem][t: t + n - 1], W[elem])))
            t = t + 1
        preResult[elem] = preResult[elem][-m:]

    totalSum = 0
    for elem in preResult:
        totalSum += sum(preResult[elem])
    result.append(str(totalSum))

    for elem in preResult:
        preResult[elem] = sum(preResult[elem])
        result.append(elem + ' ' + str(preResult[elem]))
    result.append('')
    # result.append('predict end')

    pack = predict.Packing(preResult, inputData)

    pack.packing()

    packNum = len(pack.boxes)
    result.append(str(packNum))

    temp = [0] * pack.flavorsNum
    for i in range(packNum):
        for elem in pack.boxes[i][0]:
            temp[elem[0]-1] += 1
        result.append(str(i+1) + ' ')
        for j in range(len(temp)):
            if temp[j] != 0:
                result[-1] = result[-1] + 'flavor' + str(j+1) + ' ' + str(temp[j]) + ' '

    # print(ecs_lines)
    # for item in ecs_lines:
    #     values = item.split("\t")
    #     uuid = values[0]
    #     flavorName = values[1]
    #     createTime = values[2]

    # for index, item in input_lines:
    #     print ("index of input data")

    return result

