#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import flash, redirect, url_for, render_template
from flask_login import login_required
from flask_babel import gettext

from . import flicket_bp
from application import app, db
from application.flicket.forms.flicket_forms import RequestForm
from application.flicket.models.flicket_models import FlicketRequestType, FlicketTeam


# create ticket
@flicket_bp.route(
    app.config["FLICKET"] + "request_types/<int:team_id>/", methods=["GET", "POST"]
)
@login_required
def request_types():
    form = RequestForm()
    request_types = FlicketRequestType.query.order_by(
        FlicketRequestType.request_type.asc()
    )

    if form.validate_on_submit():
        add_request_type = FlicketRequestType(request_type=form.request_type.data)
        db.session.add(add_request_type)
        db.session.commit()
        flash(
            gettext(f"New request_type {form.request_type.data} added."),
            category="success",
        )
        return redirect(url_for("flicket_bp.request_types"))

    title = gettext("Requests")

    return render_template(
        "flicket_request_types.html",
        title=title,
        form=form,
        request_types=request_types,
    )


@flicket_bp.route(
    app.config["FLICKET"] + "request_type_edit/<int:request_type_id>/",
    methods=["GET", "POST"],
)
@login_required
def request_type_edit(request_type_id=False):
    if request_type_id:

        form = RequestForm()
        request_type = FlicketRequestType.query.filter_by(id=request_type_id).first()

        if form.validate_on_submit():
            request_type.request_type = form.request_type.data
            db.session.commit()
            flash(f"Request {form.request_type.data} edited.")
            return redirect(url_for("flicket_bp.request_types"))

        form.request_type.data = request_type.request_type

        title = gettext("Edit Request")

        return render_template(
            "flicket_request_type_edit.html",
            title=title,
            form=form,
            request_type=request_type,
            team=request_type.team.team,
        )

    return redirect(url_for("flicket_bp.request_types"))
