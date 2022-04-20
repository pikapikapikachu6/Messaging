<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
</script>

<template>
  <div class="h-screen bg-gradient-to-b from-blue-100 to-purple-100">
    <button class="fixed top-10 left-5 w-20 rounded py-2 px-4 shadow-md bg-red-300 hover:shadow-lg m-2 transition-all"
            @click="router.push('/home')"> return </button>
    <div class="text-1xl font-small grid grid-cols-1 place-items-center h-48">
      <p class="mt-10"> Front-end developer: Lavender Li </p>
      <p> Back-end developer: Lavender Li and Yuexiao Zou </p>
      <a href="https://github.com/pikapikapikachu6/Messaging">Github website:
        https://github.com/pikapikapikachu6/Messaging </a>
    </div>
  </div>
</template>

<style scoped>
</style>