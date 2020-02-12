#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import abort, redirect, url_for, flash, render_template, g
from flask_babel import gettext
from flask_login import login_required

from application import app, db
from application.flicket.forms.flicket_forms import DomainForm
from application.flicket.models.flicket_models import FlicketTicket
from application.flicket.models.flicket_models import FlicketDomain
from application.flicket.scripts.flicket_functions import add_action
from . import flicket_bp


# tickets main
@flicket_bp.route(
    app.config["FLICKET"] + "ticket_domain/<int:ticket_id>/", methods=["GET", "POST"],
)
@login_required
def ticket_domain(ticket_id=False):
    if not app.config["change_domain"]:
        abort(404)

    if app.config["change_domain_only_admin_or_super_user"]:
        if not g.user.is_admin and not g.user.is_super_user:
            abort(404)

    form = DomainForm()
    ticket = FlicketTicket.query.get_or_404(ticket_id)

    if ticket.current_status.status in ("Finished", "Canceled"):
        flash(gettext("Can't change the domain on a closed ticket."))
        return redirect(url_for("flicket_bp.ticket_view", ticket_id=ticket_id))

    if form.validate_on_submit():
        domain = FlicketDomain.query.filter_by(domain=form.domain.data).one()

        if ticket.domain_id == domain.domain_id:
            flash(
                gettext(
                    f"Domain {ticket.domain.domain} is already assigned to ticket."
                ),
                category="warning",
            )
            return redirect(url_for("flicket_bp.ticket_view", ticket_id=ticket.id))

        # change domain
        ticket.domain_id = domain.domain_id

        # add action record
        add_action(
            ticket,
            "domain",
            data={"domain": domain.domain, "domain_id": domain.domain_id,},
        )

        db.session.commit()

        flash(gettext(f"You changed domain of ticket: {ticket_id}"), category="success")
        return redirect(url_for("flicket_bp.ticket_view", ticket_id=ticket.id))

    title = gettext("Change Domain of Ticket")

    return render_template("flicket_domain.html", title=title, form=form, ticket=ticket)
