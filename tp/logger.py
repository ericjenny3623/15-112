

class Logger():

    def __init__(self):
        self.dict = {}
        self.time = DataList("time")
        self.index = 0
        self.loggers = {}

    def registerLoggerDict(self, logDict, name):
        if name not in self.loggers:
            self.loggers[name] = logDict

    def log(self, time):
        assert (self.index == 0 or time > self.time.data[-1],
                "Time value in past")
        self.index += 1
        self.time.append(time)

        for genre in self.loggers:
            logDict = self.loggers[genre]
            for key in logDict:
                masterKey = genre + "." + key
                self.dict[masterKey].append(logDict[key])

        for listKey in self.dict:
            assert(len(self.dict[listKey]) == self.index+1,
                    "Logger dict lists not equal length, category not updated")

    def logIndividual(self, time, dataSet, prefix=""):
        if self.index == 0 or time > self.time.data[-1]:
            for key in self.dict:
                try:
                    strippedKey = key[len(prefix):]
                except:
                    strippedKey = key
                if strippedKey in dataSet:
                    self.dict[key].append(dataSet[strippedKey])
                    dataSet.pop(strippedKey)
                else:
                    self.dict[key].append(None)
            for key in dataSet:
                self.dict[prefix+key] = DataList(prefix+key, self.index)
                self.dict[prefix+key].append(dataSet[key])
        elif time == self.time.data[-1]:
            for key in self.dict:
                try:
                    strippedKey = key[len(prefix):]
                except:
                    strippedKey = key
                if strippedKey in dataSet:
                    self.dict[key].data[self.index] = dataSet[strippedKey]
                    dataSet.pop(strippedKey)
            for key in dataSet:
                self.dict[prefix+key] = DataList(prefix+key, self.index)
                self.dict[prefix+key].append(dataSet[key])


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
