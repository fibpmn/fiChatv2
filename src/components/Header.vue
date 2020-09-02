<template>
    <v-app-bar app clipped-right flat color="#060606">
        <img height="55px" class="ml-4" width="auto" src="/Logo.png" />
        <v-spacer></v-spacer>
    </v-app-bar>
</template>

<script>

export default {
    name: 'Header',
    //props: ['firstName', 'lastName', 'username', 'id', 'auth'],
    data () {
        return {
        }
    },
    methods: {
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
