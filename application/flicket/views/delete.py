#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import os

from flask import flash, g, redirect, url_for, render_template
from flask_babel import gettext
from flask_login import login_required

from application import app, db
from application.flicket.forms.forms_main import ConfirmPassword
from application.flicket.models.flicket_models import (
    FlicketTicket,
    FlicketUploads,
    FlicketPost,
    FlicketRequest,
    FlicketTeam,
    FlicketHistory,
)
from . import flicket_bp


# delete ticket
@flicket_bp.route(
    app.config["FLICKET"] + "delete_ticket/<ticket_id>/", methods=["GET", "POST"]
)
@login_required
def delete_ticket(ticket_id):

    form = ConfirmPassword()
    ticket = FlicketTicket.query.filter_by(id=ticket_id).first()

    if form.validate_on_submit():

        # delete images from database and folder
        images = FlicketUploads.query.filter_by(topic_id=ticket_id)
        for i in images:
            # delete files
            os.remove(
                os.path.join(
                    os.getcwd(), app.config["ticket_upload_folder"] + "/" + i.file_name
                )
            )
            # remove from database
            db.session.delete(i)

        # remove posts for ticket.
        for post in ticket.posts:
            # remove history
            history = FlicketHistory.query.filter_by(post=post).all()
            for h in history:
                db.session.delete(h)
            post.user.total_posts -= 1
            db.session.delete(post)

        user = ticket.user
        user.total_posts -= 1
        db.session.delete(ticket)

        # commit changes
        db.session.commit()
        flash(gettext("Ticket deleted."), category="success")
        return redirect(url_for("flicket_bp.tickets"))

    return render_template(
        "flicket_deletetopic.html", form=form, ticket=ticket, title="Delete Ticket"
    )


# delete post
@flicket_bp.route(
    app.config["FLICKET"] + "delete_post/<post_id>/", methods=["GET", "POST"]
)
@login_required
def delete_post(post_id):
    # check user is authorised to delete posts. Only admin can do this.
    if not g.user.is_admin:
        flash(gettext("You are not authorised to delete posts"), category="warning")

    form = ConfirmPassword()

    post = FlicketPost.query.filter_by(id=post_id).first()

    if form.validate_on_submit():

        # delete images from database and folder
        images = FlicketUploads.query.filter_by(posts_id=post_id)
        for i in images:
            # delete files
            os.remove(
                os.path.join(
                    os.getcwd(), app.config["ticket_upload_folder"] + "/" + i.file_name
                )
            )
            # remove from database
            db.session.delete(i)

        db.session.delete(post)
        # commit changes
        db.session.commit()
        flash(gettext("Ticket deleted."), category="success")
        return redirect(url_for("flicket_bp.tickets"))

    title = gettext("Delete Post")

    return render_template("flicket_deletepost.html", form=form, post=post, title=title)


# delete request
@flicket_bp.route(
    app.config["FLICKET"] + "delete/request/<int:request_id>/", methods=["GET", "POST"]
)
@login_required
def delete_request(request_id=False):
    if request_id:

        # check user is authorised to delete requests. Only admin or super_user can do this.
        if not any([g.user.is_admin, g.user.is_super_user]):
            flash(
                gettext("You are not authorised to delete requests."), category="warning"
            )
            return redirect("flicket_bp.requests")

        form = ConfirmPassword()

        requests = FlicketTicket.query.filter_by(request_id=request_id)
        request = FlicketRequest.query.filter_by(id=request_id).first()

        # stop the deletion of requests assigned to tickets.
        if requests.count() > 0:
            flash(
                gettext(
                    (
                        "Request is linked to posts. Request can not be deleted unless all posts / topics are removed"
                        " / relinked."
                    )
                ),
                category="danger",
            )
            return redirect(url_for("flicket_bp.requests"))

        if form.validate_on_submit():
            # delete request from database
            request = FlicketRequest.query.filter_by(id=request_id).first()

            db.session.delete(request)
            # commit changes
            db.session.commit()
            flash("Request deleted", category="success")
            return redirect(url_for("flicket_bp.requests"))

        notification = 'You are trying to delete request <span class="label label-default">{}</span> .'.format(
            request.request
        )

        title = gettext("Delete Request")

        return render_template(
            "flicket_delete.html", form=form, notification=notification, title=title
        )


# delete team
@flicket_bp.route(
    app.config["FLICKET"] + "delete/team/<int:team_id>/",
    methods=["GET", "POST"],
)
@login_required
def delete_team(team_id=False):
    if team_id:

        # check user is authorised to delete teams. Only admin or super_user can do this.
        if not any([g.user.is_admin, g.user.is_super_user]):
            flash(
                gettext("You are not authorised to delete teams."),
                category="warning",
            )
            return redirect("flicket_bp.teams")

        form = ConfirmPassword()

        #
        teams = FlicketTicket.query.filter_by(team_id=team_id)
        team = FlicketTeam.query.filter_by(id=team_id).first()

        # we can't delete any teams associated with requests.
        if teams.count() > 0:
            flash(
                gettext(
                    (
                        "Team has tickets linked to it. Team can not be deleted unless all linked tickets are "
                        "first removed."
                    )
                ),
                category="danger",
            )
            return redirect(url_for("flicket_bp.teams"))

        if form.validate_on_submit():
            # delete request from database
            team = FlicketTeam.query.filter_by(id=team_id).first()

            db.session.delete(team)
            # commit changes
            db.session.commit()
            flash(
                'Team "{}" deleted.'.format(team.team),
                category="success",
            )
            return redirect(url_for("flicket_bp.teams"))

        notification = gettext(
            'You are trying to delete team <span class="label label-default">%(value)s</span>.',
            value=team.team,
        )

        title = gettext("Delete Team")

        return render_template(
            "flicket_delete.html", form=form, notification=notification, title=title
        )
