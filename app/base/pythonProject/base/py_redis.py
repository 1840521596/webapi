#!/usr/bin/python
#-*-coding:utf-8 -*-
import redis
class MyRedis(object):
    def __init__(self):
        try:
            self.r = redis.Redis(host="localhost", port=6379)
        except Exception as e:
            print "redis 连接失败，错误信息%s"%(str(e))
    def str_get(self,key):
        res = self.r.get(key)
        return res
    def str_set(self,key,value,ex=60):
        res = self.r.set(key,value,ex=ex)
        return res
    def del_key(self,key):
        res = self.r.delete(key)
        return res
if __name__ == "__main__":
    s = MyRedis()
    s.str_set("wc","1234")