from tasks import create_vector
import mysql.connector as connector
def database():
    mydb = connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="develot"
    )
    return mydb


def main():
	mydb=database()
	mycursor = mydb.cursor(buffered=True)
	query = "SELECT Did,para FROM Docs where vector_created = 0"
	mycursor.execute(query)
	for (Did,para) in mycursor:
		Did = int(Did)
		result = create_vector.delay(para,Did)
		while(result.ready()==False):
			pass
		if(result.status == "SUCCESS"):
			mycursor2 = mydb.cursor(buffered=True)
			query1 = "UPDATE Docs SET vector_created = 1 where Did = %s"
			val = (Did,)
			mycursor2.execute(query1,val)
		else:
			print(Did)

if __name__ == '__main__':
	main()