#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import abort, redirect, url_for, flash, render_template, g
from flask_babel import gettext
from flask_login import login_required

from application import app, db
from application.flicket.forms.flicket_forms import TeamForm
from application.flicket.models.flicket_models import FlicketTicket
from application.flicket.models.flicket_models import FlicketTeam
from application.flicket.scripts.flicket_functions import add_action
from . import flicket_bp


# tickets main
@flicket_bp.route(
    app.config["FLICKET"] + "ticket_team/<int:ticket_id>/",
    methods=["GET", "POST"],
)
@login_required
def ticket_team(ticket_id=False):
    if not app.config["change_team"]:
        abort(404)

    if app.config["change_team_only_admin_or_super_user"]:
        if not g.user.is_admin and not g.user.is_super_user:
            abort(404)

    form = TeamForm()
    ticket = FlicketTicket.query.get_or_404(ticket_id)

    if ticket.current_status.status == "Closed":
        flash(gettext("Can't change the team on a closed ticket."))
        return redirect(url_for("flicket_bp.ticket_view", ticket_id=ticket_id))

    if form.validate_on_submit():
        team = FlicketTeam.query.filter_by(
            team=form.team.data
        ).one()

        if ticket.team_id == team.team_id:
            flash(
                gettext(
                    f"Team {ticket.team.team} is already assigned to ticket."
                ),
                category="warning",
            )
            return redirect(url_for("flicket_bp.ticket_view", ticket_id=ticket.id))

        # change team
        ticket.team_id = team.team_id

        # add action record
        add_action(
            ticket,
            "team",
            data={
                "team": team.team,
                "team_id": team.team_id,
            },
        )

        db.session.commit()

        flash(
            gettext(f"You changed team of ticket: {ticket_id}"), category="success"
        )
        return redirect(url_for("flicket_bp.ticket_view", ticket_id=ticket.id))

    title = gettext("Change Team of Ticket")

    return render_template(
        "flicket_team.html", title=title, form=form, ticket=ticket
    )
