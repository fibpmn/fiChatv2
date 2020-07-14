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

export default {
  name: "App",

  components: {
    Drawer,
    Header,
    Main,
  },

  data: () => ({
    //
  })
};
</script>
