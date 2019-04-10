import json
import mysql.connector as connector
def database():
    mydb = connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="develot"
    )
    return mydb
def read_json():
	filename = "django.json"
	with open(filename, 'r') as f:
		datastore = json.load(f)
	return datastore
def main():
	json_data = read_json()
	mydb=database()
	mycursor = mydb.cursor()
	for doc in json:
		sql =  "INSERT INTO Docs(Documentation_Url,para) Values (%s,%s)"
		val = (doc['link'],doc['para'])
		mycursor.execute(sql,val)
		mydb.commit()

if __name__ == '__main__':
	main()