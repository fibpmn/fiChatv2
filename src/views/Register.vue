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
          <v-form @submit.prevent="register">
            <v-text-field v-model="email" required label="E-mail" clearable class="ml-4 mr-4"></v-text-field>
            <v-text-field v-model="firstName" required label="Ime" clearable class="ml-4 mr-4"></v-text-field>
            <v-text-field v-model="lastName" required label="Prezime" clearable class="ml-4 mr-4"></v-text-field>
            <v-text-field
              v-model="password"
              type="password"
              required
              label="Lozinka"
              clearable
              class="ml-4 mr-4"
            ></v-text-field>
            <v-btn
              tile
              depressed
              color="primary"
              class="text-right"
              @click="register"
            >Registriraj se</v-btn>
          </v-form>
        </v-sheet>
      </v-col>
      <v-col class="col-4 hidden-xs hidden-sm"></v-col>
    </v-row>
  </v-container>
</template>

<script>
import { Auth, Rooms } from "@/services";
import router from "../router";

export default {
  name: "Register",
  data() {
    return {
      email: "",
      firstName: "",
      lastName: "",
      password: "",
    };
  },
  methods: {
    async register() {
      var data = {
        email: this.email,
        firstName: this.firstName,
        lastName: this.lastName,
        password: this.password,
      };
      await Auth.RegisterUser(data),
        await Rooms.createRoom(this.email, "fibot@unipu.hr", "Recepcija").then(
          router.push({ name: "Login" })
        );
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