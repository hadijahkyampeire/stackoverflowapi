import os
from flask import jsonify
from api import app
from api.database import Database

db = Database()

config_name = os.getenv('APP_SETTINGS')


@app.errorhandler(405)
def url_not_found(error):
    return jsonify({'message':'Requested method not allowed'}), 405

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'message':'page not found, check the url'}), 404

@app.errorhandler(500)
def internal_error(error):
    return "500 error"


if __name__ == '__main__':
    db.create_tables()
    app.run()