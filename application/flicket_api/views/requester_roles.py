#! python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

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
