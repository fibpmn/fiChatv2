<template>
  <v-row>
    <v-col class="col-3"></v-col>
    <v-col class="col-6">
      <v-sheet tile class="text-right mt-10">
        <v-form @submit.prevent="login">
          <v-text-field v-model="email" required label="E-mail" clearable class="ml-4 mr-4"></v-text-field>
          <v-text-field v-model="password" required label="Lozinka" clearable class="ml-4 mr-4"></v-text-field>
          <v-btn tile depressed color="primary" class="text-right" @click="login">Logiraj se</v-btn>
        </v-form>
      </v-sheet>
    </v-col>
    <v-col class="col-3"></v-col>
  </v-row>
</template>

<script>
import { Auth } from "@/services";
import router from "../router";
import jwtDecode from "jwt-decode";

export default {
  name: "Login",
  data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    async login() {
      var data = {
        email: this.email,
        password: this.password,
      };
      await Auth.LoginUser(data).then(
        this.$store.commit("setToTrue"),
        this.setVariables(),
        router.push({ name: "Chat" })
      );
    },
    setVariables() {
      const token = localStorage.getItem("usertoken")
      const decoded = jwtDecode(token);
      this.$store.dispatch("setFirstName", decoded.identity.firstName);
      this.$store.dispatch("setLastName", decoded.identity.lastName);
      this.$store.dispatch("setUsername", decoded.identity.username);
      this.$store.dispatch("setId", decoded.identity.id);
      var initials = (decoded.identity.firstName).charAt(0)+(decoded.identity.lastName).charAt(0)
      this.$store.dispatch("setInitials", initials)
    },
  },
};
</script>

<style lang="scss">
</style>