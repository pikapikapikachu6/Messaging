<script setup>
import { LoginIcon, UserAddIcon, UserGroupIcon } from '@heroicons/vue/outline'
import { ArrowCircleRightIcon, ArrowCircleLeftIcon } from '@heroicons/vue/solid'
import {sha256, short, salt, RSA_encryption} from '../utils/crypto.js'

import axios from 'axios'

import { useRouter } from 'vue-router'
const router = useRouter()

import {watchEffect} from "vue";
let inputElement = $ref()
watchEffect(() => {
  if (inputElement) inputElement.focus()
})

import Cookies from 'js-cookie'
import state from '../state.js'
const user = state.user
if (state.user.name) router.push("/home")
console.log(state.user)


let input = $ref('')
let random = $ref('')

let username = $ref('')
let pwd = $ref('')
let mes = $ref('')

let privateKey = $ref('')
let publicKey = $ref('')

let checkResult = $ref('')

let pk = $ref('')
let sk = $ref('')
let key = $ref('')


function success (username) {
  if (username == 'admin') user.admin = 1
  else user.admin = 0
  user.name = username
  user.pk = publicKey
  user.sk = privateKey
  console.log('privateKey:' + privateKey)
  console.log('publicKey:' + publicKey )
  console.log('pk:' + user.pk)
  console.log('sk:' + user.sk )
  console.log(state.user)
  router.push('/homePage')
}

async function generateRSAKeys () {
  function RSA2text (buffer) {
    const bytes = new Uint8Array(buffer), L = bytes.byteLength
    let bin = ''
    for (let i = 0; i < L; i++) bin += String.fromCharCode(bytes[i])
    return window.btoa(bin).replace(/[^\x00-\xff]/g, '$&\x01').replace(/.{64}\x01?/g, '$&\n')
  }
  try {
    const S = window.crypto.subtle
    const k = await S.generateKey({
      name: 'RSA-OAEP',
      modulusLength: 2048,
      publicExponent: new Uint8Array([0x01, 0x00, 0x01]),
      hash: { name: 'SHA-256' }
    }, true, ['encrypt', 'decrypt'])
    const sk = RSA2text(await S.exportKey('pkcs8', k.privateKey))
    const pk = RSA2text(await S.exportKey('spki', k.publicKey))
    return [pk, sk]
  } catch (e) {
    console.error(e)
    return null
  }
}

async function getKeys() {
  let keys = await generateRSAKeys()
  privateKey = keys[1]
  publicKey = keys[0]
}


async function pass() {
  if (!input) return
  if (!random) { // first
    key = 'pk_' + input
    pk = Cookies.get(key)
    const msg = "I am client";
    const cipher = RSA_encryption(pk, msg);
    if (cipher == "False" && input != 'admin') {
      Swal.fire('Error', 'CA error', 'error')
    }

    axios.post('/api/login-first', {
      'username': input,
      'cipher':cipher
    })
    .then(function (response) {
      checkResult = response.data['result']
      if (checkResult == "Is not a Certificate Authority"){
        Swal.fire('Error', 'CA error', 'error')
      }
      if (checkResult == true) {
        username = response.data['username']
      } else {
        username = 'there is error'
      }
      random = response.data['random']
    })
    .catch(function (error) {
      console.log(error);
    });

  } else { //second
    if (username == 'admin' && input == 'admin') success(username)
    else {
      console.log('second time here:')
      if (username != 'there is error') {
        await getKeys()
        axios.post('/api/login-second', {
          'username': username,
          'password':  await sha256(short(await sha256(input + salt)) + random),
          'public_key': publicKey
        })
        .then(function (response) {
          mes = response.data
          console.log(mes)
          if (mes == true) {
            success(username)
          } else {
            Swal.fire('Error', 'username / password error', 'error')
          }
        })
        .catch(function (error) {
          console.log(error);
        });
      } else {
        Swal.fire('Error', 'username / password error', 'error')
      }
    }
    random = ''
  }
  input = ''
}

</script>

<template>

  <div class="h-screen bg-gradient-to-b from-blue-100 to-purple-100 flex justify-center items-center">
    <div class="w-full max-w-md" >
      <div class="bg-white shadow-md rounded px-8 pt-10 pb-10 mb-4">
        <h1 class="text-3xl font-medium grid grid-cols-1 place-items-center"> Login </h1>
        <div class="mb-6 mt-10">
          <input ref="inputElement" class="w-2/3 ml-14 mt-4 mb-4 rounded px-3 py-2 radius-2 border-2 border-gray-300 focus:ring-1 focus:border-blue-300 transition"
            :placeholder="random ? 'Please input the password' : 'Please input the username'"
            :type="random ? 'password' : 'text'"
            v-model="input" @keyup.enter="pass"
          >
        </div>
        <button @click="pass" class="mt-5 ml-28"><arrow-circle-right-icon class="w-12 h-12 transition" :class="input ? 'text-blue-500' : 'text-gray-300'"/></button>
        <button @click="router.push('/')" class="mt-5 ml-16"><arrow-circle-left-icon class="w-12 h-12 transition text-blue-500"/></button>
      </div>
    </div>
    <img style="transition: all 0.5s ease;" src="login.svg" class="ml-20 absolue w-1/3">
  </div>

</template>


<style scoped>
button.card {
  @apply flex items-center rounded py-2 px-4 shadow-md bg-white hover:shadow-lg m-2 transition-all
}
</style>