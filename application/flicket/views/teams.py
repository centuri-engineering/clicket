#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import flash, redirect, url_for, render_template
from flask_babel import gettext
from flask_login import login_required

from . import flicket_bp
from application import app, db
from application.flicket.forms.flicket_forms import TeamForm
from application.flicket.models.flicket_models import FlicketTeam


# create ticket
@flicket_bp.route(app.config["FLICKET"] + "teams/", methods=["GET", "POST"])
@flicket_bp.route(
    app.config["FLICKET"] + "teams/<int:page>/", methods=["GET", "POST"]
)
@login_required
def teams(page=1):
    form = TeamForm()

    query = FlicketTeam.query.order_by(FlicketTeam.team.asc())

    if form.validate_on_submit():
        add_team = FlicketTeam(team=form.team.data)
        db.session.add(add_team)
        db.session.commit()
        flash(
            gettext(f'New team "{form.team.data}" added.'),
            category="success",
        )
        return redirect(url_for("flicket_bp.teams"))

    _teams = query.paginate(page, app.config["posts_per_page"])

    title = gettext("Teams")

    return render_template(
        "flicket_teams.html",
        title=title,
        form=form,
        page=page,
        teams=_teams,
    )


@flicket_bp.route(
    app.config["FLICKET"] + "team_edit/<int:team_id>/",
    methods=["GET", "POST"],
)
@login_required
def team_edit(team_id=False):
    if team_id:

        form = TeamForm()
        query = FlicketTeam.query.filter_by(id=team_id).first()

        if form.validate_on_submit():
            query.team = form.team.data
            db.session.commit()
            flash(gettext('Team "%(value)s" edited.', value=form.team.data))
            return redirect(url_for("flicket_bp.teams"))

        form.team.data = query.team

        return render_template(
            "flicket_team_edit.html",
            title="Edit Team",
            form=form,
            team=query,
        )

    return redirect(url_for("flicket_bp.teams"))
