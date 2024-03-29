#! python3
# -*- coding: utf-8 -*-


from application import db, app
from application.flicket.models.flicket_user import FlicketUser
from application.flicket.scripts.flicket_user_details import FlicketUserDetails


@app.cli.command("total_user_posts")
def total_user_posts():

    """
    Command used by manage.py to update the users total post count. Use when upgrading from 0.1.4.
    """
    print("!!! Warning !!!!")
    print("This script should not be run whilst the server is running.")
    print("Calculated totals could change.")
    input("Enter to continue.")
    users = FlicketUser.query.all()
    all_good = True
    for user in users:
        user_details_total = FlicketUserDetails(user).num_posts
        if user_details_total != user.total_posts:
            print(
                "{} had a calculated post count of {} and a table count of {}. This will be updated.".format(
                    user.username, user_details_total, user.total_posts
                )
            )
            user.total_posts = user_details_total
            db.session.commit()
            all_good = False
    if all_good:
        print("No updates were required.")
    else:
        print("Updates were made.")


@app.cli.command("total_user_assigned")
def total_user_assigned():
    """
    Command used by manage.py to update the users total post count. Use if upgrading to 0.1.7.
    """
    print("!!! Warning !!!!")
    print("This script should not be run whilst the server is running.")
    print("Calculated totals could change.")
    input("Enter to continue.")
    users = FlicketUser.query.all()
    all_good = True
    for user in users:
        user_details_total = FlicketUserDetails(user).num_assigned
        if user_details_total != user.total_assigned:
            print(
                "{} had a calculated assigned count of {} and a table count of {}. This will be updated.".format(
                    user.username, user_details_total, user.total_posts
                )
            )
            user.total_assigned = user_details_total
            db.session.commit()
            all_good = False
    if all_good:
        print("No updates were required.")
    else:
        print("Updates were made.")
