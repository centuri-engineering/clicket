#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField

from .flicket_forms import does_user_exist
from application.flicket.models.flicket_models import FlicketInstitute
from application.flicket.models.flicket_models import FlicketDomain
from application.flicket.models.flicket_models import FlicketStatus


class SearchTicketForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        form = super(SearchTicketForm, self).__init__(*args, **kwargs)

        # choices are populated via ajax query on page load. This are simply empty lists so
        # form can be loaded on page view
        self.institute.choices = [
            (d.id, d.institute)
            for d in FlicketInstitute.query.order_by(
                FlicketInstitute.institute.asc()
            ).all()
        ]
        self.institute.choices.insert(0, (0, "institute"))

        self.domain.choices = [
            (c.id, c.domain)
            for c in FlicketDomain.query.order_by(
                FlicketDomain.domain.asc()
            ).all()
        ]
        self.domain.choices.insert(0, (0, "domain"))

        self.status.choices = [(s.id, s.status) for s in FlicketStatus.query.all()]
        self.status.choices.insert(0, (0, "status"))

    """ Search form. """
    institute = SelectField(lazy_gettext("institute"), coerce=int, validators=[])
    domain = SelectField(lazy_gettext("domain"), coerce=int)
    status = SelectField(lazy_gettext("status"), coerce=int)
    username = StringField(lazy_gettext("username"), validators=[does_user_exist])
    content = StringField(lazy_gettext("content"), validators=[])

    def __repr__(self):
        return "<SearchTicketForm>"
