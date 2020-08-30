<template>
    <v-app-bar app clipped-right dense flat color="#060606">
        <v-btn tile class="mr-3" text color="white" to="/startproces">Start Process Instance</v-btn>
        <v-btn tile class="mr-3" text color="white" to="/usertaskform">First User Task Form</v-btn>
        <v-btn tile class="mr-3" text color="white" to="/register">Registriraj se</v-btn>
        <v-btn tile class="mr-3" text color="white" to="/login">Logiraj se</v-btn>

        <!-- <v-btn class="mr-3" v-if="auth==loggedin" to="/logi">Logiraj se</v-btn> -->
    </v-app-bar>
</template>

<script>
import EventBus from './EventBus.vue'

EventBus.$on('logged-in', test => {console.log(test)})

export default {
    name: 'Header',
    data () {
        return {
            auth: '',
            user: ''
        }
    },
    methods: {
        logout() {
            localStorage.removeItem('usertoken')
        }
    },
    mounted() {
        EventBus.$on('logged-in', status => {
            this.auth = status
        })
    }
}
</script>

<style lang="scss">
// .v-toolbar__content{
//     box-shadow: 0px 2px #90CAF9 !important;
// }
</style>
