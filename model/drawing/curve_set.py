class CurveSet:
    def __init__(self):
        self._data = []
    #end

    def __getitem__(self, i):
        return self._data[i]
    #end

    def __iter__(self):
        self._index = 0
        return self
    #end
    def __next__(self):
        if self._index >= len(self._data): raise StopIteration
        self._index += 1
        return self._data[self._index-1]
    #end

    def __len__(self):
        return len(self._data)
    #end

#end
