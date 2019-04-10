from tasks import create_vector

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
	query = "SELECT Did,para FROM Docs"
	mycursor.execute(query)
	for (Did,para) in mycursor:
		Did = int(Did)
		result = create_vector.delay(para,Did)
		while(result.ready()==False):
			pass

if __name__ == '__main__':
	main()