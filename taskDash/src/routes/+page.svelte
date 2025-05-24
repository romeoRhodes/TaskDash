<script>
    import { onMount } from 'svelte';
    let tasks = [];
    let title = '';
    let token = '';
    let editingId = null;
  
    async function login() {
      const res = await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: 'admin', password: 'password123' })
      });
      const data = await res.json();
      token = data.access_token;
      loadTasks();
    }
  
    async function loadTasks() {
      const res = await fetch('http://localhost:5000/tasks', {
        headers: { Authorization: `Bearer ${token}` }
      });
      tasks = await res.json();
    }
  
    async function addOrUpdateTask() {
      if (editingId) {
        await fetch(`http://localhost:5000/tasks/${editingId}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
          body: JSON.stringify({ title })
        });
        editingId = null;
      } else {
        await fetch('http://localhost:5000/tasks', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
          body: JSON.stringify({ title })
        });
      }
      title = '';
      loadTasks();
    }
  
    function editTask(task) {
      editingId = task._id;
      title = task.title;
    }
  
    async function deleteTask(id) {
      await fetch(`http://localhost:5000/tasks/${id}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` }
      });
      loadTasks();
    }
  
    onMount(login);
  </script>
  
  <main class="p-6 max-w-xl mx-auto">
    <h1 class="text-2xl font-bold mb-4">Task Dashboard</h1>
    <div class="mb-4">
      <input bind:value={title} placeholder="New Task" class="border p-2 mr-2 rounded" />
      <button on:click={addOrUpdateTask} class="bg-blue-500 text-white px-4 py-2 rounded">
        {editingId ? 'Update' : 'Add'}
      </button>
    </div>
    <ul>
      {#each tasks as task}
        <li class="border-b py-2 flex justify-between items-center">
          <span>{task.title}</span>
          <div class="space-x-2">
            <button on:click={() => editTask(task)} class="text-sm text-yellow-500">Edit</button>
            <button on:click={() => deleteTask(task._id)} class="text-sm text-red-500">Delete</button>
          </div>
        </li>
      {/each}
    </ul>
  </main>
  
  <style>
    main { font-family: sans-serif; }
  </style>