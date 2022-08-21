import os
import json

class DataBlock():
    data = {}
    lazy_loading = True
    def __init__(self, name, cache_dir="dataset"):
        self.data = {}
        if cache_dir == None:
            cache_dir = name
        self.set_cache_dir(cache_dir+"/"+name)
        # if not self.lazy_loading:
          
    
    def set_cache_dir(self, dir):
        self.cache_dir = dir
        try:
            os.makedirs(self.cache_dir, exist_ok=True)
        except FileExistsError:
            pass

    def __enter__(self):
        return self
     
    def __exit__(self, exc_type, exc_value, exc_traceback):
        print(exc_type)
        print(exc_value)
        print(exc_traceback)
    
    def add(self, id, data):
        self.data[id] = data
    
    def set(self, id, data):
        self.store_data(id, data)
        self.add(id, data)

    def get(self, id, handler=None, no_kwargs=False, no_args=False, args={}, **kwargs):

        if id in self.data:
          return self.data[id]
        elif self.check_cache(id):
            d = self.load_data(id)
            self.add(id, d)
            return d
        else:
            return self.raw_get(id, handler, no_kwargs,no_args, args)
    def raw_get(self, id, handler,no_kwargs=False, no_args=False,  args={}, **kwargs):
        if handler is None:
            return None
        if no_args:
            d = handler()
        elif no_kwargs:
            d = handler(id)
        else:
            d = handler(id, kwargs=args)
        self.store_data(id, d)
        self.add(id, d)
        return d

    def clear_memory(self):
        del(self.data)
        self.data = {}
    def store_data(self, id, data):
        with open(f"{self.cache_dir}/{id}.json","w") as fp:
          json.dump(data, fp, indent=2) ## TODO: Handle different data types

    def load_data(self, id):
        with open(f"{self.cache_dir}/{id}.json","r") as fp:
          data = json.load(fp)
        return data
    
    def check_cache(self, id):
        if os.path.isfile(f"{self.cache_dir}/{id}.json"):
          size = os.path.getsize(f"{self.cache_dir}/{id}.json")
          if size > 0:
            return True
        
        return False
 
# with DataBlock() as db:
#     # db.lazy_loading = True # Using this property to avoid loading data unless called
#     # db.add(id, data)
#     # db.clear(id) #Remove from cache
#     # db.get(id, handler(id)) # Get it from cache or call the handler if not in cache
#     print('with statement block')

class DataBars():
    def __init__(self, name) -> None:
        self.name = name
        self.bars = {}
    def add_bar(self, bar_name:str , bar:tuple):
        if len(bar) != 2:
            raise ValueError("Bar must be a tuple of length 2")
        if not isinstance(bar[0], float) or not isinstance(bar[1], float):
            raise ValueError("Bar must be a tuple of floats")
        self.bars[bar_name] = bar
    
    def check_bars(self, value:float):
        bars = []
        for name, bar in self.bars.items():
            if value >= bar[0] and value < bar[1]:
                bars.append(name)
        return bars
