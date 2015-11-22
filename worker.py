from retask import Queue,Task


q = Queue('instruction')
topic = ['org.fedoraproject.dev.__main__.autocloud.image.failed','org.fedoraproject.dev.__main__.autocloud.image.success']
data = { 'name' : 'test' , 'type' : 'create' , 'queue_name' : 'queue_test' , 'topic' : topic }
task = Task(data)
q.connect()
q.enqueue(task)
q = Queue('queue_test')
q.connect()
while True:
	task = q.wait()
	print task.data
