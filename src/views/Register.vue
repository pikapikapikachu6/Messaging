<script setup>
import { LoginIcon, UserAddIcon, UserGroupIcon } from '@heroicons/vue/outline'
import { ArrowCircleRightIcon } from '@heroicons/vue/solid'
import { sha256, short, salt } from '../utils/crypto.js'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Cookies from 'js-cookie'

const router = useRouter()
let username = $ref('')
let pwd = $ref('')
let checkPwd = $ref('')
let mes = $ref('')
let pk = $ref('')
let key = $ref('')

async function sendRegister() {
  axios.post('/api/register', {
    'username': username,
    'password': short(await sha256(pwd + salt))
  })
  .then(resp => {
    // console.log(resp)
    mes = resp.data['result']
    if (mes === 'success') {
      pk = resp.data['public_key']
      key = 'pk_' + username
      Cookies.remove(key);
      Cookies.set(key, pk, {expires: 1});
      // console.log("This is register")
      // console.log(Cookies.get('pk_'))
      router.push('/login')
    } else {
      Swal.fire('Error', 'username has exists', 'error')
    }
  })
  .catch(function (error) {
    Swal.fire('Error', 'register failed', 'error')
    // console.log(error)
  })
}

</script>

<template>
  <div class="h-screen bg-gradient-to-b from-blue-100 to-purple-100 flex justify-center items-center">
    <img style="transition: all 0.5s ease;" src="register.svg" class="mr-20 absolue w-1/3">
    <div class="w-full max-w-sm" >
      <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <h1 class="text-3xl font-medium grid grid-cols-1 place-items-center"> Register </h1>
        <div class="mb-6 mt-10">
          <label class="block text-md font-bold mb-2" for="username"> Username: </label>
          <input class="shadow appearance-none border rounded w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline" id="username" type="text" placeholder="Username" v-model="username">
        </div>
        <div class="mb-6">
          <label class="block text-md font-bold mb-2" for="password"> Password: </label>
          <input class="shadow appearance-none border rounded w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline" id="password" type="password" placeholder="************" v-model="pwd">
        </div>
        <div class="mb-6">
          <label class="block text-md font-bold mb-2" for="password"> Retype Password: </label>
          <input class="shadow appearance-none border rounded w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline" id="re-password" type="password" placeholder="************" v-model="checkPwd">
        </div>
        <button class="text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mt-5 ml-12" :class="(pwd === checkPwd && pwd != '') ? 'bg-blue-500 hover:bg-blue-300' : 'bg-gray-300'" @click="sendRegister"> Register </button>
        <button class="bg-blue-500 hover:bg-blue-300 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mt-5 ml-12" @click="router.push('/')"> Return</button>
     </div>
    </div>
  </div>

</template>


<style scoped>
button.card {
  @apply flex items-center rounded py-2 px-4 shadow-md bg-white hover:shadow-lg m-2 transition-all
}
</style>