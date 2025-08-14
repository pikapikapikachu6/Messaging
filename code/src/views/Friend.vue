<script setup>
import { UserAddIcon } from '@heroicons/vue/outline'
import Popper from './Popper.vue'
import axios from "axios";
import {salt, sha256, short} from "../utils/crypto";
import AffairCard from '../components/AffairCard.vue'
import { useRouter } from 'vue-router'
const router = useRouter()

let username = $ref('')
const friend =  $ref([])
let addfriend = $ref('')

console.log("friend start:")
console.log(friend)
let result =  $ref([])
let user = $ref('')
let mes = $ref('')

import state from '../state.js'
if (typeof(state.user.name) == "undefined") {
  router.push("/login")
}
user = state.user.name
if (user != null) getFriendList()
else router.push("/login")


async function addFriendToDB() {
  console.log("add friend")
  console.log(addfriend)
  axios.post('/api/add-friend', {
    'username': user,
    'friend': addfriend
  })
      .then(resp => {
        console.log(resp)
        mes = resp.data
        if (mes === 'success') {
          router.push('/login')
        }
      })
      .catch(function (error) {
        console.log(error)
      })
}

async function addFriend() {
  addfriend = username
  axios.post('/api/check-friend', {
    'username': username
  })
      .then(async function (res) {
        console.log('res:' + res.data)
        result = res.data
        if (result === false) {
          Swal.fire('Error', 'username not exists', 'error')
        } else {
          console.log('username add:')
          console.log(addfriend)
          await addFriendToDB()
          if (result.toString() === state.user.name.toString()) {
            Swal.fire('Error', 'cannot add yourself', 'error')
          } else if (friend.indexOf(result.toString()) >= 0) {
            Swal.fire('Error', 'friend already exists', 'error')
          } else {
            friend.push(result.toString())
          }
          console.log(friend)
        }
      })
      .catch(function (error) {
        console.log(error);
      });
  username = ''
}

async function getFriendList() {
  axios.post('/api/get-friend-list', {
    'username': user,
  })
      .then(resp => {
        result = resp.data
        if (result != '') {
          console.log("none here:")
          console.log(resp.data)
          console.log(result)
          result = result.trim().split(/\s+/)
          console.log("friend is :  ")
          console.log(result)
          for (let i = 0; i < result.length; i++) {
            console.log(result[i])
            if (friend.indexOf(result[i].toString()) < 0) {
              friend.push(result[i].toString())
            }
          }
          console.log(friend)
        }
      })
      .catch(function (error) {
        console.log(error)
      })
}

function logout() {
  state.user = {}
  router.push('/')
}

</script>

<template>
  <div class="h-screen bg-gradient-to-b from-blue-100 to-purple-100">
    <button class="fixed top-10 left-5 w-20 rounded py-2 px-4 shadow-md bg-red-300 hover:shadow-lg m-2 transition-all"
            @click="router.push('/homePage')"> return </button>
    <h1 class="text-4xl font-medium grid grid-cols-1 place-items-center h-40 text-rose-700"> Welcome to Messaging Tool ~ </h1>
    <h1 class="text-3xl font-medium grid grid-cols-1 place-items-center text-amber-400"> Friend List </h1>
    <div class="flex justify-center">
      <button class="flex items-center rounded py-2 px-4 shadow-md bg-red-300 hover:shadow-lg m-2 transition-all ml-20 mt-10" @click="logout">Logout</button>
      <button class="flex items-center rounded py-2 px-4 shadow-md bg-pink-200 hover:shadow-lg m-2 transition-all ml-20 mt-10" @click="$refs.PopperCom.show($event)"> Add Friend </button>
      <Popper ref="PopperCom">
        <input class="shadow appearance-none border rounded py-2 px-2 mt-3" id="username" type="text" placeholder="Enter username" v-model="username" @keyup.enter="addFriend">
        <button class="rounded py-2 px-4 shadow-md bg-red-100 ml-3" @click="addFriend">Add</button>
      </Popper>
    </div>
    <div v-for="a in friend">
      <affair-card :friend="a" v-if="a != 'None'"></affair-card>
    </div>
  </div>

</template>


<style scoped>
</style>