#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import time
from application import app

from application.flicket.models.flicket_models import FlicketTicket
from application.flicket.models.flicket_user import FlicketUser
from application.flicket.scripts.email import FlicketMail


@app.cli.command("email_outstanding_tickets")
def run(self):
    # find all users
    users = FlicketUser.query.all()
    for user in users:
        # that have created a ticket or have a ticket assigned to them.
        tickets = (
            FlicketTicket.query.filter(FlicketTicket.user == user)
            .filter(FlicketTicket.assigned == user)
            .filter(FlicketTicket.status_id != 2)
        )

        if tickets.count() > 0:
            mail = FlicketMail()
            mail.tickets_not_closed(user, tickets)
            time.sleep(10)
