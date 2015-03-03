import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)
# r = redis.StrictRedis(host='localhost', port=6000, db=0)
p = r.pubsub() # create pubsub object

# channels and patterns can be subscribed:
p.subscribe('my-first-channel', 'my-second-channel') # channels
p.psubscribe('my-*') # pattern

# pubsub instance now subscribed to those channels/patterns

p.get_message()
p.get_message()
p.get_message()

# every message read from pubsub instance will be a dictionary
# with the following keys:

# type - one of the following: subscribe, unsubscribe, psubscribe, punsubscribe, message, pmessage
# channel - the channel (un)subscribed to or the chennel a message was published to
# pattern - pattern that matched a published message's channel. None for all case but 'pmessage' types
# data - the message data



##################### original example ##############################################
# r_server = redis.Redis('localhost') #this line creates a new Redis object and
#                                     #connects to our redis server
# r_server.set('test_key', 'test_value') #with the created redis object we can
#                                         #submits redis commands as its methods
                                        
# print 'previous set key ' + r_server.get('test_key') # the previous set key is fetched

# '''In the previous example you saw that we introduced a redis
# data type: the string, now we will set an integer and try to
# increase its value using redis object built-in methods'''

# r_server.set('counter', 1) #set an integer to a key
# r_server.incr('counter') #we increase the key value by 1, has to be int
# print 'the counter was increased! '+ r_server.get('counter') #notice that the key is increased now

# r_server.decr('counter') #we decrease the key value by 1, has to be int
# print 'the counter was decreased! '+ r_server.get('counter') #the key is back to normal


# '''Now we are ready to jump into another redis data type, the list, notice 
# that they are exactly mapped to python lists once you get them'''

# r_server.rpush('list1', 'element1') #we use list1 as a list and push element1 as its element

# r_server.rpush('list1', 'element2') #assign another element to our list
# r_server.rpush('list2', 'element3') #the same

# print 'our redis list len is: %s'% r_server.llen('list1') #with llen we get our redis list size right from redis

# print 'at pos 1 of our list is: %s'% r_server.lindex('list1', 1) #with lindex we query redis to tell us which element is at pos 1 of our list

# '''sets perform identically to the built in Python set type. 
# Simply, sets are lists but, can only have unique values.'''

# r_server.sadd("set1", "el1")
# r_server.sadd("set1", "el2")
# r_server.sadd("set1", "el2")

# print 'the member of our set are: %s'% r_server.smembers("set1")

# '''basically our redis client can do any command supported by redis, 
# check out redis documentation for available commands for your server'''
#################################################################################################