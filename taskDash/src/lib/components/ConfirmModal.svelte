<script>
    import { createEventDispatcher } from 'svelte';
    const dispatch = createEventDispatcher();
  </script>
  
  <div class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
    <div class="bg-white p-6 rounded shadow-xl w-80">
      <h2 class="text-lg font-semibold mb-4">Confirm Deletion</h2>
      <p class="mb-4">Are you sure you want to delete this task?</p>
      <div class="flex justify-end space-x-4">
        <button on:click={() => dispatch('cancel')} class="px-4 py-2 bg-gray-300 rounded">Cancel</button>
        <button on:click={() => dispatch('confirm')} class="px-4 py-2 bg-red-500 text-white rounded">Delete</button>
      </div>
    </div>
  </div>