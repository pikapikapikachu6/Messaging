<script setup>
import { LoginIcon, UserAddIcon, UserGroupIcon } from '@heroicons/vue/outline'

import axios from 'axios'

import { useRouter } from 'vue-router'

const router = useRouter()

import state from '../state.js'
if (typeof(state.user.name) != "undefined") {
  router.push("/friend")
}

</script>

<template>

  <div class="h-screen bg-gradient-to-b from-blue-100 to-purple-100">
    <h1 class="text-5xl font-medium grid grid-cols-1 place-items-center h-72"> Messaging tool </h1>

    <div class="ml-96 mr-96 font-medium grid grid-cols-3 place-items-center">
      <button class="card" @click="router.push('/register')"><user-add-icon class="w-6 text-red-500 mr-2"/> Register</button>
      <button class="card" @click="router.push('/login')"><login-icon class="w-6 text-purple-500 mr-2"/> Login</button>
      <button class="card" @click="router.push('/admin/sas')"><user-group-icon class="w-6 text-orange-500 mr-2"/>About</button>
    </div>
    <img style="transition: all 0.5s ease;" src="chat.svg" class="absolute w-1/3 group-hover:left-0 left-1/3">
 </div>

</template>


<style scoped>
button.card {
  @apply flex items-center rounded py-2 px-4 shadow-md bg-white hover:shadow-lg m-2 transition-all
}
</style>