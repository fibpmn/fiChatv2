<template>
  <v-container class="bg" fill-height fluid>
    <v-row align="center" justify="center">
      <v-col class="col-4 hidden-xs hidden-sm"></v-col>
      <v-col class="col-4">
        <v-sheet elevation="2" tile class="text-right pa-15">
          <div align="center" justify="center">
            <v-avatar size="120" class="fi">
              <img src="/Fi.png" />
            </v-avatar>
          </div>
          <v-form @submit.prevent="login">
            <v-text-field v-model="email" required label="E-mail" class="mb-2" clearable></v-text-field>
            <v-text-field
              v-model="password"
              type="password"
              required
              label="Lozinka"
              class="mb-2"
              clearable
            ></v-text-field>
            <v-btn tile depressed color="primary" class="mt-4" @click="login">Logiraj se</v-btn>
          </v-form>
        </v-sheet>
      </v-col>
      <v-col class="col-4 hidden-xs hidden-sm"></v-col>
    </v-row>
  </v-container>
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
      await Auth.LoginUser(data);
      this.$store.commit("setToTrue"),
      this.setVariables(),
      router.push({ name: "Chat" });
    },
    setVariables() {
      const token = localStorage.getItem("usertoken");
      const decoded = jwtDecode(token);
      this.$store.dispatch("setFirstName", decoded.identity.firstName);
      this.$store.dispatch("setLastName", decoded.identity.lastName);
      this.$store.dispatch("setUsername", decoded.identity.username);
      this.$store.dispatch("setId", decoded.identity.id);
      var initials =
        decoded.identity.firstName.charAt(0) +
        decoded.identity.lastName.charAt(0);
      this.$store.dispatch("setInitials", initials);
    },
  },
};
</script>

<style lang="scss">
.fi {
  justify-content: space-around !important;
  align-items: center !important;
}
.bg {
  background-image: url("/bg.png");
}
</style>