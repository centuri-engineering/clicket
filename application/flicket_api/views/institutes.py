#! python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

"""
    Teams
    ===========

    Get Team by ID
    ~~~~~~~~~~~~~~~~~~~~

    .. http:get:: /flicket-api/team/(int:team_id)

        **Request**

        .. sourcecode:: http

            GET /flicket-api/team/1 HTTP/1.1
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
                "team": "Design",
                "id": 1,
                "links": {
                    "teams": "http://127.0.0.1:5000/flicket-api/teams/",
                    "self": "http://127.0.0.1:5000/flicket-api/team/1"
                }
            }

    Get Teams
    ~~~~~~~~~~~~~~~~

    .. http:get:: /flicket-api/teams/

        **Request**

        .. sourcecode:: http

            GET /flicket-api/teams/ HTTP/1.1
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
                    "self": "http://127.0.0.1:5000/flicket-api/teams/?page=1&per_page=50"
                },
                "_meta": {
                    "page": 1,
                    "per_page": 50,
                    "total_items": 9,
                    "total_pages": 1
                },
                "items": [
                    {
                        "team": "Commercial",
                        "id": 6,
                        "links": {
                            "teams": "http://127.0.0.1:5000/flicket-api/teams/",
                            "self": "http://127.0.0.1:5000/flicket-api/team/6"
                        }
                    },
                    {
                        "team": "Design",
                        "id": 1,
                        "links": {
                            "teams": "http://127.0.0.1:5000/flicket-api/teams/",
                            "self": "http://127.0.0.1:5000/flicket-api/team/1"
                        }
                    },
                    {
                        "team": "Human Resources",
                        "id": 5,
                        "links": {
                            "teams": "http://127.0.0.1:5000/flicket-api/teams/",
                            "self": "http://127.0.0.1:5000/flicket-api/team/5"
                        }
                    },
                    {
                        "team": "IT",
                        "id": 3,
                        "links": {
                            "teams": "http://127.0.0.1:5000/flicket-api/teams/",
                            "self": "http://127.0.0.1:5000/flicket-api/team/3"
                        }
                    }
                ]
            }


    Create Team
    ~~~~~~~~~~~~~~~~~

    .. http:post:: http://localhost:5000/flicket-api/teams(str:team)

        **Request**

        .. sourcecode:: http

            POST /flicket-api/teams HTTP/1.1
            HOST: localhost:5000
            Accept: application/json
            Authorization: Bearer <token>

            {
                "team": "new team"
            }

        **Response**

        .. sourcecode: http::

            HTTP/1.0 201 CREATED
            Content-Length: 201
            Content-Type: application/json
            Date: Sun, 30 Jun 2019 12:45:35 GMT
            Location: http://localhost:5000/flicket-api/team/12
            Server: Werkzeug/0.14.1 Python/3.7.3

            {
                "team": "New Team",
                "id": 12,
                "links": {
                    "teams": "http://127.0.0.1:5000/flicket-api/teams/",
                    "self": "http://127.0.0.1:5000/flicket-api/team/12"
                }
            }
"""

from flask import jsonify, request, url_for

from .sphinx_helper import api_url
from . import bp_api
from application import app, db
from application.flicket.models.flicket_models import FlicketTeam
from application.flicket_api.views.auth import token_auth
from application.flicket_api.views.errors import bad_request


@bp_api.route(api_url + "team/<int:id>", methods=["GET"])
@token_auth.login_required
def get_team(id):
    return jsonify(
        FlicketTeam.query.order_by(FlicketTeam.team.asc())
        .get_or_404(id)
        .to_dict()
    )


@bp_api.route(api_url + "teams/", methods=["GET"])
@token_auth.login_required
def get_teams():
    page = request.args.get("page", 1, type=int)
    per_page = min(
        request.args.get("per_page", app.config["posts_per_page"], type=int), 100
    )
    data = FlicketTeam.to_collection_dict(
        FlicketTeam.query.order_by(FlicketTeam.team.asc()),
        page,
        per_page,
        "bp_api.get_teams",
    )
    return jsonify(data)


@bp_api.route(api_url + "teams", methods=["POST"])
@token_auth.login_required
def create_team():

    # todo add authentication. only those in the admin or super_user groups should be allowed to create.

    data = request.get_json() or {}

    if "team" not in data:
        return bad_request("Must include team name.")

    if FlicketTeam.query.filter_by(team=data["team"]).first():
        return bad_request("Team already created.")

    team = FlicketTeam(data["team"])
    db.session.add(team)
    db.session.commit()

    response = jsonify(team.to_dict())
    response.status_code = 201
    response.headers["Location"] = url_for("bp_api.get_team", id=team.id)

    return response
