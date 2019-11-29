

class Logger():

    def __init__(self):
        self.dict = {}
        self.time = DataList("time")
        self.index = 0

    def log(self, time, dataSet, cat=""):
        if self.index == 0 or time > self.time.data[-1]:
            self.index += 1
            self.time.append(time)
            for key in self.dict:
                try:
                    strippedKey = key[len(cat):]
                except:
                    strippedKey = key
                if strippedKey in dataSet:
                    self.dict[key].append(dataSet[strippedKey])
                    dataSet.pop(strippedKey)
                else:
                    self.dict[key].append(None)
            for key in dataSet:
                self.dict[cat+key] = DataList(cat+key, self.index)
                self.dict[cat+key].append(dataSet[key])
        elif time == self.time.data[-1]:
            for key in self.dict:
                try:
                    strippedKey = key[len(cat):]
                except:
                    strippedKey = key
                if strippedKey in dataSet:
                    self.dict[key].data[self.index] = dataSet[strippedKey]
                    dataSet.pop(strippedKey)
            for key in dataSet:
                self.dict[cat+key] = DataList(cat+key, self.index)
                self.dict[cat+key].append(dataSet[key])


class DataList():

    def __init__(self, label, noneLength=0):
        self.data = [None for i in range(noneLength)]
        self.label = label
        self.min = 0
        self.max = 0

    def append(self, data):
        self.data.append(data)
        if data is None:
            return
        if data < self.min:
            self.min = data
        elif data > self.max:
            self.max = data

    def __repr__(self):
        return self.label + ": " + str(self.data)


if __name__ == "__main__":
    l = DataList("test")
