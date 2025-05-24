<script>
    import { onMount } from 'svelte';
    import ConfirmModal from '$lib/components/ConfirmModal.svelte';
    import Toast from '$lib/components/Toast.svelte';
  
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
      if (!title.trim()) {
        showMessage('Task title cannot be empty', 'error');
        return;
      }
  
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
  
    <Toast {message} {messageType} />
  
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
      <ConfirmModal on:cancel={cancelDelete} on:confirm={deleteTaskConfirmed} />
    {/if}
  </main>
  
  <style>
    main { font-family: sans-serif; }
  </style>
  