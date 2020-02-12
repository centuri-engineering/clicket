#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import abort, redirect, url_for, flash, render_template, g
from flask_babel import gettext
from flask_login import login_required

from application import app, db
from application.flicket.forms.flicket_forms import InstituteForm
from application.flicket.models.flicket_models import FlicketTicket
from application.flicket.models.flicket_models import FlicketInstitute
from application.flicket.scripts.flicket_functions import add_action
from . import flicket_bp


# tickets main
@flicket_bp.route(
    app.config["FLICKET"] + "ticket_institute/<int:ticket_id>/",
    methods=["GET", "POST"],
)
@login_required
def ticket_institute(ticket_id=False):
    if not app.config["change_institute"]:
        abort(404)

    if app.config["change_institute_only_admin_or_super_user"]:
        if not g.user.is_admin and not g.user.is_super_user:
            abort(404)

    form = InstituteForm()
    ticket = FlicketTicket.query.get_or_404(ticket_id)

    if ticket.current_status.status in ("Finished", "Canceled"):
        flash(gettext("Can't change the institute on a closed ticket."))
        return redirect(url_for("flicket_bp.ticket_view", ticket_id=ticket_id))

    if form.validate_on_submit():
        institute = FlicketInstitute.query.filter_by(
            institute=form.institute.data
        ).one()

        if ticket.institute_id == institute.institute_id:
            flash(
                gettext(
                    f"Institute {ticket.institute.institute} is already assigned to ticket."
                ),
                category="warning",
            )
            return redirect(url_for("flicket_bp.ticket_view", ticket_id=ticket.id))

        # change institute
        ticket.institute_id = institute.institute_id

        # add action record
        add_action(
            ticket,
            "institute",
            data={
                "institute": institute.institute,
                "institute_id": institute.institute_id,
            },
        )

        db.session.commit()

        flash(
            gettext(f"You changed institute of ticket: {ticket_id}"), category="success"
        )
        return redirect(url_for("flicket_bp.ticket_view", ticket_id=ticket.id))

    title = gettext("Change Institute of Ticket")

    return render_template(
        "flicket_institute.html", title=title, form=form, ticket=ticket
    )
