from typing import Union, List, Tuple, Any, Callable
from dataset import DataSetItem
from dataset import DataSetInterface

class DataSet(DataSetInterface):
    def __init__(self, items: Union[List[DataSetItem], Tuple[DataSetItem, ...]] = []):
        super().__init__(items)
        self.items = list(items)

    def __setitem__(self, name: str, id_content: Tuple[int, Any]):
        self += DataSetItem(name, id_content[0], id_content[1])
    
    def __iadd__(self, item):
        for i in range(len(self.items)):
            if self.items[i].name == item.name:
                self.items[i] = item
                return self
        l = self.items
        self.items = l + [item]
        return self

    def __delitem__(self, name):
        i = 0
        while i < len(self.items):
            if self.items[i].name == name:
                self.items.pop(i)
            i += 1

    def __contains__(self, name):
        a = False
        for data in self.items:
            if data.name == name:
                a = True
        return a

    def __getitem__(self, name):
        for data in self.items:
            if data.name == name:
                return data

    def __and__(self, dataset):
        result = DataSet() 
        for item in self.items:
            if item.name in dataset:
                 result += item
        return result

    def __or__(self, dataset):
        result = DataSet(self.items)  
        for item in dataset:
            result += item
        return result

    def __iter__(self):
        if self.iterate_sorted:
            items = sorted(
                self.items,
                key=lambda x: getattr(x, self.iterate_key),
                reverse=self.iterate_reversed
            )
        else:
            items = list(self.items)  
            if self.iterate_reversed:
                items.reverse() 

        for item in items:
            yield item

    def filtered_iterate(self, filter: Callable[[str, int], bool]):
        for data in self.items:
            if filter(data.name, data.id):
                yield data

    def __len__(self):
        return len(self.items)
