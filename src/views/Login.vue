<script setup>
import { LoginIcon, UserAddIcon, UserGroupIcon } from '@heroicons/vue/outline'
import { ArrowCircleRightIcon, ArrowCircleLeftIcon } from '@heroicons/vue/solid'
import {HS256, sha256, short, salt, sha256a} from '../utils/crypto.js'
import axios from 'axios'

import { useRouter } from 'vue-router'
import {watchEffect} from "vue";

const router = useRouter()

let input = $ref('')
let random = $ref('')

let username = $ref('')
let pwd = $ref('')
let mes = $ref('')

let privateKey = $ref('')
let publicKey = $ref('')

let checkResult = $ref('')

let pk = $ref('')

let inputElement = $ref()
watchEffect(() => {
  if (inputElement) inputElement.focus()
})

function getRsaKeys(func){
  window.crypto.subtle.generateKey(
      {
        name: "RSA-OAEP",
        modulusLength: 2048, //can be 1024, 2048, or 4096
        publicExponent: new Uint8Array([0x01, 0x00, 0x01]),
        hash: {name: "SHA-256"}, //can be "SHA-1", "SHA-256", "SHA-384", or "SHA-512"
      },
      true, //whether the key is extractable (i.e. can be used in exportKey)
      ["encrypt", "decrypt"] //must be ["encrypt", "decrypt"] or ["wrapKey", "unwrapKey"]
  ).then(function(key){
    window.crypto.subtle.exportKey(
        "pkcs8",
        key.privateKey
    ).then(function(keydata1){
      window.crypto.subtle.exportKey(
          "spki",
          key.publicKey
      ).then(function(keydata2){
        var privateKey = RSA2text(keydata1,1);
        var publicKey = RSA2text(keydata2);
        var code = {
          'privateKey':privateKey,
          'publicKey':publicKey
        }
        console.log(code)
        return code
        RSA2text(privateKey,publicKey);
      }).catch(function(err){
        console.error(err);
      });
    })
        .catch(function(err){
          console.error(err);
        });
  })
      .catch(function(err){
        console.error(err);
      });
}

function RSA2text(buffer,isPrivate=0) {
  var binary = '';
  var bytes = new Uint8Array(buffer);
  var len = bytes.byteLength;
  for (var i = 0; i < len; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  var base64 = window.btoa(binary);
  var text = base64.replace(/[^\x00-\xff]/g,"$&\x01").replace(/.{64}\x01?/g,"$&\n");
  return text;
}

async function pass() {
  console.log('random: ' + random)
  console.log('input: ' + input)
  if (!input) return
  if (!random) { // first
    axios.post('/api/login-first', {
      'username': input
    })
    .then(function (response) {
      checkResult = response.data['result']
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
  } else {
    if (username != 'there is error') {
      axios.post('/api/login-second', {
        'username': username,
        'password':  await sha256(short(await sha256(input + salt)) + random)
      })
      .then(function (response) {
        mes = response.data
        console.log(mes)
        if (mes == true) {
          router.push('/friend')
        }
      })
      .catch(function (error) {
        console.log(error);
      });
    }
    random = ''
  }
  input = ''
}

</script>

<template>
  <div class="h-screen bg-gradient-to-b from-blue-100 to-purple-100 flex justify-center items-center">
    <div class="w-full max-w-md" >
      <form class="bg-white shadow-md rounded px-8 pt-10 pb-10 mb-4">
        <h1 class="text-3xl font-medium grid grid-cols-1 place-items-center"> Login </h1>
        <div class="mb-6 mt-10">
          <input ref="inputElement" class="w-2/3 ml-14 mt-4 mb-4 rounded px-3 py-2 radius-2 border-2 border-gray-300 focus:ring-1 focus:border-blue-300 transition"
            :placeholder="random ? 'Please input the password' : 'Please input the username'"
            :type="random ? 'password' : 'text'"
            v-model="input" @keyup.enter="pass()"
          >
        </div>
        <button @click="pass()" name="toNext" class="mt-5 ml-28"><arrow-circle-right-icon class="w-12 h-12 transition" :class="input ? 'text-blue-500' : 'text-gray-300'"/></button>
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