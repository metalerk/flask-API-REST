from flask import Flask
from flask import g
from flask import jsonify

from models import initialize
from models import Course
from models import DATABASE

app = Flask(__name__)
PORT = 8080
DEBUG = True
API_BASE = '/api/v1/'

@app.before_request
def before_request():
    g.db = DATABASE
    g.db.connect()

@app.after_request
def after_request(request):
    g.db.close()
    return request

@app.errorhandler(404)
def not_found(error):
    return "Not Found"

@app.route(API_BASE + 'courses', methods=['GET'])
def get_courses():
    courses = Course.select()
    courses = [course.to_json() for course in courses]
    return jsonify(generate_response(data=courses))

@app.route(API_BASE + 'courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    course = Course.get(Course.id == course_id)
    return jsonify(generate_response(data=course.to_json()))

def generate_response(status=200, data=None, error=None):
    return {
        'status' : status,
        'data' : data,
        'error' : error
    }


if __name__ == '__main__':
    initialize()
    app.run(port=PORT, debug=DEBUG)
