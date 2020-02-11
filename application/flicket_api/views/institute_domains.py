#! python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

"""
    Institute / Domain
    =====================

    Get Institute / Domain By Domain ID
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. http:get:: /flicket-api/institute_domain/(int:domain_id)

    Get Institute / Categories
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. http:get:: /flicket-api/institute_domains/
"""

from flask import jsonify, request

from .sphinx_helper import api_url
from . import bp_api
from application import app
from application.flicket.models.flicket_models import FlicketInstituteDomain
from application.flicket_api.views.auth import token_auth


@bp_api.route(api_url + "institute_domain/<int:id>", methods=["GET"])
@token_auth.login_required
def get_institute_domain(id):
    return jsonify(FlicketInstituteDomain.query.get_or_404(id).to_dict())


@bp_api.route(api_url + "institute_domains/", methods=["GET"])
@token_auth.login_required
def get_institute_domains():
    institute_domain = request.args.get("institute_domain")
    institute_id = request.args.get("institute_id")
    institute = request.args.get("institute")
    institute_domains = FlicketInstituteDomain.query.order_by(
        FlicketInstituteDomain.institute_domain
    )
    kwargs = {}
    if institute_domain:
        institute_domains = institute_domains.filter(
            FlicketInstituteDomain.institute_domain.ilike(
                f"%{institute_domain}%"
            )
        )
        kwargs["institute_domain"] = institute_domain
    if institute_id:
        institute_domains = institute_domains.filter_by(
            institute_id=institute_id
        )
        kwargs["institute_id"] = institute_id
    if institute:
        institute_domains = institute_domains.filter(
            FlicketInstituteDomain.institute.ilike(f"%{institute}")
        )
        kwargs["institute"] = institute
    page = request.args.get("page", 1, type=int)
    per_page = min(
        request.args.get("per_page", app.config["posts_per_page"], type=int), 100
    )
    data = FlicketInstituteDomain.to_collection_dict(
        institute_domains,
        page,
        per_page,
        "bp_api.get_institute_domains",
        **kwargs,
    )
    return jsonify(data)
