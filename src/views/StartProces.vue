<template>
  <v-row class="justify-center">
    <v-col class="col-3"></v-col>
    <v-col class="col-4">
      <v-sheet class="pa-12 mt-10 mb-10" elevation="4" tile>
        <v-row class="justify-center align-center mb-4">
          <v-avatar tile height="auto" width="150px" class="mb-3">
            <img src alt="LOGO" />
          </v-avatar>
        </v-row>
        <v-form @submit.prevent="StartProcessInstance">
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
          <div>
            <v-checkbox
              class="my-3 ml-4 mr-4 mb-4"
              v-model="item.value"
              v-for="item in model"
              :label="item.name"
              :key="item.key"
            ></v-checkbox>
          </div>
          <div class="text-center pt-0 pb-0 my-3">
            <v-btn
              tile
              depressed
              @click.prevent="StartProcessInstance"
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
import { Camunda } from "@/services";
import jwtDecode from "jwt-decode";

export default {
  components: {},
  data() {
      const token = localStorage.usertoken;
      const decoded = jwtDecode(token);
      localStorage.getItem("username", decoded.identity.username)
    return {
      start: "",
      username: decoded.identity.username,
      model: []
    };
  },
  mounted() {
    this.getProcesses();
  },
  methods: {
    async StartProcessInstance() {
      var key = ""
      var name = ""
      this.model.forEach(index => {
        if(index.value == true) {
          key = index.key
          name = index.name
        }
      })
      await Camunda.StartProcessInstance(key, name, this.username);
    },
    async getProcesses() {
      this.processes = await Camunda.getProcesses();
      this.processes.map(process => {
        const element = {
        name: process.name,
        key: process.key,
        value: false, 
        }
        this.model.push(element)
      });
    }
  }
};
</script>