# Copyright 2008 Tom Oakley 
# This file is part of pylibra.
#
# pylibra is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pylibra is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pylibra.  If not, see <http://www.gnu.org/licenses/>.

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
        self.__data = self.__data[:id] + self.__data[(id+1):]
        
    def __str__(self):
        "Prints readable representation of data."
        return str(self.__data)
