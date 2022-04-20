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

function chat() {
  user.friend = props.friend
  router.push("/chat")
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
