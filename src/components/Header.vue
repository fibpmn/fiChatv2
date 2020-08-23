<template>
    <v-app-bar app clipped-right dense flat color="blue lighten-1">
        <v-btn class="mr-3" to="/">Home</v-btn>
        <v-btn class="mr-3" to="/startproces">Start Process Instance</v-btn>
        <v-btn class="mr-3" to="/usertaskform">First User Task Form</v-btn>
    </v-app-bar>
</template>

<script>
export default {
    name: 'Header',
}
</script>

<style lang="scss">
.v-toolbar__content{
    box-shadow: 0px 2px #90CAF9 !important;
}
</style>
