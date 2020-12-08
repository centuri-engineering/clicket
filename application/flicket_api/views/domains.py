#! python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

"""
    Categories
    ==========

    Get Request By ID
    ~~~~~~~~~~~~~~~~~~

    .. http:get:: /flicket-api/request/(int:request_id)

        **Request**

        .. sourcecode:: http

            GET /flicket-api/request/1 HTTP/1.1
            HOST: localhost:5000
            Accept: application/json
            Authorization: Bearer <token>

        **Response**

        .. sourcecode:: http

            HTTP/1.0 200 OK
            Content-Length: 282
            Content-Type: application/json
            Date: Sun, 30 Jun 2019 12:55:57 GMT
            Server: Werkzeug/0.14.1 Python/3.7.3

            {
                "request": "Dataset",
                "id": 1,
                "links": {
                    "requests": "http://127.0.0.1:5000/flicket-api/requests/",
                    "self": "http://127.0.0.1:5000/flicket-api/request/1"
                }
            }

    Get Requests
    ~~~~~~~~~~~~~~

    .. http:get:: /flicket-api/requests/

        **Request**

        .. sourcecode:: http

            GET /flicket-api/requests/ HTTP/1.1
            HOST: localhost:5000
            Accept: application/json
            Authorization: Bearer <token>

        **Response**

        .. sourcecode:: http

            HTTP/1.0 200 OK
            Content-Length: 5192
            Content-Type: application/json
            Date: Sun, 30 Jun 2019 12:51:02 GMT
            Server: Werkzeug/0.14.1 Python/3.7.3

            {
                "_links": {
                    "next": null,
                    "prev": null,
                    "self": "http://127.0.0.1:5000/flicket-api/requests/?page=1&per_page=50"
                },
                "_meta": {
                    "page": 1,
                    "per_page": 50,
                    "total_items": 15,
                    "total_pages": 1
                },
                "items": [
                    {
                        "request": "Approved Suppliers",
                        "id": 14,
                        "links": {
                            "requests": "http://127.0.0.1:5000/flicket-api/requests/",
                            "self": "http://127.0.0.1:5000/flicket-api/request/14"
                        }
                    },
                    {
                        "request": "Dataset",
                        "id": 1,
                        "links": {
                            "requests": "http://127.0.0.1:5000/flicket-api/requests/",
                            "self": "http://127.0.0.1:5000/flicket-api/request/1"
                        }
                    },
                    {
                        "request": "ECR",
                        "id": 3,
                        "links": {
                            "requests": "http://127.0.0.1:5000/flicket-api/requests/",
                            "self": "http://127.0.0.1:5000/flicket-api/request/3"
                        }
                    },
                    {
                        "request": "Holidays",
                        "id": 12,
                        "links": {
                            "requests": "http://127.0.0.1:5000/flicket-api/requests/",
                            "self": "http://127.0.0.1:5000/flicket-api/request/12"
                        }
                    }
                ]
            }

"""

from flask import jsonify, request, url_for

from .sphinx_helper import api_url
from . import bp_api
from application import app, db
from application.flicket.models.flicket_models import FlicketRequest
from application.flicket_api.views.auth import token_auth
from application.flicket_api.views.errors import bad_request


@bp_api.route(api_url + "request/<int:id>", methods=["GET"])
@token_auth.login_required
def get_request(id):
    return jsonify(FlicketRequest.query.get_or_404(id).to_dict())


@bp_api.route(api_url + "requests/", methods=["GET"])
@token_auth.login_required
def get_requests():
    requests = FlicketRequest.query.order_by(FlicketRequest.request.asc())
    page = request.args.get("page", 1, type=int)
    per_page = min(
        request.args.get("per_page", app.config["posts_per_page"], type=int), 100
    )
    data = FlicketRequest.to_collection_dict(
        requests, page, per_page, "bp_api.get_requests"
    )
    return jsonify(data)


@bp_api.route(api_url + "requests", methods=["POST"])
@token_auth.login_required
def create_request():
    data = request.get_json() or {}

    if "request" not in data:
        return bad_request("Must include request name")

    if FlicketRequest.query.filter_by(request=data["request"]).first():
        return bad_request("Request  already exists.")

    request = FlicketRequest(data["request"])
    db.session.add(request)
    db.session.commit()

    response = jsonify(request.to_dict())
    response.status_code = 201
    response.headers["Location"] = url_for("bp_api.get_request", id=request.id)
    return response
