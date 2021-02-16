#! python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

"""
    Categories
    ==========

    Get Request By ID
    ~~~~~~~~~~~~~~~~~~

    .. http:get:: /flicket-api/request_type/(int:request_type_id)

        **Request**

        .. sourcecode:: http

            GET /flicket-api/request_type/1 HTTP/1.1
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
                    "request_types": "http://127.0.0.1:5000/flicket-api/request_types/",
                    "self": "http://127.0.0.1:5000/flicket-api/request_type/1"
                }
            }

    Get Requests
    ~~~~~~~~~~~~~~

    .. http:get:: /flicket-api/request_types/

        **Request**

        .. sourcecode:: http

            GET /flicket-api/request_types/ HTTP/1.1
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
                    "self": "http://127.0.0.1:5000/flicket-api/request_types/?page=1&per_page=50"
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
                            "request_types": "http://127.0.0.1:5000/flicket-api/request_types/",
                            "self": "http://127.0.0.1:5000/flicket-api/request_type/14"
                        }
                    },
                    {
                        "request": "Dataset",
                        "id": 1,
                        "links": {
                            "request_types": "http://127.0.0.1:5000/flicket-api/request_types/",
                            "self": "http://127.0.0.1:5000/flicket-api/request_type/1"
                        }
                    },
                    {
                        "request": "ECR",
                        "id": 3,
                        "links": {
                            "request_types": "http://127.0.0.1:5000/flicket-api/request_types/",
                            "self": "http://127.0.0.1:5000/flicket-api/request_type/3"
                        }
                    },
                    {
                        "request": "Holidays",
                        "id": 12,
                        "links": {
                            "request_types": "http://127.0.0.1:5000/flicket-api/request_types/",
                            "self": "http://127.0.0.1:5000/flicket-api/request_type/12"
                        }
                    }
                ]
            }

"""

from flask import jsonify, request, url_for

from .sphinx_helper import api_url
from . import bp_api
from application import app, db
from application.flicket.models.flicket_models import FlicketRequestType
from application.flicket_api.views.auth import token_auth
from application.flicket_api.views.errors import bad_request


@bp_api.route(api_url + "request_type/<int:id>", methods=["GET"])
@token_auth.login_required
def get_request_type(id):
    return jsonify(FlicketRequestType.query.get_or_404(id).to_dict())


@bp_api.route(api_url + "request_types/", methods=["GET"])
@token_auth.login_required
def get_request_types():
    request_types = FlicketRequestType.query.order_by(
        FlicketRequestType.request_type.asc()
    )
    page = request.args.get("page", 1, type=int)
    per_page = min(
        request.args.get("per_page", app.config["posts_per_page"], type=int), 100
    )
    data = FlicketRequestType.to_collection_dict(
        request_types, page, per_page, "bp_api.get_request_types"
    )
    return jsonify(data)


@bp_api.route(api_url + "request_types", methods=["POST"])
@token_auth.login_required
def create_request_type():
    data = request.get_json() or {}

    if "request_type" not in data:
        return bad_request("Must include request_type name")

    if FlicketRequestType.query.filter_by(request_type=data["request_type"]).first():
        return bad_request("Request  already exists.")

    request_type = FlicketRequestType(data["request_type"])
    db.session.add(request_type)
    db.session.commit()

    response = jsonify(request_type.to_dict())
    response.status_code = 201
    response.headers["Location"] = url_for(
        "bp_api.get_request_type", id=request_type.id
    )
    return response
