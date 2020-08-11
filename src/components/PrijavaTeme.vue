<template>
  <v-row class="justify-center">
    <v-col class="col-3"></v-col>
    <v-col class="col-4">
      <v-sheet class="pa-12 mt-10 mb-10" elevation="4" tile>
        <v-row class="justify-center align-center mb-4">
          <v-avatar tile height="auto" width="150px" class="mb-3">
            <img src="/1961V2.png" alt="LOGO" />
          </v-avatar>
        </v-row>
        <v-form @submit.prevent="login">
          <v-text-field
            v-model="naslov"
            label="Naslov"
            placeholder="Unesite naslov rada"
            row-height="14"
            rows="2"
            auto-grow
            clearable
            dense
            class="ml-4 mr-4 mb-4"
          ></v-text-field>
          <v-text-field
            v-model="sazetak"
            class="my-3 mt-3 ml-4 mr-4 mb-4"
            label="sazetak"
            placeholder="Unesite sazetak rada"
            row-height="14"
            rows="3"
            auto-grow
            clearable
            dense
          ></v-text-field>
          <v-text-field
            v-model="mentor1"
            class="my-3 mt-3 ml-4 mr-4 mb-4"
            label="Mentor"
            placeholder="Unesite potencijalnog mentora"
            row-height="14"
            rows="3"
            auto-grow
            clearable
            dense
          ></v-text-field>
          <v-text-field
            v-model="mentor2"
            class="my-3 mt-3 ml-4 mr-4 mb-4"
            label="Mentor"
            placeholder="Unesite potencijalnog mentora"
            row-height="14"
            rows="3"
            auto-grow
            clearable
            dense
          ></v-text-field>
          <div class="text-center pt-0 pb-0 my-3">
            <v-btn
              tile
              depressed
              @click.prevent="sendVariables"
              type="submit"
              class="ma-2 signbtn"
              outlined
            >POSALJI</v-btn>
          </div>
        </v-form>
      </v-sheet>
    </v-col>
    <v-col class="col-3"></v-col>
  </v-row>
</template>

<script>
import axios from "axios";
export default {
  name: "PrijavaTeme",
  data() {
    return {
      naslov: "",
      sazetak: "",
      mentori: [],
      mentor1: "",
      mentor2: "",
    };
  },
  methods: {
    sendVariables() {
      axios.defaults.baseURL = "http://localhost:5000";
      axios
        .post("/api/uzmiVarijable", {
          naslov: this.naslov,
          sazetak: this.sazetak,
          mentori: [
            {
              value: this.mentor1,
              type: "string",
            },
            {
              value: this.mentor2,
              type: "string",
            },
          ],
        })
        .then(
          (response) => {
            console.log(response);
          },
          (error) => {
            console.log(error);
          }
        );
    },
  },
};
</script>

<style lang="scss">
</style>