import falcon

api = application = falcon.API()
from sentence import Search,Add_Doc,Result

search = Search()
add_doc = Add_Doc()
result = Result()
# Add a route to serve the resource
api.add_route('/search',search)
api.add_route('/add_doc',add_doc)
api.add_route('/get_result',result)

