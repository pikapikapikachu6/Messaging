<script setup>
import { useRouter } from 'vue-router'
import { ChatIcon } from '@heroicons/vue/outline'
const router = useRouter()
const props = defineProps(['friend'])
import state from '../state.js'
if (typeof(state.user.name) == "undefined") {
  router.push("/login")
}
let user = state.user
let friendPK = $ref('')
let cipher = $ref('')

async function setDate() {
  await getFriendPk()
}

function chat() {
  console.log("chat firend result: " + user.friendPK)
  setDate()
  user.friend = props.friend
  // user.friendPK = friendPK
  router.push("/chat")
}

async function getFriendPk() {
  axios.post('/api/getPK', {
    'username': props.friend,
  })
  .then(resp => {
    console.log('resp result: ' + resp.data)
    user.friendPK = resp.data
    console.log('friend result: ' + user.friendPK)
  })
  .catch(function (error) {
    Swal.fire('Error', 'He is not login', 'error')
    console.log(error)
  })
}

</script>

<template>
  <div class="py-4 px-20 flex justify-between my-3 rounded-full mx-72 bg-white shadow all-transition hover:shadow-md">
    <div class="text-xl sm:text-2xl font-bold mb-1 ">
      {{ props.friend }}
    </div>
    <button class="text-xl sm:text-2xl font-bold text-black-500" @click="chat">
      <chat-icon class="w-6 text-red-500 mr-2"/>
    </button>
  </div>
</template>
