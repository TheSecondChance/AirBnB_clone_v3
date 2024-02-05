#!/usr/bin/python3
""" This for Review objects that handles default API actions """
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def reviews(place_id):
    """
    This for Retrieves the list of all Review objects
    """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delReview(review_id):
    """ This for Deletes Review object """
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def postReview(place_id):
    """ This for Creates a Review object """

    createPlace = storage.get("Place", place_id)
    if not createPlace:
        abort(404)
    newReview = request.get_json()
    if not newReview:
        abort(400, "Not a JSON")
    if "user_id" not in newReview:
        abort(400, "Missing user_id")
    user_id = newReview['user_id']
    if not storage.get("User", user_id):
        abort(404)
    if "text" not in newReview:
        abort(400, "Missing text")

    review = Review(**newReview)
    setattr(review, 'place_id', place_id)
    storage.new(review)
    storage.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def reviewId(review_id):
    """ This for Retrieves a Review object """
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def putReview(review_id):
    """ Updates a Review object """
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")
    for k, v in body_request.items():
        if k not in ['id', 'user_id', 'place_id',
                     'created_at', 'updated_at']:
            setattr(review, k, v)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
