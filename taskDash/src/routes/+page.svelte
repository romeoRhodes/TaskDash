<script>
    import { onMount } from 'svelte';
    let tasks = [];
    let title = '';
    let token = '';
    let editingId = null;
    let showModal = false;
    let taskToDelete = null;
    let message = '';
    let messageType = '';
    let timeoutId;
  
    function showMessage(msg, type = 'success') {
      message = msg;
      messageType = type;
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => message = '', 3000);
    }
  
    async function login() {
      try {
        const res = await fetch('http://localhost:5000/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username: 'admin', password: 'password123' })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.msg);
        token = data.access_token;
        loadTasks();
      } catch (err) {
        showMessage(err.message, 'error');
      }
    }
  
    async function loadTasks() {
      try {
        const res = await fetch('http://localhost:5000/tasks', {
          headers: { Authorization: `Bearer ${token}` }
        });
        tasks = await res.json();
      } catch (err) {
        showMessage('Failed to load tasks', 'error');
      }
    }
  
    async function addOrUpdateTask() {
      try {
        const url = editingId ? `http://localhost:5000/tasks/${editingId}` : 'http://localhost:5000/tasks';
        const method = editingId ? 'PUT' : 'POST';
        const res = await fetch(url, {
          method,
          headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
          body: JSON.stringify({ title })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.msg);
        title = '';
        editingId = null;
        loadTasks();
        showMessage(data.msg);
      } catch (err) {
        showMessage(err.message, 'error');
      }
    }
  
    function editTask(task) {
      editingId = task._id;
      title = task.title;
    }
  
    function confirmDelete(task) {
      taskToDelete = task;
      showModal = true;
    }
  
    async function deleteTaskConfirmed() {
      try {
        const res = await fetch(`http://localhost:5000/tasks/${taskToDelete._id}`, {
          method: 'DELETE',
          headers: { Authorization: `Bearer ${token}` }
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.msg);
        showModal = false;
        taskToDelete = null;
        loadTasks();
        showMessage(data.msg);
      } catch (err) {
        showMessage(err.message, 'error');
      }
    }
  
    function cancelDelete() {
      showModal = false;
      taskToDelete = null;
    }
  
    onMount(login);
  </script>
  
  <main class="p-6 max-w-xl mx-auto">
    <h1 class="text-2xl font-bold mb-4">Task Dashboard</h1>
  
    {#if message}
      <div class={`mb-4 p-3 rounded ${messageType === 'success' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>{message}</div>
    {/if}
  
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
            <button on:click={() => confirmDelete(task)} class="text-sm text-red-500">Delete</button>
          </div>
        </li>
      {/each}
    </ul>
  
    {#if showModal}
      <div class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
        <div class="bg-white p-6 rounded shadow-xl w-80">
          <h2 class="text-lg font-semibold mb-4">Confirm Deletion</h2>
          <p class="mb-4">Are you sure you want to delete this task?</p>
          <div class="flex justify-end space-x-4">
            <button on:click={cancelDelete} class="px-4 py-2 bg-gray-300 rounded">Cancel</button>
            <button on:click={deleteTaskConfirmed} class="px-4 py-2 bg-red-500 text-white rounded">Delete</button>
          </div>
        </div>
      </div>
    {/if}
  </main>
  
  <style>
    main { font-family: sans-serif; }
  </style>