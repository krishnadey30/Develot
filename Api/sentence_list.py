import VectorModule #C library for vector product
import mysql.connector as connector
from tasks import create_vector


'''
creating the database connection
database is mysql

'''
def database():
    mydb = connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="develot"
    )
    return mydb



'''
This function takes a sentence id and find the all 512 vector data from database and 
returns a vector of 1*512
'''
def get_vector(sid):
	mydb=database()
	mycursor = mydb.cursor()
	query = "SELECT value FROM Vector_data WHERE Sid = {}".format(sid)
	mycursor.execute(query)
	Vector =[]
	#(value,) as mycursor returns tuple
	for (value,) in mycursor:
		Vector.append(value)
	return Vector



''' 
this function will take the query sentence id and return a list of sentence ids in decreasing
order of cosine angle
'''
def vector_Similarity(sentence):
	mydb=database()
	mycursor = mydb.cursor(buffered=True)

	#checking if the sentence is available in database
	query = "SELECT Sid FROM Sentences WHERE sentence =%s LIMIT 1"
	mycursor.execute(query,(sentence,))

	#getting the count of returned rows
	count = mycursor.rowcount
	
	if count > 0:
		#if sentence is available
		myresult = mycursor.fetchall()
		#id of the searched sentence
		sentence_id = int(myresult[0][0])
	else:
		# else sending the sentence for vector formation
		result = create_vector.delay(sentence)
		while(result.ready()==False):
			pass
		#id of the searched sentence
		sentence_id = int(result.get())

	#getting the vector of query sentence
	Vector1  = get_vector(sentence_id)
	#getting the sentence id of all the sentences.
	query = "SELECT Sid,Did FROM Sentences where Did IS NOT Null"
	mycursor.execute(query)
	documents = []
	for (Sid,Tid) in mycursor:
		Sid = int(Sid)
		if Sid!=sentence_id:
			# getting the vector of a Sentence
			Vector2 = get_vector(Sid)
			if(len(Vector2)==512):
				#calling the C function for finding the angle between the query vector and different sentence
				angle = VectorModule.Product(Vector1,Vector2)
				documents.append((Tid,angle))
			else:
				print(Sid)

	#sorting the list of ids based on the angle between them
	documents = sorted(documents,key = lambda x:-x[1])

	#retreiving the tool ids, angles
	if len(documents)>0:
		all_doc_ids,all_angles = list(zip(*documents))
		all_doc_ids = [i for i in all_doc_ids  if i is not None]
	else:
		all_doc_ids = []

	return Doc_details(all_doc_ids)



def Doc_details(doc_ids):
	mydb=database()
	mycursor = mydb.cursor()
	doc_list=[]
	for each_id in doc_ids[:4]:
		if each_id is not None:
			query = "SELECT * FROM Docs WHERE Did = {} LIMIT 1".format(int(each_id))
			mycursor.execute(query)
			myresult = mycursor.fetchone()
			doc = {}
			doc['documentationUrl'] = myresult[1]
			doc['para'] = myresult[2]
			doc_list.append(doc)
	return doc_list

