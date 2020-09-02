<template>
  <v-app>
    <Drawer
      :firstName="firstName"
      :lastName="lastName"
      :username="username"
      :id="id"
      :auth="auth"
      :initials="initials"
    />
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
    Main,
  },
  data() {
    return {};
  },
  mounted() {
    this.reAuth();
  },
  computed: {
    auth(auth) {
      auth = this.$store.state.auth;
      return auth;
    },
    firstName(firstName) {
      firstName = this.$store.state.firstName;
      return firstName;
    },
    lastName(lastName) {
      lastName = this.$store.state.lastName;
      return lastName;
    },
    username(username) {
      username = this.$store.state.username;
      return username;
    },
    id(id) {
      id = this.$store.state.id;
      return id;
    },
    initials(initials) {
      initials = this.$store.state.initials;
      return initials;
    },
  },
  methods: {
    reAuth() {
      if (localStorage.getItem("usertoken")) {
        const token = localStorage.usertoken;
        const decoded = jwtDecode(token);
        this.$store.commit("setToTrue")
        this.$store.dispatch("setFirstName", decoded.identity.firstName);
        this.$store.dispatch("setLastName", decoded.identity.lastName);
        this.$store.dispatch("setUsername", decoded.identity.username);
        this.$store.dispatch("setId", decoded.identity.id);
        var initials =
          decoded.identity.firstName.charAt(0) +
          decoded.identity.lastName.charAt(0);
        this.$store.dispatch("setInitials", initials);
      } else {
        this.$store.dispatch("setFirstName", "Anonymous");
        this.$store.dispatch("setUsername", "Anonymous");
        this.$store.dispatch("setInitials", "A");
      }
    },
  },
};
</script>

<style lang="scss">
#theme--light.v-application {
  background-clip: content-box;
  color: "#060606";
}
</style>