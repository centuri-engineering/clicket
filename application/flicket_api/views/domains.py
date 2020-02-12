#! python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

"""
    Categories
    ==========

    Get Domain By ID
    ~~~~~~~~~~~~~~~~~~

    .. http:get:: /flicket-api/domain/(int:domain_id)

        **Request**

        .. sourcecode:: http

            GET /flicket-api/domain/1 HTTP/1.1
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
                "domain": "Dataset",
                "id": 1,
                "links": {
                    "domains": "http://127.0.0.1:5000/flicket-api/domains/",
                    "self": "http://127.0.0.1:5000/flicket-api/domain/1"
                }
            }

    Get Domains
    ~~~~~~~~~~~~~~

    .. http:get:: /flicket-api/domains/

        **Request**

        .. sourcecode:: http

            GET /flicket-api/domains/ HTTP/1.1
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
                    "self": "http://127.0.0.1:5000/flicket-api/domains/?page=1&per_page=50"
                },
                "_meta": {
                    "page": 1,
                    "per_page": 50,
                    "total_items": 15,
                    "total_pages": 1
                },
                "items": [
                    {
                        "domain": "Approved Suppliers",
                        "id": 14,
                        "links": {
                            "domains": "http://127.0.0.1:5000/flicket-api/domains/",
                            "self": "http://127.0.0.1:5000/flicket-api/domain/14"
                        }
                    },
                    {
                        "domain": "Dataset",
                        "id": 1,
                        "links": {
                            "domains": "http://127.0.0.1:5000/flicket-api/domains/",
                            "self": "http://127.0.0.1:5000/flicket-api/domain/1"
                        }
                    },
                    {
                        "domain": "ECR",
                        "id": 3,
                        "links": {
                            "domains": "http://127.0.0.1:5000/flicket-api/domains/",
                            "self": "http://127.0.0.1:5000/flicket-api/domain/3"
                        }
                    },
                    {
                        "domain": "Holidays",
                        "id": 12,
                        "links": {
                            "domains": "http://127.0.0.1:5000/flicket-api/domains/",
                            "self": "http://127.0.0.1:5000/flicket-api/domain/12"
                        }
                    }
                ]
            }

"""

from flask import jsonify, request, url_for

from .sphinx_helper import api_url
from . import bp_api
from application import app, db
from application.flicket.models.flicket_models import FlicketDomain
from application.flicket_api.views.auth import token_auth
from application.flicket_api.views.errors import bad_request


@bp_api.route(api_url + "domain/<int:id>", methods=["GET"])
@token_auth.login_required
def get_domain(id):
    return jsonify(FlicketDomain.query.get_or_404(id).to_dict())


@bp_api.route(api_url + "domains/", methods=["GET"])
@token_auth.login_required
def get_domains():
    domains = FlicketDomain.query.order_by(FlicketDomain.domain.asc())
    page = request.args.get("page", 1, type=int)
    per_page = min(
        request.args.get("per_page", app.config["posts_per_page"], type=int), 100
    )
    data = FlicketDomain.to_collection_dict(
        domains, page, per_page, "bp_api.get_domains"
    )
    return jsonify(data)


@bp_api.route(api_url + "domains", methods=["POST"])
@token_auth.login_required
def create_domain():
    data = request.get_json() or {}

    if "domain" not in data:
        return bad_request("Must include domain name")

    if FlicketDomain.query.filter_by(domain=data["domain"]).first():
        return bad_request("Domain  already exists.")

    domain = FlicketDomain(data["domain"])
    db.session.add(domain)
    db.session.commit()

    response = jsonify(domain.to_dict())
    response.status_code = 201
    response.headers["Location"] = url_for("bp_api.get_domain", id=domain.id)
    return response
