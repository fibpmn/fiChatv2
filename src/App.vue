<template>
  <v-app>
    <Drawer />
    <Header />
    <Main />
  </v-app>
</template>

<script>
import Drawer from "./components/Drawer";
import Header from "./components/Header";
import Main from "./components/Main";
import EventBus from "./components/EventBus";
import jwtDecode from "jwt-decode";

export default {
  name: "App",
  components: {
    Drawer,
    Header,
    Main
  },
  data() {
      const token = localStorage.usertoken;
      const decoded = jwtDecode(token);
      localStorage.setItem("firstName", decoded.identity.firstName)
      localStorage.setItem("lastName", decoded.identity.lastName)
      localStorage.setItem("username", decoded.identity.username)
    return {
      firstName: decoded.identity.firstName,
      lastName: decoded.identity.lastName,
      username: decoded.identity.username,
      auth: "",
      user: ""
    };
  },
  mounted() {
    EventBus.$on("logged-in", status => {
      this.auth = status;
    });
  }
};
</script>

<style lang="scss">
#theme--light.v-application {
  background-clip: content-box;
  color: "#060606";
}
</style>