from pymongo import MongoClient
# import multiprocessing

var_url = f"mongodb+srv://joeysabusido:genesis11@cluster0.bmdqy.mongodb.net/ldglobal?retryWrites=true&w=majority"



# create the MongoClient before forking
client = MongoClient(var_url,maxPoolSize=None)
mydb = client['ldglobal']

# create a new process
# p = multiprocessing.Process(target=mydb)

# start the process
# p.start()

# wait for the process to finish
# p.join()

# continue to use the original client instance in the parent process
