from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample data for the todo list
todos = [
    {'id': 1, 'task': 'Learn Flask', 'completed': False},
    {'id': 2, 'task': 'Build a Todo API', 'completed': False}
]

# Counter for generating unique IDs
todo_id_counter = 3

@app.route('/hello')
def hello():
    return "Hello, World!"

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
    global todo_id_counter
    data = request.get_json()
    if 'task' not in data:
        return jsonify({'message': 'Task is required'}), 400
    
    new_todo = {
        'id': todo_id_counter,
        'task': data['task'],
        'completed': False
    }
    todos.append(new_todo)
    todo_id_counter += 1
    return jsonify(new_todo), 201

# PUT (update) an existing todo
@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = next((todo for todo in todos if todo['id'] == todo_id), None)
    if not todo:
        return jsonify({'message': 'Todo not found'}), 404
    
    data = request.get_json()
    if 'task' in data:
        todo['task'] = data['task']
    if 'completed' in data:
        todo['completed'] = data['completed']
    return jsonify(todo)

# DELETE a todo
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todos = [todo for todo in todos if todo['id'] != todo_id]
    return jsonify({'message': 'Todo deleted'})

if __name__ == '__main__':
    app.run(debug=True)
