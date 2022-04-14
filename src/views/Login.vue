<script setup>
import { LoginIcon, UserAddIcon, UserGroupIcon } from '@heroicons/vue/outline'
import { ArrowCircleRightIcon } from '@heroicons/vue/solid'
import { HS256, sha256, short, salt } from '../utils/crypto.js'
import { useRouter } from 'vue-router'

const router = useRouter()

</script>

<template>
  <div class="h-screen bg-gradient-to-b from-blue-100 to-purple-100 flex justify-center items-center">
    <div class="w-full max-w-sm" >
      <form class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <h1 class="text-3xl font-medium grid grid-cols-1 place-items-center"> Login </h1>
        <div class="mb-6 mt-10">
          <label class="block text-md font-bold mb-2" for="username"> Username: </label>
          <input class="shadow appearance-none border rounded w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline" id="username" type="text" placeholder="Username">
        </div>
        <div class="mb-6">
          <label class="block text-md font-bold mb-2" for="password"> Password: </label>
          <input class="shadow appearance-none border rounded w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline" id="password" type="password" placeholder="************">
        </div>
        <button class="bg-blue-500 hover:bg-blue-300 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mt-5 ml-12"> Sign In </button>
        <button class="bg-blue-500 hover:bg-blue-300 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mt-5 ml-12" @click="router.push('/')"> Return</button>
     </form>
    </div>
     <img style="transition: all 0.5s ease;" src="../../public/login.svg" class="ml-20 absolue w-1/3">
  </div>

</template>


<style scoped>
button.card {
  @apply flex items-center rounded py-2 px-4 shadow-md bg-white hover:shadow-lg m-2 transition-all
}
</style>