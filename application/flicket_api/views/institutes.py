#! python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

"""
    Institutes
    ===========

    Get Institute by ID
    ~~~~~~~~~~~~~~~~~~~~

    .. http:get:: /flicket-api/institute/(int:institute_id)

        **Request**

        .. sourcecode:: http

            GET /flicket-api/institute/1 HTTP/1.1
            HOST: localhost:5000
            Accept: application/json
            Authorization: Bearer <token>

        **Response**

        .. sourcecode:: http

            HTTP/1.0 200 OK
            Content-Length: 191
            Content-Type: application/json
            Date: Sun, 30 Jun 2019 12:37:21 GMT
            Server: Werkzeug/0.14.1 Python/3.7.3

            {
                "institute": "Design",
                "id": 1,
                "links": {
                    "institutes": "http://127.0.0.1:5000/flicket-api/institutes/",
                    "self": "http://127.0.0.1:5000/flicket-api/institute/1"
                }
            }

    Get Institutes
    ~~~~~~~~~~~~~~~~

    .. http:get:: /flicket-api/institutes/

        **Request**

        .. sourcecode:: http

            GET /flicket-api/institutes/ HTTP/1.1
            HOST: localhost:5000
            Accept: application/json
            Authorization: Bearer <token>

        **Response**

        .. sourcecode:: http

            HTTP/1.0 200 OK
            Content-Length: 2307
            Content-Type: application/json
            Date: Sun, 30 Jun 2019 12:40:21 GMT
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
                    "total_items": 9,
                    "total_pages": 1
                },
                "items": [
                    {
                        "institute": "Commercial",
                        "id": 6,
                        "links": {
                            "institutes": "http://127.0.0.1:5000/flicket-api/institutes/",
                            "self": "http://127.0.0.1:5000/flicket-api/institute/6"
                        }
                    },
                    {
                        "institute": "Design",
                        "id": 1,
                        "links": {
                            "institutes": "http://127.0.0.1:5000/flicket-api/institutes/",
                            "self": "http://127.0.0.1:5000/flicket-api/institute/1"
                        }
                    },
                    {
                        "institute": "Human Resources",
                        "id": 5,
                        "links": {
                            "institutes": "http://127.0.0.1:5000/flicket-api/institutes/",
                            "self": "http://127.0.0.1:5000/flicket-api/institute/5"
                        }
                    },
                    {
                        "institute": "IT",
                        "id": 3,
                        "links": {
                            "institutes": "http://127.0.0.1:5000/flicket-api/institutes/",
                            "self": "http://127.0.0.1:5000/flicket-api/institute/3"
                        }
                    }
                ]
            }


    Create Institute
    ~~~~~~~~~~~~~~~~~

    .. http:post:: http://localhost:5000/flicket-api/institutes(str:institute)

        **Request**

        .. sourcecode:: http

            POST /flicket-api/institutes HTTP/1.1
            HOST: localhost:5000
            Accept: application/json
            Authorization: Bearer <token>

            {
                "institute": "new institute"
            }

        **Response**

        .. sourcecode: http::

            HTTP/1.0 201 CREATED
            Content-Length: 201
            Content-Type: application/json
            Date: Sun, 30 Jun 2019 12:45:35 GMT
            Location: http://localhost:5000/flicket-api/institute/12
            Server: Werkzeug/0.14.1 Python/3.7.3

            {
                "institute": "New Institute",
                "id": 12,
                "links": {
                    "institutes": "http://127.0.0.1:5000/flicket-api/institutes/",
                    "self": "http://127.0.0.1:5000/flicket-api/institute/12"
                }
            }
"""

from flask import jsonify, request, url_for

from .sphinx_helper import api_url
from . import bp_api
from application import app, db
from application.flicket.models.flicket_models import FlicketInstitute
from application.flicket_api.views.auth import token_auth
from application.flicket_api.views.errors import bad_request


@bp_api.route(api_url + "institute/<int:id>", methods=["GET"])
@token_auth.login_required
def get_institute(id):
    return jsonify(
        FlicketInstitute.query.order_by(FlicketInstitute.institute.asc())
        .get_or_404(id)
        .to_dict()
    )


@bp_api.route(api_url + "institutes/", methods=["GET"])
@token_auth.login_required
def get_institutes():
    page = request.args.get("page", 1, type=int)
    per_page = min(
        request.args.get("per_page", app.config["posts_per_page"], type=int), 100
    )
    data = FlicketInstitute.to_collection_dict(
        FlicketInstitute.query.order_by(FlicketInstitute.institute.asc()),
        page,
        per_page,
        "bp_api.get_institutes",
    )
    return jsonify(data)


@bp_api.route(api_url + "institutes", methods=["POST"])
@token_auth.login_required
def create_institute():

    # todo add authentication. only those in the admin or super_user groups should be allowed to create.

    data = request.get_json() or {}

    if "institute" not in data:
        return bad_request("Must include institute name.")

    if FlicketInstitute.query.filter_by(institute=data["institute"]).first():
        return bad_request("Institute already created.")

    institute = FlicketInstitute(data["institute"])
    db.session.add(institute)
    db.session.commit()

    response = jsonify(institute.to_dict())
    response.status_code = 201
    response.headers["Location"] = url_for("bp_api.get_institute", id=institute.id)

    return response
