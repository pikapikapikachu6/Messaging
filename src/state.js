import { reactive, watchEffect } from 'vue'

const state = reactive({
  user: {}
})

export default state

// cache
const SS = window.sessionStorage

if (SS.user) state.user = JSON.parse(SS.user)
watchEffect(() => { SS.user = JSON.stringify(state.user) })

