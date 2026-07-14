from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Connect to SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    result = [{"id": s.id, "name": s.name} for s in students]
    return jsonify(result), 200


@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    new_student = Student(name=data['name'])
    db.session.add(new_student)
    db.session.commit()
    return jsonify({"message": "Student created!", "id": new_student.id}), 201

if __name__ == '__main__':
    app.run(debug=True)
