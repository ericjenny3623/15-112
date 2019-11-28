

class Logger():

    def __init__(self):
        self.dict = {}
        self.time = []
        self.index = 0

    def log(self, time, dataSet, cat=""):
        if time > self.time[-1]:
            self.index += 1
            self.time.append(time)
            for key in self.dict:
                try:
                    strippedKey = key[len(cat):]
                except:
                    strippedKey = key
                if strippedKey in dataSet:
                    self.dict[key].data.append(dataSet[strippedKey])
                    dataSet.remove(strippedKey)
                else:
                    self.dict[key].data.append(None)
            for key in dataSet:
                self.dict[cat+key] = DataList(cat+key, self.index)
                self.dict[cat+key].append(dataSet[key])
        elif time == self.time[-1]:





class DataList():

    def __init__(self, label, noneLength=0):
        self.data = [None for i in range(noneLength)]
        self.label = label

    def __repr__(self):
        return label + ": " + str(self.data)


if __name__ == "__main__":
    l = DataList("test")
