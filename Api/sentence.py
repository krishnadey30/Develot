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
		all_docs = vector_Similarity(sentence)
		doc['docs']=all_docs
		
		# Create a JSON representation of the resource
		resp.body = json.dumps(doc, ensure_ascii=False)
		# The following line can be omitted because 200 is the default
		# status returned by the framework, but it is included here to
		# illustrate how this may be overridden as needed.
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

		

