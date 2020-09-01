<template>
    <v-app-bar app clipped-right dense flat color="#060606">
        <v-btn v-show="auth" tile class="mr-3" text color="white" to="/startproces">Start Process Instance</v-btn>
        <v-btn v-show="auth" tile class="mr-3" text color="white" to="/usertaskform">First User Task Form</v-btn>
        <v-btn v-show="!auth" tile class="mr-3" text color="white" to="/register">Registriraj se</v-btn>
        <v-btn v-show="!auth" tile class="mr-3" text color="white" to="/login">Logiraj se</v-btn>
        <v-btn v-show="auth" tile class="mr-3" text color="white" @click="logout">Odlogiraj se</v-btn>
        <v-spacer></v-spacer>
        <img height="45px" width="auto" src="/Logo.png" />
    </v-app-bar>
</template>

<script>

export default {
    name: 'Header',
    props: ['firstName', 'lastName', 'username', 'id', 'auth'],
    data () {
        return {
        }
    },
    methods: {
        logout() {
            localStorage.removeItem('usertoken')
            localStorage.removeItem('firstName')
            localStorage.removeItem('lastName')
            localStorage.removeItem('username')
            localStorage.removeItem('id')
        }
    },
    mounted() {
    }
}
</script>

<style lang="scss">
// .v-toolbar__content{
//     box-shadow: 0px 2px #90CAF9 !important;
// }
</style>
