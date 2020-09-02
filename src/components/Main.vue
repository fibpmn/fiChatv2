<template>
    <v-main>
    <v-container fluid>
      <router-view :firstName="firstName" :lastName="lastName" :username="username" :id="id" :auth="auth"></router-view>
    </v-container>
    </v-main>
</template>

<script>
export default {
    name: 'Main',
    props: ['firstName', 'lastName', 'username', 'id', 'auth'],
}
</script>