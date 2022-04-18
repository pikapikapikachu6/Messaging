<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
</script>

<template>
  <div class="gradient-card py-4 px-6 flex items-center flex-wrap my-3 border">
    <div class="all-transition text-xl sm:text-2xl font-bold text-gray-500 mb-1 flex items-center"> {{ comData.guaranteeType }}
    </div>
  </div>
</template>
