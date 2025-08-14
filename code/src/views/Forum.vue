<script setup>
import { UserAddIcon } from '@heroicons/vue/outline'
import Popper from './Popper.vue'
import axios from "axios";
import { salt, sha256, short } from "../utils/crypto";
import AffairCard from '../components/AffairCard.vue'
import PostCard from '../components/PostCard.vue'
import { useRouter } from 'vue-router'
const router = useRouter()
let postTitle = $ref()
let postContent = $ref()

import state from '../state.js'
let user = state.user.name
let id =state.user.id
let file
let postList = $ref()

function getFile(event) {
    file = event.target.files;
    console.log(file);
    console.log(file.length);
    console.log(file[0]);
    console.log(file[0].name);
    console.log(file[0].value);
}

async function createPost() {
    axios.post('/api/create-post', {
            'title': postTitle,
            'content': postContent,
            'creator': user
        })
        .then(async function(res) {
            console.log('res:' + res.data)
            id = res.data['id']
            console.log("The id is :" + id)
            console.log('res:' + res.data)
            await getPost()
            postTitle = null
            postContent = null
            Swal.fire('Success', 'Create Success', 'success')
        })
        .catch(function(error) {
            console.log(error);
        });
}

async function getPost() {
    axios.get('/api/get-post')
        .then(async function(res) {
            postList = res.data
            console.log(postList)
        })
        .catch(function(error) {
            console.log(error);
        });
}
</script>

<template>
    <div class="h-screen bg-gradient-to-b from-blue-100 to-purple-100">
        <button class="fixed top-10 left-5 w-20 rounded py-2 px-4 shadow-md bg-red-300 hover:shadow-lg m-2 transition-all" @click="router.push('/homePage')"> return </button>
        <h1 class="text-4xl font-medium grid grid-cols-1 place-items-center text-amber-400 h-24"> Post List </h1>
        <div class="overflow-auto" style="height: 450px">
            <template> {{ getPost() }} </template>
            <div v-for="a in postList" v-if="postList != null">
                <post-card :post="a" v-if="a != 'None'"></post-card>
            </div>
        </div>
        <div class="flex flex-col justify-center items-center">
            <div class="grid grid-cols-2 fixed bottom-52">
                <label class="block text-md font-bold" for="name"> Post name: </label>
                <input class="shadow appearance-none border rounded leading-tight focus:outline-none focus:shadow-outline" type="text" placeholder="undefined name" v-model="postTitle">
            </div>
            <textarea class="w-3/4 items-center fixed bottom-20" id="textarea" rows="5" placeholder="Write here..." v-model="postContent"></textarea>
            <div class="grid grid-cols-2 fixed bottom-0">
                <input class="rounded py-2 px-4 shadow-md bg-red-300 hover:file:shadow-lg m-2 transition-all ml-20 mt-10
            file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sx file:font-semibold          file:bg-violet-50 file:text-violet-700" type="file" multiple="multiplt" @change="getFile($event)" />
                <button class="rounded py-2 px-4 shadow-md bg-red-300 hover:shadow-lg m-2 transition-all ml-20 mt-10" @click="createPost"> create post </button>
            </div>
        </div>
    </div>
</template>


<style scoped>

</style>