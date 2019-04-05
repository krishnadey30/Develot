import falcon

api = application = falcon.API()
from sentence import Search,Add_Doc,Result,TestResource

search = Search()
add_doc = Add_Doc()
result = Result()
test_resource = TestResource()
# Add a route to serve the resource
api.add_route('/test',test_resource)
api.add_route('/search',search)
api.add_route('/add_doc',add_doc)
api.add_route('/get_result',result)

