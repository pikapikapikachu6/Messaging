<script setup>
import { useRouter } from 'vue-router'
import { ChatIcon } from '@heroicons/vue/outline'
const router = useRouter()
const props = defineProps(['friend'])

</script>

<template>
  <div class="py-4 px-20 flex justify-between my-3 rounded-full mx-72 bg-white shadow all-transition hover:shadow-md">
    <div class="text-xl sm:text-2xl font-bold mb-1 ">
      {{ props.friend }}
    </div>
    <button class="text-xl sm:text-2xl font-bold text-black-500" @click="router.push('/')">
      <chat-icon class="w-6 text-red-500 mr-2"/>
    </button>
  </div>
</template>
