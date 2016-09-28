#!/usr/bin/python
from rq import Connection, Queue
from redis import Redis
from pythast_engine  import generate_call,command
redis_conn = Redis()
q = Queue(connection=redis_conn)
job = q.enqueue(command, 'USER','PASS','core show hints')
print job
