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
let comments = $ref()
let name = state.user.name
let information = $ref()
let id = state.user.id

async function createComment() {
    console.log("Create")
    console.log(creator);
    console.log(comments);
    axios.post('/api/add-comment', {
            'title': title,
            'content': content,
            'creator': creator,
            'comment': information,
            'name': name
        })
        .then(async function(res) {
            console.log('res:' + res.data)
            id = res.data
            await getComment()
            postTitle = null
            postContent = null
        })
        .catch(function(error) {
            console.log(error);
        });
}

async function getComment() {
    axios.post('/api/get-comment', {
            'id': id
        })
        .then(async function(res) {
            comments = res.data
            console.log("This is id:" + id)
            console.log(comments)
            //console.log("Hello")
        })
        .catch(function(error) {
            console.log(error);
        });
}
</script>

<template>
    <div class="h-screen bg-gradient-to-b from-blue-100 to-purple-100">
        <button class="fixed top-10 left-5 w-20 rounded py-2 px-4 shadow-md bg-red-300 hover:shadow-lg m-2 transition-all" @click="router.push('/forum')"> return </button>
        <h1 class="text-5xl font-medium grid grid-cols-1 place-items-center text-amber-400 h-24"> Post View: {{title}} </h1>
        <div class="grid grid-row-3">
            <div class="border-2 border-red-500 w-4/5 overflow-auto" style="height: 350px; position: absolute;
             left: 50%; transform: translateX(-50%);">
                <h1 class="text-3xl font-medium grid grid-cols-1 place-items-center text-blue-400 h-12"> Post Content </h1>
                <h1 class="text-2xl font-medium grid grid-cols-1 place-items-center text-green-400 h-12"> Creator: {{creator}} </h1>
                <div class="mx-20 ml-10"> {{content}} </div>
            </div>
            <div class="border-2 border-blue-500 w-4/5 overflow-auto" style="height: 200px; position: absolute;
             left: 50%; top: 55%; transform: translateX(-50%);">
                <h1 class="text-3xl font-medium grid grid-cols-1 place-items-center text-blue-400"> Comments </h1>
            <template> {{ getComment() }}</template>
            <div v-for="comment_list in comments" v-if="comments != null">
                <div v-for=" comments in comment_list" v-if="comment_list != null">
                    {{comments[0]}} : {{comments[1]}}
                </div>
            </div>

        </div>
            <div class="border-2 border-green-500 w-4/5 overflow-auto" style="height: 150px; position: absolute;
             left: 50%; top:80%; transform: translateX(-50%);">
                <h1 class="text-2xl font-medium grid grid-cols-1 place-items-center text-blue-400"> New Comment </h1>
                <div style="display: grid; grid-template-columns: 80% 20%">
                <textarea class="w-4/5 mt-2" id="textarea" rows="3" placeholder="Write here..." v-model="information"></textarea>
                <button class="rounded py-2 px-4 shadow-md bg-red-300 hover:shadow-lg m-2 transition-all ml-20 mt-10 text-center" @click="createComment"> create comment </button>
                </div>
            </div>
        </div>
    </div>
</template>


<style scoped>

</style>