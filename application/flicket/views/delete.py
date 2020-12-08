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
    FlicketDomain,
    FlicketInstitute,
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


# delete domain
@flicket_bp.route(
    app.config["FLICKET"] + "delete/domain/<int:domain_id>/", methods=["GET", "POST"]
)
@login_required
def delete_domain(domain_id=False):
    if domain_id:

        # check user is authorised to delete domains. Only admin or super_user can do this.
        if not any([g.user.is_admin, g.user.is_super_user]):
            flash(
                gettext("You are not authorised to delete domains."), category="warning"
            )
            return redirect("flicket_bp.domains")

        form = ConfirmPassword()

        domains = FlicketTicket.query.filter_by(domain_id=domain_id)
        domain = FlicketDomain.query.filter_by(id=domain_id).first()

        # stop the deletion of domains assigned to tickets.
        if domains.count() > 0:
            flash(
                gettext(
                    (
                        "Domain is linked to posts. Domain can not be deleted unless all posts / topics are removed"
                        " / relinked."
                    )
                ),
                category="danger",
            )
            return redirect(url_for("flicket_bp.domains"))

        if form.validate_on_submit():
            # delete domain from database
            domain = FlicketDomain.query.filter_by(id=domain_id).first()

            db.session.delete(domain)
            # commit changes
            db.session.commit()
            flash("Domain deleted", category="success")
            return redirect(url_for("flicket_bp.domains"))

        notification = 'You are trying to delete domain <span class="label label-default">{}</span> .'.format(
            domain.domain
        )

        title = gettext("Delete Domain")

        return render_template(
            "flicket_delete.html", form=form, notification=notification, title=title
        )


# delete institute
@flicket_bp.route(
    app.config["FLICKET"] + "delete/institute/<int:institute_id>/",
    methods=["GET", "POST"],
)
@login_required
def delete_institute(institute_id=False):
    if institute_id:

        # check user is authorised to delete institutes. Only admin or super_user can do this.
        if not any([g.user.is_admin, g.user.is_super_user]):
            flash(
                gettext("You are not authorised to delete institutes."),
                category="warning",
            )
            return redirect("flicket_bp.institutes")

        form = ConfirmPassword()

        #
        institutes = FlicketTicket.query.filter_by(institute_id=institute_id)
        institute = FlicketInstitute.query.filter_by(id=institute_id).first()

        # we can't delete any institutes associated with domains.
        if institutes.count() > 0:
            flash(
                gettext(
                    (
                        "Institute has tickets linked to it. Institute can not be deleted unless all linked tickets are "
                        "first removed."
                    )
                ),
                category="danger",
            )
            return redirect(url_for("flicket_bp.institutes"))

        if form.validate_on_submit():
            # delete domain from database
            institute = FlicketInstitute.query.filter_by(id=institute_id).first()

            db.session.delete(institute)
            # commit changes
            db.session.commit()
            flash(
                'Institute "{}" deleted.'.format(institute.institute),
                category="success",
            )
            return redirect(url_for("flicket_bp.institutes"))

        notification = gettext(
            'You are trying to delete institute <span class="label label-default">%(value)s</span>.',
            value=institute.institute,
        )

        title = gettext("Delete Institute")

        return render_template(
            "flicket_delete.html", form=form, notification=notification, title=title
        )
