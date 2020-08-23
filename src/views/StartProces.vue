<template>
  <v-row class="justify-center">
    <v-col class="col-3"></v-col>
    <v-col class="col-4">
      <v-sheet class="pa-12 mt-10 mb-10" elevation="4" tile>
        <v-row class="justify-center align-center mb-4">
          <v-avatar tile height="auto" width="150px" class="mb-3">
            <img src="" alt="LOGO" />
          </v-avatar>
        </v-row>
        <v-form @submit.prevent="sendVariables">
          <v-text-field
            v-model="start"
            label="Test"
            placeholder="Ovdje testiraj matching"
            row-height="14"
            rows="2"
            auto-grow
            clearable
            dense
            class="ml-4 mr-4 mb-4"
          ></v-text-field>
          <v-checkbox class="my-3 ml-4 mr-4 mb-4" v-model="PrijavaZavrsni" label="Prijava završnog rada"></v-checkbox>
          <v-checkbox class="my-3 ml-4 mr-4 mb-4" v-model="UpisDiplomski" label="Upis na diplomski studij"></v-checkbox>
          <v-checkbox class="my-3 ml-4 mr-4 mb-4" v-model="Informacije" label="Želim informacije"></v-checkbox>
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
  components: {
  },
  data() {
    return {
      start: "",
      PrijavaZavrsni: false,
      UpisDiplomski: false,
      Informacije: false,
    }
  },
  methods: {
    sendVariables() {
      if(this.PrijavaZavrsni == true) 
        var key = "PrijavaZavrsnogRada";
      else
        return "Nope";
      axios.defaults.baseURL = "http://localhost:5000";
      axios.post(`/api/instance/${key}`, {
      })
      .then(
        response => {
          console.log(response);
        },
        error => {
          console.log(error);
        }
      );
    }
  }
}
</script>