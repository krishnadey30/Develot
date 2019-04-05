import falcon,json
from sentence_list import vector_Similarity,Doc_details
from tasks import Add_Doc_to_database


class TestResource(object):
    def on_get(self, req, res):
        """Handles all GET requests."""
        res.status = falcon.HTTP_200  # This is the default status
        res.body = ('This is me, Falcon, serving a resource!')

class Search(object):
	def on_get(self, req, resp):
		doc = {}
        #reading the query sentence
		sentence=req.get_param('sentence',required=True)

		#getting all the matching docs
		all_doc_ids = vector_Similarity(sentence)
		doc['doc_ids']=all_doc_ids
		
		# Create a JSON representation of the resource
		resp.body = json.dumps(doc, ensure_ascii=False)
		# The following line can be omitted because 200 is the default
		# status returned by the framework, but it is included here to
		# illustrate how this may be overridden as needed.
		resp.status = falcon.HTTP_200


class Result(object):
	def on_get(self,req,resp):
		doc_ids=req.get_param('doc_ids',required=True)
		doc_ids=json.loads(doc_ids)
		#getting the details of all the Documentations in the list
		Doc_list = Doc_details(doc_ids)

		doc ={}
		doc['data'] = Doc_list
		resp.body = json.dumps(doc, ensure_ascii=False)
		resp.status = falcon.HTTP_200

	

class Add_Doc(object):
	def on_post(self,req,resp):
		doc_data = req.stream.read()
		data = json.loads(doc_data.decode('utf8').replace("'",'"'))
		result = Add_Doc_to_database.delay(data['doc'])
		while(result.ready()==False):
			pass
		doc_id = result.get()
		doc = {}
		doc['doc_id']=doc_id
		resp.body = json.dumps(doc, ensure_ascii=False)
		resp.status = falcon.HTTP_200

		

