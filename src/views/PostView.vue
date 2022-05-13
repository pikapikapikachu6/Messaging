<script setup>
import { UserAddIcon } from '@heroicons/vue/outline'
import Popper from './Popper.vue'
import axios from "axios";
import { salt, sha256, short } from "../utils/crypto";
import AffairCard from '../components/AffairCard.vue'
import PostCard from '../components/PostCard.vue'
import { useRouter } from 'vue-router'
const router = useRouter()

import state from '../state.js'
let user = state.user
let title = user.postTitle
let content = user.postContent
let creator = user.postCreator
let comments = user.comments



</script>

<template>
    <div class="h-screen bg-gradient-to-b from-blue-100 to-purple-100">
        <button class="fixed top-10 left-5 w-20 rounded py-2 px-4 shadow-md bg-red-300 hover:shadow-lg m-2 transition-all" @click="router.push('/forum')"> return </button>
        <h1 class="text-5xl font-medium grid grid-cols-1 place-items-center text-amber-400 h-24"> Post View </h1>
         <div class="grid grid-row-2">
        <div class="border-2 border-red-500 w-4/5 overflow-auto" style="height: 350px; position: absolute;
         left: 50%; transform: translateX(-50%);">
            <h1 class="text-3xl font-medium grid grid-cols-1 place-items-center text-blue-400 h-12"> Post Content </h1>
            <h1 class="text-2xl font-medium grid grid-cols-1 place-items-center text-green-400 h-12"> Creator: {{creator}} </h1>
            <div class="mx-20 ml-10"> {{content}} </div>
        </div>
        <div class="border-2 border-blue-500 w-4/5 overflow-aut" style="height: 200px; position: absolute;
         left: 50%; top: 60%; transform: translateX(-50%);">
            <h1 class="text-3xl font-medium grid grid-cols-1 place-items-center text-blue-400"> Comments </h1>
            <div v-for="comm in comments"> {{comm}} </div>
        </div>
        </div>
    </div>
</template>


<style scoped>

</style>