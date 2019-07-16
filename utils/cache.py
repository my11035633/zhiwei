import memcache
cache=memcache.Client(["127.0.0.1:11211"],debug=True)   #开启memcache,前提，电脑上已经打开了memcache

#下面是对memcache的方法的封装，方便直接调用
def set(key, value, timeout=180):
    return cache.set(key,value,timeout)

def get(key):
    return cache.get(key)

def delete(key):
    return cache.delete(key )
