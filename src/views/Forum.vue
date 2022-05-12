<script setup>
import { UserAddIcon } from '@heroicons/vue/outline'
import Popper from './Popper.vue'
import axios from "axios";
import { salt, sha256, short } from "../utils/crypto";
import AffairCard from '../components/AffairCard.vue'
import { useRouter } from 'vue-router'
const router = useRouter()
</script>

<template>
    <div class="h-screen bg-gradient-to-b from-blue-100 to-purple-100">
      <button class="fixed top-10 left-5 w-20 rounded py-2 px-4 shadow-md bg-red-300 hover:shadow-lg m-2 transition-all" @click="router.push('/homePage')"> return </button>
      <div class="flex flex-col justify-center items-center">
        <div class="grid grid-cols-2 fixed bottom-52">
            <label class="block text-md font-bold" for="name"> Post name: </label>
            <input class="shadow appearance-none border rounded leading-tight focus:outline-none focus:shadow-outline" type="text" placeholder="undefined name">
        </div>
        <textarea class="w-3/4 items-center fixed bottom-20" id="textarea" rows="5" placeholder="Write here..."></textarea>
        <div class="grid grid-cols-2 fixed bottom-0">
            <input class="rounded py-2 px-4 shadow-md bg-red-300 hover:file:shadow-lg m-2 transition-all ml-20 mt-10
        file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sx file:font-semibold          file:bg-violet-50 file:text-violet-700" type="file"/>
            <button class="rounded py-2 px-4 shadow-md bg-red-300 hover:shadow-lg m-2 transition-all ml-20 mt-10"> create post </button>
        </div>
      </div>
   </div>
</template>


<style scoped>

</style>