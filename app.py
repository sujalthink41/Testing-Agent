from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample data for the todo list
todos = [
    {'id': 1, 'task': 'Learn Flask', 'completed': False},
    {'id': 2, 'task': 'Build a Todo API', 'completed': False}
]

# Hello endpoint
@app.route('/hello')
def hello():
    return 'Hello, World!'

# GET all todos
@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

# GET a specific todo by ID
@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = next((todo for todo in todos if todo['id'] == todo_id), None)
    if todo:
        return jsonify(todo)
    return jsonify({'message': 'Todo not found'}), 404

# POST a new todo
@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    new_todo = {
        'id': len(todos) + 1,
        'task': data['task'],
        'completed': False
    }
    todos.append(new_todo)
    return jsonify(new_todo), 201

# PUT (update) an existing todo
@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = next((todo for todo in todos if todo['id'] == todo_id), None)
    if todo:
        data = request.get_json()
        todo['task'] = data.get('task', todo['task'])
        todo['completed'] = data.get('completed', todo['completed'])
        return jsonify(todo)
    return jsonify({'message': 'Todo not found'}), 404

# DELETE a todo
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todos = [todo for todo in todos if todo['id'] != todo_id]
    return jsonify({'message': 'Todo deleted'})

if __name__ == '__main__':
    app.run(debug=True)
