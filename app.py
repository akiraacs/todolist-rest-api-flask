from flask import Flask, request
from dados import tasks

app = Flask(__name__)

max_id_value = max([task["id"] for task in tasks]) + 1

@app.get('/tasks')
def get_all_tasks():
    return {'tasks': tasks}, 200


@app.get('/tasks/<int:task_id>')
def get_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            return {'task': task}, 200
    return {'message': 'Task not found'}, 404


@app.post('/tasks')
def create_task():
    data: dict = request.json
    title = data.get('title')
    description = data.get('description')
    status = data.get('status', 'Pendente')

    if not title:
        return {'message': 'Title is required'}, 400

    for task in tasks:
        if task['title'] == title:
            return {'message': f"Task '{title}' already exists"}, 409

    new_task = {'id': max_id_value, 'title': title, 'description': description, 'status': status}
    tasks.append(new_task)
    return {'message': 'Task created successfully', 'task': new_task}, 201


@app.put('/tasks/<int:task_id>')
def update_task(task_id):
    data: dict = request.json
    title = data.get('title')
    description = data.get('description')
    status = data.get('status', 'Pendente')

    task = [task for task in tasks if task_id == task.get('id')]
    if not task:
        return {'message': 'Task not found'}, 404

    task = task[0]
    if title:
        task['title'] = title
    if description:
        task['description'] = description
    if status:
        task['status'] = status

    return {'message': 'Task update successfully', 'task': task}


@app.delete('/tasks/<int:task_id>')
def delete_task(task_id):
    task = [task for task in tasks if task_id == task.get('id')]
    if not task:
        return {'message': 'Task not found'}, 404

    task = task[0]
    tasks.remove(task)
    return {'message': 'Task deleted successfully'}


if __name__ == '__main__':
    from db import db
    db.init_app()
    app.run(debug=True)