#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import flash, redirect, url_for, request, session, render_template, g
from flask_babel import gettext
from flask_login import login_required

from . import flicket_bp
from application import app
from application.flicket.forms.flicket_forms import CreateTicketForm
from application.flicket.models.flicket_models_ext import FlicketTicketExt


# create ticket
@flicket_bp.route(app.config["FLICKET"] + "ticket_create/", methods=["GET", "POST"])
@login_required
def ticket_create():
    # default request_type based on last submit (get from session)
    # using session, as information about last created ticket can be sensitive
    # in future it can be stored in extended user model instead
    last_request_type = session.get("ticket_create_last_request_type")
    form = CreateTicketForm(request_type=last_request_type)

    if form.validate_on_submit():
        new_ticket = FlicketTicketExt.create_ticket(
            title=form.title.data,
            user=g.user,
            content=form.content.data,
            requester=form.requester.data,
            referee=form.referee.data,
            instrument=form.instrument.data,
            request_stage=1,
            request_type=form.request_type.data,
            team=form.team.data,
            days=form.days.data,
            files=request.files.getlist("file"),
        )

        flash(gettext("New Ticket created."), category="success")

        session["ticket_create_last_request_type"] = form.request_type.data

        return redirect(url_for("flicket_bp.ticket_view", ticket_id=new_ticket.id))

    title = gettext("Create Ticket")
    return render_template("flicket_create.html", title=title, form=form)
