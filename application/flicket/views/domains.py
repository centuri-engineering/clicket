#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import flash, redirect, url_for, render_template
from flask_login import login_required
from flask_babel import gettext

from . import flicket_bp
from application import app, db
from application.flicket.forms.flicket_forms import DomainForm
from application.flicket.models.flicket_models import FlicketDomain, FlicketInstitute


# create ticket
@flicket_bp.route(
    app.config["FLICKET"] + "domains/<int:institute_id>/", methods=["GET", "POST"]
)
@login_required
def domains():
    form = DomainForm()
    domains = FlicketDomain.query.order_by(FlicketDomain.domain.asc())

    if form.validate_on_submit():
        add_domain = FlicketDomain(domain=form.domain.data)
        db.session.add(add_domain)
        db.session.commit()
        flash(gettext(f"New domain {form.domain.data} added."), category="success")
        return redirect(url_for("flicket_bp.domains"))

    title = gettext("Domains")

    return render_template(
        "flicket_domains.html", title=title, form=form, domains=domains
    )


@flicket_bp.route(
    app.config["FLICKET"] + "domain_edit/<int:domain_id>/", methods=["GET", "POST"]
)
@login_required
def domain_edit(domain_id=False):
    if domain_id:

        form = DomainForm()
        domain = FlicketDomain.query.filter_by(id=domain_id).first()

        if form.validate_on_submit():
            domain.domain = form.domain.data
            db.session.commit()
            flash(f"Domain {form.domain.data} edited.")
            return redirect(url_for("flicket_bp.domains"))

        form.domain.data = domain.domain

        title = gettext("Edit Domain")

        return render_template(
            "flicket_domain_edit.html",
            title=title,
            form=form,
            domain=domain,
            institute=domain.institute.institute,
        )

    return redirect(url_for("flicket_bp.domains"))
