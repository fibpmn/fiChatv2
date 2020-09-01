<template>
  <v-app>
    <Drawer :firstName="firstName" :lastName="lastName" :username="username" :id="id" :auth="auth" />
    <Header :firstName="firstName" :lastName="lastName" :username="username" :id="id" :auth="auth" />
    <Main :firstName="firstName" :lastName="lastName" :username="username" :id="id" :auth="auth" />
  </v-app>
</template>

<script>
import Drawer from "./components/Drawer";
import Header from "./components/Header";
import Main from "./components/Main";
import jwtDecode from "jwt-decode";

export default {
  name: "App",
  components: {
    Drawer,
    Header,
    Main
  },
  data() {
    return {
      firstName: "",
      lastName: "",
      username: "",
      id: "",
      auth: false
    };
  },
  mounted() {
    if(localStorage.getItem("usertoken") !== null) {
      this.auth=true
      const token = localStorage.usertoken;
      const decoded = jwtDecode(token);
      localStorage.setItem("firstName", decoded.identity.firstName)
      this.firstName = decoded.identity.firstName,
      localStorage.setItem("lastName", decoded.identity.lastName)
      this.lastName = decoded.identity.lastName,
      localStorage.setItem("username", decoded.identity.username)
      this.username = decoded.identity.username,
      localStorage.setItem("id", decoded.identity.id)
      this.id = decoded.identity.id
    } else {
      this.auth=false
    }
  }
};
</script>

<style lang="scss">
#theme--light.v-application {
  background-clip: content-box;
  color: "#060606";
}
</style>