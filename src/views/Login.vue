<script setup>
import { LoginIcon, UserAddIcon, UserGroupIcon } from '@heroicons/vue/outline'
import { ArrowCircleRightIcon, ArrowCircleLeftIcon } from '@heroicons/vue/solid'
import { HS256, sha256, short, salt } from '../utils/crypto.js'
import axios from 'axios'

import { useRouter } from 'vue-router'

const router = useRouter()

let input = $ref('')
let random = $ref('')

// let inputElement = $ref()
// watchEffect(() => {ß
//   if (inputElement) inputElement.focus()
// })

async function next() {
  console.log('input'+ input)
  console.log(random);
  if (!input) return
  if (!random) {
    random = '12345'
    console.log('random' + random);
    user.name = short(await sha256(input))
    // random = await axios.get('./test.json').then(res => {console.log(res)})
    console.log(user.name)
  } else {
    return
  }
  input = ''
}


</script>

<template>
  <div class="h-screen bg-gradient-to-b from-blue-100 to-purple-100 flex justify-center items-center">
    <div class="w-full max-w-sm" >
      <form class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <h1 class="text-3xl font-medium grid grid-cols-1 place-items-center"> Login </h1>
        <div class="mb-6 mt-10">
          <!-- <label class="block text-md font-bold mb-2" for="username"> Username: </label> -->
          <!-- <input class="shadow appearance-none border rounded w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline" id="username" placeholder="Username" v-model="input"> -->
          <input class="w-2/3 mt-6 mb-4 rounded px-3 py-2 radius-2 border-2 border-gray-300 focus:ring-1 focus:border-blue-300 transition"
            :placeholder="random ? '请输入密码' : '请输入用户名'"
            :type="random ? 'password' : 'text'"
            v-model="input" @keyup.enter="next"
          >
        </div>
        <button @click="next" name="next" class="mt-5 ml-20"><arrow-circle-right-icon class="w-12 h-12 transition" :class="input ? 'text-blue-500' : 'text-gray-300'"/></button>
        <button @click="router.push('/')" name="return" class="mt-5 ml-16"><arrow-circle-left-icon class="w-12 h-12 transition text-blue-500"/></button>
      </form>
    </div>
    <img style="transition: all 0.5s ease;" src="login.svg" class="ml-20 absolue w-1/3">
  </div>

</template>


<style scoped>
button.card {
  @apply flex items-center rounded py-2 px-4 shadow-md bg-white hover:shadow-lg m-2 transition-all
}
</style>