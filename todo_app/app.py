
from flask import Flask, request, jsonify, render_template, redirect, url_for
from .database import get_db, init_db, close_db

app = Flask(__name__)

# DB connection is closing..
app.teardown_appcontext(close_db)

# UI Route ----------------------
@app.route('/app/tasks', methods=['GET'])
def tasks_page():
    """
    Returns JSON when client requests 'Accept: application/json'.
    Otherwise, render an HTML template (index.html) with tasks.
    """
    conn = get_db()
    tasks = [dict(t) for t in conn.execute('SELECT * FROM tasks').fetchall()]

    # tests send Accept
    if request.accept_mimetypes.best == 'application/json':
        return jsonify(tasks), 200

    return render_template('index.html', tasks=tasks), 200

# API: CRUD OPERATION
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    conn = get_db()
    rows = conn.execute('SELECT * FROM tasks').fetchall()
    return jsonify([dict(row) for row in rows]), 200


@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json(silent=True) or {}
    title = data.get('title')
    description = data.get('description', '')
    due_date = data.get('due_date')
    status = data.get('status', 'pending')

    if not title:
        return jsonify({'error': 'Title is required'}), 400

    conn = get_db()
    cur = conn.execute(
        'INSERT INTO tasks (title, description, due_date, status) VALUES (?, ?, ?, ?)',
        (title, description, due_date, status)
    )
    conn.commit()
    task_id = cur.lastrowid

    # Tests look for 'id' in the response
    return jsonify({'id': task_id, 'message': 'Task created'}), 201


@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    conn = get_db()
    row = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    if not row:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(dict(row)), 200


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json(silent=True) or {}

    # Collect only provided fields
    fields, values = [], []
    for key in ('title', 'description', 'due_date', 'status'):
        if key in data and data[key] is not None:
            fields.append(f'{key} = ?')
            values.append(data[key])

    if not fields:
        return jsonify({'error': 'No fields to update'}), 400

    values.append(task_id)

    conn = get_db()
    cur = conn.execute(f'UPDATE tasks SET {", ".join(fields)} WHERE id = ?', tuple(values))
    conn.commit()

    # If no row was updated, return 404
    if cur.rowcount == 0:
        return jsonify({'error': 'Task not found'}), 404

    return jsonify({'message': 'Task updated'}), 200


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db()
    cur = conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()

    if cur.rowcount == 0:
        return jsonify({'error': 'Task not found'}), 404

    return jsonify({'deleted': task_id}), 200

# Template routes ----------------------
@app.route('/', methods=['GET'])
def index():
    # Homepage
    conn = get_db()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    return render_template('index.html', tasks=tasks), 200


@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description', '')
        due_date = request.form.get('due_date') 
        status = request.form.get('status', 'pending')

        if not title:
            return jsonify({'error': 'Title is required'}), 400

        conn = get_db()
        conn.execute(
            'INSERT INTO tasks (title, description, due_date, status) VALUES (?, ?, ?, ?)',
            (title, description, due_date, status)
        )
        conn.commit()
        return redirect(url_for('index'))

    return render_template('add_task.html'), 200


if __name__ == "__main__":
    app.run(debug=True)

