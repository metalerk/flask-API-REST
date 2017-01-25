from flask import Flask
from flask import g
from flask import jsonify
from flask import abort

from models import initialize
from models import Course
from models import DATABASE

app = Flask(__name__)
PORT = 8080
DEBUG = True
API_BASE = '/api/v1/'
@app.errorhandler(404):
def not_found(error):
    return jsonify(generate_response(404, error='Curso no encontrado'))

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
    return jsonify(generate_response(404, error="Curso no encontrado"))

@app.route(API_BASE + 'courses', methods=['GET'])
def get_courses():
    courses = Course.select()
    courses = [course.to_json() for course in courses]
    return jsonify(generate_response(data=courses))

@app.route(API_BASE + 'courses/<int:course_id>', methods=['GET'])
def try_course(course_id):
    course = try_course(course_id)
    return jsonify(generate_response(data=course.to_json()))

def get_course(course_id):
    try:
        return Course.get(Course.id == course_id)
    except CourseDoesNotExist as e:
        abort(404)

def generate_response(status=200, data=None, error=None):
    return {
        'status' : status,
        'data' : data,
        'error' : error
    }


if __name__ == '__main__':
    initialize()
    app.run(port=PORT, debug=DEBUG)
