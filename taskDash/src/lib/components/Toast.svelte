<script>
    export let message = '';
    export let messageType = 'success';
  </script>
  
  {#if message}
    <div class="mb-4 p-3 rounded transition-opacity duration-300"
         class:bg-green-100={messageType === 'success'}
         class:text-green-700={messageType === 'success'}
         class:bg-red-100={messageType === 'error'}
         class:text-red-700={messageType === 'error'}>
      {message}
    </div>
  {/if}
  