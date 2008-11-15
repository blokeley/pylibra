"Abstract tabular data model."

class Model:
    "Model of tabular data."
    
    def __init__(self, columns=None):
        self.columns = columns
        self.__data = []
        
    def getColumns(self):
        return self.columns
    
    # Turn columns into a read-only property
    columns = property(getColumns)
    
    def getData(self):
        return self.__data
    
    data = property(getData)
        
    def addRow(self, row):
        self.__data.append(row)
        
    def removeRow(self, id):
#        self.__data = self.__data[:id] = self.__data[id:]
        self.__data = self.__data[:id] + self.__data[(id+1):]
        
    def __str__(self):
        "Prints readable representation of data."
        return str(self.__data)
