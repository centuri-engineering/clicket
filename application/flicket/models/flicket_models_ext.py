#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import datetime
import os

from application import app, db
from application.flicket.scripts.flicket_upload import UploadAttachment
from application.flicket.models.flicket_models import (
    FlicketTicket,
    FlicketStatus,
    FlicketInstrument,
    FlicketRequestStage,
    FlicketRequest,
    FlicketTeam,
    FlicketSubscription,
    FlicketHistory,
    FlicketUploads,
)


class FlicketTicketExt:
    """
    A class to extend the functionality of FlicketTicket.

    Methods aren't included in the FlicketTicket class itself
    due to potential circular import issues with flicket_upload.py
    """

    @staticmethod
    def create_ticket(
        title=None,
        user=None,
        content=None,
        requester=None,
        referee=None,
        instrument=None,
        request_stage=None,
        request=None,
        team=None,
        files=None,
        days=0,
    ):
        """
        :param title:
        :param user:
        :param content:
        :param requester:
        :param instrument:
        :param request:
        :param files:
        :param days:
        :return:
        """

        ticket_status = FlicketStatus.query.filter_by(status="Open").first()
        ticket_team = FlicketTeam.query.filter_by(id=int(team)).first()
        ticket_request = FlicketRequest.query.filter_by(id=int(request)).first()
        instrument = FlicketInstrument.query.filter_by(id=int(instrument)).first()

        request_stage = FlicketRequestStage.query.filter_by(request_stage="New").first()

        upload_attachments = UploadAttachment(files)
        if upload_attachments.are_attachments():
            upload_attachments.upload_files()

        # submit ticket data to database
        new_ticket = FlicketTicket(
            title=title,
            date_added=datetime.datetime.now(),
            user=user,
            current_status=ticket_status,
            content=content,
            team=ticket_team,
            requester=requester,
            referee=referee,
            instrument=instrument,
            request_stage=request_stage,
            request=ticket_request,
            days=days,
        )

        db.session.add(new_ticket)
        # add attachments to the database
        upload_attachments.populate_db(new_ticket)
        # subscribe user to ticket.
        subscribe = FlicketSubscription(user=user, ticket=new_ticket)
        db.session.add(subscribe)

        # add count of 1 to users total posts.
        user.total_posts += 1

        db.session.commit()

        return new_ticket

    @staticmethod
    def edit_ticket(
        ticket=None,
        title=None,
        user=None,
        content=None,
        requester=None,
        referee=None,
        instrument=None,
        request_stage=None,
        request=None,
        team=None,
        files=None,
        form_uploads=None,
        days=None,
    ):
        """

        :param ticket:
        :param title:
        :param user:
        :param content:
        :param request:
        :param files:
        :param form_uploads:
        :param days:
        :return:
        """
        # before we make any changes store the original post content in the history table if it has changed.
        if ticket.modified_id:
            history_id = ticket.modified_id
        else:
            history_id = ticket.started_id

        if ticket.content != content:
            history = FlicketHistory(
                original_content=ticket.content,
                topic=ticket,
                date_modified=datetime.datetime.now(),
                user_id=history_id,
            )
            db.session.add(history)

        # loop through the selected uploads for deletion.
        if len(form_uploads) > 0:
            for i in form_uploads:
                # get the upload document information from the database.
                query = FlicketUploads.query.filter_by(id=i).first()
                # define the full uploaded filename
                the_file = os.path.join(
                    app.config["ticket_upload_folder"], query.filename
                )

                if os.path.isfile(the_file):
                    # delete the file from the folder
                    os.remove(the_file)

                db.session.delete(query)

        instrument = FlicketInstrument.query.filter_by(id=int(instrument)).first()
        request_stage = FlicketRequestStage.query.filter_by(
            id=int(request_stage)
        ).first()

        ticket_request = FlicketRequest.query.filter_by(id=int(request)).first()
        ticket_team = FlicketTeam.query.filter_by(id=int(team)).first()

        ticket.content = content
        ticket.requester = requester
        ticket.referee = referee
        ticket.title = title
        ticket.modified = user
        ticket.date_modified = datetime.datetime.now()
        ticket.instrument = instrument
        ticket.request_stage = request_stage
        ticket.request = ticket_request
        ticket.team = ticket_team
        ticket.days = days
        # set status to Open
        ticket_status = FlicketStatus.query.filter_by(status="Open").first()
        ticket.current_status = ticket_status
        files = files
        upload_attachments = UploadAttachment(files)
        if upload_attachments.are_attachments():
            upload_attachments.upload_files()

        # add files to database.
        upload_attachments.populate_db(ticket)

        db.session.commit()

        return ticket.id
