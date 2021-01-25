from flask import Response, request
from flask_restful import Resource
from mongoengine import DoesNotExist, Q
import models
import json

class CommentListEndpoint(Resource):
    
    def get(self):
        #TODO: implement GET endpoint
        #list all of comments that are currnetly in my db
        data = models.Comment.objects
        # formatting the output JSON
        data = data.to_json()
        return Response(data, mimetype="application/json", status=200)

    def post(self):
        #makes new comments
        body = request.get_json()
        #do some data validation
        #comment = Comment Text
        #author = name of author
        #post = the id of post
        print(body)
        comment = models.Comment(**body).save()
        serialized_data = {
            'id': str(comment.id),
            'message': 'Post {0} successfully created.'.format(comment.id)
        }
        return Response(json.dumps(serialized_data), mimetype="application/json", status=201)
        
class CommentDetailEndpoint(Resource):
    def put(self, id):
        # TODO: implement PUT endpoint
        comment = models.Comment.objects.get(id=id)
        request_data = request.get_json()
        #comment.id = request_data.get('id')
        comment.comment = request_data.get('comment')
        comment.author = request_data.get('author')
        comment.save()
        print(comment.to_json())
        return Response(comment.to_json(), mimetype="application/json", status=200)


        #return Response(json.dumps([]), mimetype="application/json", status=200)
    
    def delete(self, id):
        # TODO: implement DELETE endpoint
        comment = models.Comment.objects.get(id=id)
        comment.delete()
        serialized_data = {
            'message': 'Post {0} successfully deleted.'.format(id)
        }
        return Response(json.dumps(serialized_data), mimetype="application/json", status=200)

        #return Response(json.dumps([]), mimetype="application/json", status=200)

    def get(self, id):
        # TODO: implement GET endpoint
        comment = models.Comment.objects.get(id=id)
        return Response(comment.to_json(), mimetype="application/json", status=200)
        #return Response(json.dumps([]), mimetype="application/json", status=200)

def initialize_routes(api):
    api.add_resource(CommentListEndpoint, '/api/comments', '/api/comments/')
    api.add_resource(CommentDetailEndpoint, '/api/comments/<id>', '/api/comments/<id>/')
    # api.add_resource(CommentListEndpoint, '/api/posts/<post_id>/comments', '/api/posts/<post_id>/comments/')
    # api.add_resource(CommentDetailEndpoint, '/api/posts/<post_id>/comments/<id>', '/api/posts/<post_id>/comments/<id>/')