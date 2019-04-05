from celery import Celery
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import json,arrow
import datetime as datetime
import mysql.connector as connector
import ast

#specifying the URL of the message broker we are using. Here using RabbitMQ (also the default option).
app = Celery('tasks', backend='rpc://', broker='pyamqp://develot:develot@localhost:5672/develot_host')

'''
Run the worker by executing our program with the worker argument
`celery -A tasks worker --loglevel=info`
'''


#this function Import the Universal Sentence Encoder's TF Hub module
def load_module():
	module_url = "https://tfhub.dev/google/universal-sentence-encoder-large/3"
	embed = hub.Module(module_url)
	return embed

'''
creating the database connection
database is mysql

schema of the tables

mysql> desc Sentences;
+------------------+-----------+------+-----+-------------------+-----------------------------+
| Field            | Type      | Null | Key | Default           | Extra                       |
+------------------+-----------+------+-----+-------------------+-----------------------------+
| Sid              | int(11)   | NO   | PRI | NULL              | auto_increment              |
| sentence         | text      | NO   |     | NULL              |                             |
| Date_of_Creation | timestamp | NO   |     | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP |
| Tid              | int(11)   | YES  | MUL | NULL              |                             |
+------------------+-----------+------+-----+-------------------+-----------------------------+
4 rows in set (0.01 sec)

mysql> desc Vector_data;
+---------+---------------+------+-----+---------+----------------+
| Field   | Type          | Null | Key | Default | Extra          |
+---------+---------------+------+-----+---------+----------------+
| data_id | int(11)       | NO   | PRI | NULL    | auto_increment |
| value   | double(14,13) | NO   |     | NULL    |                |
| Sid     | int(11)       | NO   | MUL | NULL    |                |
+---------+---------------+------+-----+---------+----------------+
3 rows in set (0.00 sec)

'''


def database():
    mydb = connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="develot"
    )
    return mydb


#defining the task

@app.task
def create_vector(sentence,tid=None):
	embed=load_module() #loading the module
	utc = arrow.utcnow()
	timestamp = utc.to('Asia/Kolkata').format("YYYY-MM-DD HH:mm:ss") #getting the timestamp
	with tf.Session() as session:
		#initialising the tensorflow vaiables
		session.run([tf.global_variables_initializer(), tf.tables_initializer()])
		embeddings = embed([sentence]) #creating the embedding
		message_embeddings=session.run(embeddings) 
		mydb=database()
		mycursor = mydb.cursor()
		#inserting the sentence in database
		if tid != None:
			sql = "INSERT INTO Sentences(sentence, Date_of_Creation,Tid) VALUES (%s,%s,%s)"
			val=(sentence,timestamp,tid)
		else:
			sql = "INSERT INTO Sentences(sentence, Date_of_Creation) VALUES (%s,%s)"
			val=(sentence,timestamp)
		mycursor.execute(sql,val)
		mydb.commit()
		#retriving the id of the inserted sentence
		id_no=mycursor.lastrowid
		#inserting each value of the vector in table with id of the sentence as foreign key
		sql = "INSERT INTO Vector_data(value, Sid) VALUES (%s,%s)"
		for message_embedding in np.array(message_embeddings).tolist():
			for data in message_embedding:
				val=(data,id_no)
				mycursor.execute(sql,val)
				mydb.commit()
		return id_no


#after changing the code please restart the supervisor
#use the following command
#   sudo systemctl restart celeryd



@app.task
def Add_Doc_to_database(doc):
	mydb=database()
	mycursor = mydb.cursor()
	sql =  "INSERT INTO Docs(Documentation_Url,para) Values (%s,%s)"
	val = (doc['url'],doc['para'])
	mycursor.execute(sql,val)
	mydb.commit()
	#retriving the id of the inserted sentence
	id_no=mycursor.lastrowid
	para = ast.literal_eval(doc['para'])
	result = create_vector.delay(para,id_no)
	# waiting till final sentence is completed
	while(result.ready()==False):
		pass
	return id_no
		
