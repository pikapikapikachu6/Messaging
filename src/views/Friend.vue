<script setup>
import { UserAddIcon } from '@heroicons/vue/outline'
import Popper from './Popper.vue'
import axios from "axios";
import {salt, sha256, short} from "../utils/crypto";
import AffairCard from '../components/AffairCard.vue'

let username = $ref('')
let friend =  $ref([])
let result =  $ref([])
let user = $ref('')

import state from '../state.js'
console.log(state.user)

async function addFriendToDB() {
  axios.post('/api/add-friend', {
    'username': user,
    'friend': result
  })
      .then(resp => {
        console.log(resp)
        mes = resp.data
        if (mes === 'success') {
          router.push('/login')
        }
      })
      .catch(function (error) {
        mes = error
        console.log(error)
      })
}

async function addFriend() {
  axios.post('/api/check-friend', {
    'username': username
  })
  .then(async function (res) {
    console.log(res)
    result = res.data
    if (result === false) {
      Swal.fire('Error', 'username not exists', 'error')
    } else {
      friend.push(result)
      await addFriendToDB()
    }
  })
  .catch(function (error) {
    console.log(error);
  });
  username = ''
}
</script>

<template>

  <div class="h-screen bg-gradient-to-b from-blue-100 to-purple-100">
    <h1 class="text-4xl font-medium grid grid-cols-1 place-items-center h-40 text-rose-700"> Welcome to Messaging Tool ~ </h1>
    <h1 class="text-3xl font-medium grid grid-cols-1 place-items-center text-amber-400"> Friend List </h1>
    <button class="card" @click="$refs.PopperCom.show($event)"> Add Friend </button>
    <Popper ref="PopperCom">
      <input class="shadow appearance-none border rounded py-2 px-2 mt-3" id="username" type="text" placeholder="Enter username" v-model="username">
      <button class="rounded py-2 px-4 shadow-md bg-red-100 ml-3" @click="addFriend()">Add</button>
    </Popper>

    
    <div v-for="a in friend">
      <affair-card :friend="a"></affair-card>
    </div>
  </div>

</template>


<style scoped>
button.card {
  @apply flex items-center rounded py-2 px-4 shadow-md bg-pink-200 hover:shadow-lg m-2 transition-all ml-20 mt-10
}
</style>