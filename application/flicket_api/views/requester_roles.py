#! python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

"""
    Status
    ======

    Get Status By ID
    ~~~~~~~~~~~~~~~~

    .. http:get:: /flicket-api/status/(int:status_id)

        **Request**

        .. sourcecode:: http

            GET /flicket-api/requester_role/1 HTTP/1.1
            HOST: localhost:5000
            Accept: application/json
            Authorization: Bearer <token>


        **Response**

        .. sourcecode:: http

            HTTP/1.0 200 OK
            Content-Length: 175
            Content-Type: application/json
            Date: Mon, 01 Jul 2019 11:17:00 GMT
            Server: Werkzeug/0.14.1 Python/3.7.3

            {
                "id": 1,
                "links": {
                    "self": "http://127.0.0.1:5000/flicket-api/requester_role/1",
                    "requester_roles": "http://127.0.0.1:5000/flicket-api/requester_roles/"
                },
                "requester_role": "Open"
            }


    Get RequesterRoles
    ~~~~~~~~~~~~

    .. http:get:: /flicket-api/requester_roles/

        **Request**

        .. sourcecode:: http

            GET /flicket-api/requester_roles/ HTTP/1.1
            HOST: localhost:5000
            Accept: application/json
            Authorization: Bearer <token>

        **Response**

        .. sourcecode:: http

            HTTP/1.0 200 OK
            Content-Length: 1114
            Content-Type: application/json
            Date: Mon, 01 Jul 2019 11:18:23 GMT
            Server: Werkzeug/0.14.1 Python/3.7.3

            {
                "_links": {
                    "next": null,
                    "prev": null,
                    "self": "http://127.0.0.1:5000/flicket-api/institutes/?page=1&per_page=50"
                },
                "_meta": {
                    "page": 1,
                    "per_page": 50,
                    "total_items": 4,
                    "total_pages": 1
                },
                "items": [
                    {
                        "id": 1,
                        "links": {
                            "self": "http://127.0.0.1:5000/flicket-api/requester_role/1",
                            "requester_roles": "http://127.0.0.1:5000/flicket-api/requester_roles/"
                        },
                        "requester_role": "Open"
                    },
                    {
                        "id": 2,
                        "links": {
                            "self": "http://127.0.0.1:5000/flicket-api/requester_role/2",
                            "requester_roles": "http://127.0.0.1:5000/flicket-api/requester_roles/"
                        },
                        "requester_role": "Closed"
                    },
                    {
                        "id": 3,
                        "links": {
                            "self": "http://127.0.0.1:5000/flicket-api/requester_role/3",
                            "requester_roles": "http://127.0.0.1:5000/flicket-api/requester_roles/"
                        },
                        "requester_role": "In Work"
                    },
                    {
                        "id": 4,
                        "links": {
                            "self": "http://127.0.0.1:5000/flicket-api/requester_role/4",
                            "requester_roles": "http://127.0.0.1:5000/flicket-api/requester_roles/"
                        },
                        "requester_role": "Awaiting Information"
                    }
                ]
            }

"""

from flask import jsonify, request

from .sphinx_helper import api_url
from . import bp_api
from application import app
from application.flicket.models.flicket_models import FlicketRequesterRole
from application.flicket_api.views.auth import token_auth


@bp_api.route(api_url + "requester_role/<int:id>", methods=["GET"])
@token_auth.login_required
def get_requester_role(id):
    return jsonify(FlicketRequesterRole.query.get_or_404(id).to_dict())


@bp_api.route(api_url + "requester_roles/", methods=["GET"])
@token_auth.login_required
def get_requester_roles():
    page = request.args.get("page", 1, type=int)
    per_page = min(
        request.args.get("per_page", app.config["posts_per_page"], type=int), 100
    )
    data = FlicketRequesterRole.to_collection_dict(
        FlicketRequesterRole.query, page, per_page, "bp_api.get_requester_roles"
    )

    return jsonify(data)
