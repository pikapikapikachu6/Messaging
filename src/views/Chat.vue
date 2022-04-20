<script setup>
import { ChevronDoubleUpIcon } from '@heroicons/vue/outline'
import { useRouter } from 'vue-router'
const router = useRouter()

import {sha256, short, salt, RSA_encryption} from '../utils/crypto.js'

import axios from 'axios'
import state from '../state.js'
if (typeof(state.user.name) == "undefined") {
  router.push("/login")
}
let user = state.user
let friend = user.friend
let current = $ref('')
let cipher = $ref('')
let friendPK = user.friendPK


async function sendMess() {
  console.log('friend here: ' + friendPK)
  console.log('current: '+ current)
  console.log('friend: ' + friend)
  cipher = RSA_encryption(friendPK, current)
  console.log('cipher: ' + cipher)
}


</script>

<template>
  {{ cipher }}
  <div className="flex flex-col h-screen bg-gradient-to-b from-blue-100 to-purple-100">
    <h1 className="text-4xl font-medium grid grid-cols-1 place-items-center h-32 text-rose-700"> chat with {{
        friend }} </h1>
    <button class="fixed top-10 left-5 w-20 rounded py-2 px-4 shadow-md bg-red-300 hover:shadow-lg m-2 transition-all"
            @click="router.push('/friend')">
      return
    </button>
    <div class="bg-lime-100 flex-grow mx-24">

    </div>
    <div class="relative mx-24 flex flex-wrap items-stretch h-16 mt-10 mb-10">
      <input type="text"
             class="relative py-1 px-2 pr-10 w-full bg-white rounded shadow outline-none text-sm text-gray-700
             placeholder-gray-400 focus:outline-none focus:shadow-outline" placeholder="Enter the message" v-model="current"/>
      <button
          class="absolute right-0 z-10 py-1 pr-2 w-8 h-full leading-snug bg-transparent rounded text-base font-normal
          text-gray-400 text-center flex items-center justify-center" @click="sendMess()">
        <chevron-double-up-icon class="fa fa-user"></chevron-double-up-icon>
      </button>
    </div>
  </div>
</template>
