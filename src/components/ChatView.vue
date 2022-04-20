<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
const props = defineProps(['name'])
</script>

<template>
  {{ props.hisName }}
  <div class="h-screen bg-gradient-to-b from-blue-100 to-purple-100">
    <h1 class="text-4xl font-medium grid grid-cols-1 place-items-center h-40 text-rose-700"> chat with {{
        props.hisName}} </h1>
  </div>
</template>
