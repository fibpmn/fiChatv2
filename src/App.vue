<template>
  <v-app>
    <Drawer/>
    <Header/>
    <Main/>
  </v-app>
</template>

<script>
import Drawer from './components/Drawer'
import Header from './components/Header'
import Main from './components/Main'
// import tojetaforma from './components/forms/Pristup/tojetaforma'

export default {
  name: "App",

  components: {
    Drawer,
    Header,
    Main,
    // tojetaforma
  },

  data: () => ({
    //
  })
};
</script>
