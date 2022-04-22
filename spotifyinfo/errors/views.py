from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(401)
def error_401(_):
    return render_template("401.html"), 401

@errors.app_errorhandler(403)
def error_404(_):
    return render_template("403.html"), 403

@errors.app_errorhandler(404)
def error_404(_):
    return render_template("404.html"), 404

@errors.app_errorhandler(405)
def error_405(_):
    return render_template("405.html"), 405

@errors.app_errorhandler(500)
def error_500(_):
    return render_template("500.html"), 500