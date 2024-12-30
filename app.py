from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 데이터베이스 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask_user:password@localhost/flask_todo_db'
app.config['SQLALCHEMY_TRACKMODIFICATIONS'] = False

# SQLAlchemy 객체 생성
db = SQLAlchemy(app)

"""
    db.Model : SQLAlchemy의 모델 클래스를 상속받아 데이터베이스 테이블을 정의함.
    id : 정수형 기본 키(primary key)로, 자동으로 증가함.
    title : 최대 100자의 문자열로, null 값을 허용하지 않음(nullable = False).
    description : 최대 200자의 문자열로, null 값을 허용함.
    completed : 불리언 값으로, 기본값을 False임.
    created_at : DateTime 타입으로, 기본값은 현재 시간. db.func.current_timestamp() 는 데이터베이스의 현재 시간 함수를 사용함.
    __repr__ : 객체의 문자열 표현을 정의. 디버깅에 유용함.
"""
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self): 
        return f'<Todo {self.title}>'

# Create
@app.route('/todo', methods = ['POST'])
def add_todo():
    title = request.form['title']
    description = request.form['description']
    
    new_todo = Todo(
        title = title,
        description = description
    )

    db.session.add(new_todo)
    db.session.commit()

    return redirect(url_for('index'))

# Read
@app.route('/')
def index():
    page = request.args.get('page', 1, type = int)
    per_page = request.args.get('per_page', 5, type=int)
    search_query = request.args.get('search', '')

    if search_query:
        todos = Todo.query.filter(Todo.title.contains(search_query)).paginate(page=page, per_page=per_page, error_out=False)
    else:
        todos = Todo.query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('index.html', todos = todos)

# Update
@app.route('/update_todo/<int:todo_id>', methods=['POST'])
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.title = request.form['title']
    todo.description = request.form['description']

    db.session.commit()
    page = request.args.get('page', 1, type=int)

    return redirect(url_for('index', page=page))

# Delete
@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()

    page = request.args.get('page', 1, type=int)
    return redirect(url_for('index', page = page))


@app.route('/complete/<int:todo_id>', methods = ['POST'])
def complete(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.completed = not todo.completed
    db.session.commit()
    page = request.args.get('page', 1, type = int)
    return redirect(url_for('index', page=page))

@app.route('/edit_todo/<int:todo_id>', methods=['GET'])
def edit_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id) 
    page = request.args.get('page', 1, type=int)
    return render_template('edit_todo.html', todo=todo, page=page)


# 데이터베이스 테이블 생성 
# 기존에 없는 테이블만 생성, 이미 존재하는 테이블의 구조를 변경하지 않음.
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

