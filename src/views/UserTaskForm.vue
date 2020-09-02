<template>
  <v-card>
    <vue-form-generator :schema="schema" :model="model" :options="formOptions"></vue-form-generator>
    <v-btn @click="SendTaskVariables">Pošalji</v-btn>
  </v-card>
</template>

<script>
import { Camunda } from "@/services";
import jwtDecode from "jwt-decode";

export default {
  name: "UserTaskForm",
  data() {
      const token = localStorage.usertoken;
      const decoded = jwtDecode(token);
      localStorage.getItem("username", decoded.identity.username)
    return {
      model: {},
      schema: {},
      formOptions: {},
      username: decoded.identity.username,
    };
  },
  mounted() {
    this.getTaskFormVariables();
  },
  methods: {
    async SendTaskVariables() {
      var temp = {};
      var variables = {};
      Object.entries(this.model).map(fieldM => {
        Object.entries(this.schema.fields).map(fieldS => {
          if (typeof fieldM[1] === "boolean") fieldS[1].inputType = "boolean";
          else fieldS[1].inputType = "String";
          temp = {
            [`${fieldM[0]}`]: {
              value: fieldM[1],
              type: fieldS[1].inputType
            }
          };
        });
        Object.assign(variables, temp);
      });
      let assignee = this.username
      let id = await Camunda.getTaskId(assignee)
      await Camunda.completeTaskForm(id, variables);
    },
    async getTaskFormVariables() {
      var username = this.username
      let data = await Camunda.getTaskFormVariables(username);
      this.model = data.model;
      this.schema = data.schema;
    }
  }
};
</script>