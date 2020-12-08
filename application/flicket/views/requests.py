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
from application.flicket.models.flicket_models import FlicketRequest, FlicketTeam


# create ticket
@flicket_bp.route(
    app.config["FLICKET"] + "requests/<int:team_id>/", methods=["GET", "POST"]
)
@login_required
def requests():
    form = RequestForm()
    requests = FlicketRequest.query.order_by(FlicketRequest.request.asc())

    if form.validate_on_submit():
        add_request = FlicketRequest(request=form.request.data)
        db.session.add(add_request)
        db.session.commit()
        flash(gettext(f"New request {form.request.data} added."), category="success")
        return redirect(url_for("flicket_bp.requests"))

    title = gettext("Requests")

    return render_template(
        "flicket_requests.html", title=title, form=form, requests=requests
    )


@flicket_bp.route(
    app.config["FLICKET"] + "request_edit/<int:request_id>/", methods=["GET", "POST"]
)
@login_required
def request_edit(request_id=False):
    if request_id:

        form = RequestForm()
        request = FlicketRequest.query.filter_by(id=request_id).first()

        if form.validate_on_submit():
            request.request = form.request.data
            db.session.commit()
            flash(f"Request {form.request.data} edited.")
            return redirect(url_for("flicket_bp.requests"))

        form.request.data = request.request

        title = gettext("Edit Request")

        return render_template(
            "flicket_request_edit.html",
            title=title,
            form=form,
            request=request,
            team=request.team.team,
        )

    return redirect(url_for("flicket_bp.requests"))
