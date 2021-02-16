#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import abort, redirect, url_for, flash, render_template, g
from flask_babel import gettext
from flask_login import login_required

from application import app, db
from application.flicket.forms.flicket_forms import RequestForm
from application.flicket.models.flicket_models import FlicketTicket
from application.flicket.models.flicket_models import FlicketRequestType
from application.flicket.scripts.flicket_functions import add_action
from . import flicket_bp


# tickets main
@flicket_bp.route(
    app.config["FLICKET"] + "ticket_request_type/<int:ticket_id>/",
    methods=["GET", "POST"],
)
@login_required
def ticket_request_type(ticket_id=False):
    if not app.config["change_request_type"]:
        abort(404)

    if app.config["change_request_type_only_admin_or_super_user"]:
        if not g.user.is_admin and not g.user.is_super_user:
            abort(404)

    form = RequestForm()
    ticket = FlicketTicket.query.get_or_404(ticket_id)

    if ticket.current_status.status == "Closed":
        flash(gettext("Can't change the request_type on a closed ticket."))
        return redirect(url_for("flicket_bp.ticket_view", ticket_id=ticket_id))

    if form.validate_on_submit():
        request_type = FlicketRequestType.query.filter_by(
            request_type=form.request_type.data
        ).one()

        if ticket.request_type_id == request_type.request_type_id:
            flash(
                gettext(
                    f"Request {ticket.request_type.request_type} is already assigned to ticket."
                ),
                category="warning",
            )
            return redirect(url_for("flicket_bp.ticket_view", ticket_id=ticket.id))

        # change request
        ticket.request_type_id = request_type.request_type_id

        # add action record
        add_action(
            ticket,
            "request_type",
            data={
                "request_type": request_type.request_type,
                "request_type_id": request_type.request_type_id,
            },
        )

        db.session.commit()

        flash(
            gettext(f"You changed request of ticket: {ticket_id}"), category="success"
        )
        return redirect(url_for("flicket_bp.ticket_view", ticket_id=ticket.id))

    title = gettext("Change RequestType of Ticket")

    return render_template(
        "flicket_request_type.html", title=title, form=form, ticket=ticket
    )
