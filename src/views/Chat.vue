<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

import { ChevronDoubleUpIcon } from '@heroicons/vue/outline'
import {sha256, short, salt, RSA_encryption, RSA_decryption} from '../utils/crypto.js'
import axios from 'axios'
import state from '../state.js'
import {onMounted, onUnmounted} from "vue";
// import {init} from "@vitejs/plugin-vue";
if (typeof(state.user.name) == "undefined") {
  router.push("/login")
}
let user = state.user
let friend = user.friend
let current = $ref('')
let cipher = $ref('')
let friendPK = user.friendPK
let receiveMess = $ref([])
let sendMess = $ref([])


async function postMessDB() {
  axios.post('/api/post_mess_DB', {
    'sender': user.name,
    'receiver': user.friend,
    'message': cipher
  })
      .then(resp => {
        console.log('resp result: ' + resp.data)
      })
      .catch(function (error) {
        Swal.fire('Error', 'He is not login', 'error')
        console.log(error)
      })
}

async function getAllMess() {
  receiveMess = []
  axios.post('/api/get_all_message', {
    'sender': user.friend,
    'receiver': user.name
  })
  .then(resp => {
    let result = resp.data
    for (let i = 0; i < result.length; i++) {
      console.log("receive message" + result[i])
      console.log("sk:" + user.sk)
      let sk = user.sk
      let decrypt = RSA_decryption(sk, result[i])
      console.log("decrypt result" + decrypt)
      receiveMess.push(decrypt)
    }
  })
  .catch(function (error) {
    Swal.fire('Error', 'Get message error', 'error')
    console.log(error)
  })
}

async function sendMessFunc() {
  console.log('friend here: ' + friendPK)
  console.log('current: '+ current)
  console.log('friend: ' + friend)
  current = user.name + ':' + current
  cipher = RSA_encryption(friendPK, current)
  console.log('cipher: ' + cipher)
  await postMessDB()
  sendMess.push(current)
  current = ''
  await getAllMess()
}


</script>

<template>
  <div className="flex flex-col h-screen bg-gradient-to-b from-blue-100 to-purple-100">
    <h1 className="text-4xl font-medium grid grid-cols-1 place-items-center h-32 text-rose-700"> chat with {{
        friend }} </h1>
    <button class="fixed top-10 left-5 w-20 rounded py-2 px-4 shadow-md bg-red-300 hover:shadow-lg m-2 transition-all"
            @click="router.push('/friend')"> return </button>
    <div class="bg-lime-100 flex-grow mx-24 overflow-auto">
      <p v-for="x in sendMess">{{ x }}</p>
      <p v-for="y in receiveMess">{{ y }}</p>
    </div>
    <div class="relative mx-24 flex flex-wrap items-stretch h-16 mt-10 mb-10">
      <input type="text"
             class="relative py-1 px-2 pr-10 w-full bg-white rounded shadow outline-none text-sm text-gray-700
             placeholder-gray-400 focus:outline-none focus:shadow-outline" placeholder="Enter the message" v-model="current"/>
      <button
          class="absolute right-0 z-10 py-1 pr-2 w-8 h-full leading-snug bg-transparent rounded text-base font-normal
          text-gray-400 text-center flex items-center justify-center" @click="sendMessFunc">
        <chevron-double-up-icon class="fa fa-user"></chevron-double-up-icon>
      </button>
    </div>
  </div>
</template>
