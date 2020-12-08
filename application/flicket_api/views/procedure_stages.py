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

            GET /flicket-api/procedure_stage/1 HTTP/1.1
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
                    "self": "http://127.0.0.1:5000/flicket-api/procedure_stage/1",
                    "procedure_stages": "http://127.0.0.1:5000/flicket-api/procedure_stages/"
                },
                "procedure_stage": "Open"
            }


    Get ProcedureStages
    ~~~~~~~~~~~~

    .. http:get:: /flicket-api/procedure_stages/

        **Request**

        .. sourcecode:: http

            GET /flicket-api/procedure_stages/ HTTP/1.1
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
                    "self": "http://127.0.0.1:5000/flicket-api/teams/?page=1&per_page=50"
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
                            "self": "http://127.0.0.1:5000/flicket-api/procedure_stage/1",
                            "procedure_stages": "http://127.0.0.1:5000/flicket-api/procedure_stages/"
                        },
                        "procedure_stage": "Open"
                    },
                    {
                        "id": 2,
                        "links": {
                            "self": "http://127.0.0.1:5000/flicket-api/procedure_stage/2",
                            "procedure_stages": "http://127.0.0.1:5000/flicket-api/procedure_stages/"
                        },
                        "procedure_stage": "Closed"
                    },
                    {
                        "id": 3,
                        "links": {
                            "self": "http://127.0.0.1:5000/flicket-api/procedure_stage/3",
                            "procedure_stages": "http://127.0.0.1:5000/flicket-api/procedure_stages/"
                        },
                        "procedure_stage": "In Work"
                    },
                    {
                        "id": 4,
                        "links": {
                            "self": "http://127.0.0.1:5000/flicket-api/procedure_stage/4",
                            "procedure_stages": "http://127.0.0.1:5000/flicket-api/procedure_stages/"
                        },
                        "procedure_stage": "Awaiting Information"
                    }
                ]
            }

"""

from flask import jsonify, request

from .sphinx_helper import api_url
from . import bp_api
from application import app
from application.flicket.models.flicket_models import FlicketProcedureStage
from application.flicket_api.views.auth import token_auth


@bp_api.route(api_url + "procedure_stage/<int:id>", methods=["GET"])
@token_auth.login_required
def get_procedure_stage(id):
    return jsonify(FlicketProcedureStage.query.get_or_404(id).to_dict())


@bp_api.route(api_url + "procedure_stages/", methods=["GET"])
@token_auth.login_required
def get_procedure_stages():
    page = request.args.get("page", 1, type=int)
    per_page = min(
        request.args.get("per_page", app.config["posts_per_page"], type=int), 100
    )
    data = FlicketProcedureStage.to_collection_dict(
        FlicketProcedureStage.query, page, per_page, "bp_api.get_procedure_stages"
    )

    return jsonify(data)
