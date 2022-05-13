<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
import { ChatIcon } from '@heroicons/vue/outline'
import axios from 'axios'
import { toRaw } from '@vue/reactivity'

const props = defineProps(['post'])
let post = toRaw(props.post)
let postContent = []
for (let a in post) {
  postContent[a] = post[a]
}
let title = postContent[0]
let content = postContent[1]
let creator = postContent[2]

import state from '../state.js'
if (typeof(state.user.name) == "undefined") {
  router.push("/login")
}
let user = state.user

function view() {
  user.postTitle = title
  user.postContent = content
  user.postCreator = creator
  router.push("./postView")
}

</script>

<template>
  <div class="py-4 px-20 flex justify-between my-3 rounded-full mx-72 bg-white shadow all-transition hover:shadow-md" v-if="props.post!=null">
    <button class="text-xl sm:text-2xl font-bold mb-1 grid grid-cols-2 mt-3"> 
      <div class="text-black"> {{title}} </div>
      <div class="text-blue-500 ml-24"> {{creator}} </div>
    </button>
    <div class="grid grid-cols-2">
      <button class="rounded-full py-2 px-4 shadow-md bg-red-300 hover:shadow-lg m-2 transition-all" @click="delete" v-if="user.admin==1">
        delete
      </button>
      <button class="rounded-full py-2 px-4 shadow-md bg-red-300 hover:shadow-lg m-2 transition-all" @click="view">
        view
      </button>
    </div>
  </div>
</template>
