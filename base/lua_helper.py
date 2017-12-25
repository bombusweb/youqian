# -*- coding: utf-8 -*-

import redis_helper
import json

redis_master=redis_helper.RedisMaster.instance().redis_master

family=[]
mother={'name':'mother'}
father={'name':'father'}
brother={'name':'brother'}
    
family.append(mother)
family.append(father)
family.append(brother)
    
family_json=json.dumps(family)
print family_json
    
redis_master.hset('family','china',family_json)


lua = """
if redis.call("HEXISTS", KEYS[1],KEYS[2]) == 1 then
    local family = redis.call('HGET',KEYS[1],KEYS[2])
    if type(family) == "string" then
    local family_list=cjson.decode(family)
    local sun=cjson.decode(ARGV[1])
    table.insert(family_list,sun)
    local new_family=cjson.encode(family_list)
    redis.call("HSET", KEYS[1],KEYS[2],new_family)
    return (new_family)
    end
else
    return 0
end 
"""
 
 
helper = redis_master.register_script(lua)
son={'name':'son'}
son=json.dumps(son) 
print helper(keys=['family','china'], args=[son])
