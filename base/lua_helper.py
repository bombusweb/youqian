# -*- coding: utf-8 -*-

import redis_helper
import json
import time
redis_master=redis_helper.RedisMaster.instance().redis_master

# family=[]
# mother={'name':'mother'}
# father={'name':'father'}
# brother={'name':'brother'}
#     
# family.append(mother)
# family.append(father)
# family.append(brother)
#     
# family_json=json.dumps(family)
# print family_json
#     
# redis_master.hset('family','china',family_json)


# lua = """
# if redis.call("HEXISTS", KEYS[1],KEYS[2]) == 1 then
#     local family = redis.call('HGET',KEYS[1],KEYS[2])
#     if type(family) == "string" then
#     local family_list=cjson.decode(family)
#     local sun=cjson.decode(ARGV[1])
#     table.insert(family_list,sun)
#     local new_family=cjson.encode(family_list)
#     redis.call("HSET", KEYS[1],KEYS[2],new_family)
#     return (new_family)
#     end
# else
#     local empty_family = "[]"
#     redis.call("HSET", KEYS[1],KEYS[2],empty_family)
#     return 0
# end 
# """
 
lua = """
if redis.call("HEXISTS", KEYS[1],KEYS[2]) == 0 then
    local empty_list_string = "[]"
    redis.call("HSET", KEYS[1],KEYS[2],empty_list_string)
end 
    local list_in_redis = redis.call('HGET',KEYS[1],KEYS[2])
    local table_in_lua=cjson.decode(list_in_redis)
    local dict_from_argv=cjson.decode(ARGV[1])
    table.insert(table_in_lua,dict_from_argv)
    local json_from_table=cjson.encode(table_in_lua)
    redis.call("HSET", KEYS[1],KEYS[2],json_from_table)
    redis.call('expire',KEYS[1], ARGV[2])
    return (json_from_table)
"""

helper = redis_master.register_script(lua)
dict_to_redis={'key':time.time()}
json_to_redis=json.dumps(dict_to_redis) 
expire_time=500
print helper(keys=['setkey','filed'], args=[json_to_redis,expire_time])
