<template>
    <v-main>
      <router-view :firstName="firstName" :lastName="lastName" :username="username" :id="id" :auth="auth"></router-view>
    </v-main>
</template>

<script>
export default {
    name: 'Main',
    props: ['firstName', 'lastName', 'username', 'id', 'auth'],
}
</script>