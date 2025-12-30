document.addEventListener('DOMContentLoaded', function() {
    loadTasks();

    //Handle add task form
    const addForm = document.getElementById('add-task-form');
    console.log('Before addForm checked......');
    if (addForm){
        console.log('After addForm checked......');
        addForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const data = {
                title: document.getElementById('title').value,
                description: document.getElementById('description').value,
                due_date: document.getElementById('due_date').value,
                status: document.getElementById('status').value
            };
            fetch('/api/tasks', {
                method: 'POST',
                headers: {'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            }).then(() => {
                window.location.href = '/'; // Redirect to dashboard
            });
        });
    }
});

function loadTasks() {
    console.log("loadTasks() function loaded from app.js file ...");
    fetch('/api/tasks')
        .then(response => response.json())
        .then(tasks => {
            const container = document.getElementById('tasks-container');
            container.innerHTML = '';
            tasks.forEach(task => {
                const card = createTaskCard(task);
                container.appendChild(card);
            });
        });
}


function createTaskCard(task) {
    const card = document.createElement('div');
    card.innerHTML = `
        <div class="card-body">
            <h5 class="card-title task-title ${task.status === 'completed' ? 'completed' : ''}">${task.title}</h5>
            <p class="card-text">${task.description || 'No description'}</p>
            <p class="card-text><small class="text-muted">Due: ${task.due_date || 'N/A'} | Status: ${task.status}</small></p>
            <button class="btn btn-success btn-custom" onclick="toggleStatus(${task.id}, '${task.status}')">${task.status === 'completed' ? 'Mark Pending' : 'Mark Complete'}</button>
            <button class="btn btn-primary btn-sm  btn-custom" onclick="editTask(${task.id})">Edit</button>
            <button class="btn btn-danger btn-sm btn-custom" onclick="deleteTask(${task.id})">Delete</button>
        </div>
    `;

    return card;
}

function toggleStatus(id, currentStatus) {
    const newStatus = currentStatus === 'completed' ? 'pending' : 'completed';
    fetch(`/api/tasks/${id}`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({status: newStatus})
    }).then(() => loadTasks());
}


function editTask(id) {
    // Simple prompt for edit (can be replaced with a model)
    const newTitle = prompt('Edit title: ');
    const description = prompt('Edit Description: ')
    const newDateValue = prompt("Choose Date: ", Date()); // 'YYYY-MM-DD' or null
    const status = prompt('Edit Status: ')

     fetch(`/api/tasks/${id}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                title: newTitle,
                description: description,
                due_date: newDateValue,
                status: status
            })
        }).then(() => loadTasks());
}

function deleteTask(id) {
    if (confirm('Delete this task?')) {
        fetch(`/api/tasks/${id}`, {
            method: 'DELETE'
        }).then(() => loadTasks());
    }
}