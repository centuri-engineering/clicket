#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import flash, redirect, url_for, render_template
from flask_babel import gettext
from flask_login import login_required

from . import flicket_bp
from application import app, db
from application.flicket.forms.flicket_forms import InstituteForm
from application.flicket.models.flicket_models import FlicketInstitute


# create ticket
@flicket_bp.route(app.config["FLICKET"] + "institutes/", methods=["GET", "POST"])
@flicket_bp.route(
    app.config["FLICKET"] + "institutes/<int:page>/", methods=["GET", "POST"]
)
@login_required
def institutes(page=1):
    form = InstituteForm()

    query = FlicketInstitute.query.order_by(FlicketInstitute.institute.asc())

    if form.validate_on_submit():
        add_institute = FlicketInstitute(institute=form.institute.data)
        db.session.add(add_institute)
        db.session.commit()
        flash(
            gettext(f'New institute "{form.institute.data}" added.'),
            category="success",
        )
        return redirect(url_for("flicket_bp.institutes"))

    _institutes = query.paginate(page, app.config["posts_per_page"])

    title = gettext("Institutes")

    return render_template(
        "flicket_institutes.html",
        title=title,
        form=form,
        page=page,
        institutes=_institutes,
    )


@flicket_bp.route(
    app.config["FLICKET"] + "institute_edit/<int:institute_id>/",
    methods=["GET", "POST"],
)
@login_required
def institute_edit(institute_id=False):
    if institute_id:

        form = InstituteForm()
        query = FlicketInstitute.query.filter_by(id=institute_id).first()

        if form.validate_on_submit():
            query.institute = form.institute.data
            db.session.commit()
            flash(gettext('Institute "%(value)s" edited.', value=form.institute.data))
            return redirect(url_for("flicket_bp.institutes"))

        form.institute.data = query.institute

        return render_template(
            "flicket_institute_edit.html",
            title="Edit Institute",
            form=form,
            institute=query,
        )

    return redirect(url_for("flicket_bp.institutes"))
