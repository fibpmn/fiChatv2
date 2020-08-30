<template>
  <v-card>
    <vue-form-generator :schema="schema" :model="model" :options="formOptions"></vue-form-generator>
    <v-btn @click="SendTaskVariables">Pošalji</v-btn>
  </v-card>
</template>

<script>
import { Camunda } from "@/services";

export default {
  name: "UserTaskForm",
  data() {
    return {
      model: {},
      schema: {},
      formOptions: {}
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
      var id = "2662a007-e649-11ea-b1fa-60f262e99a90";
      //slanje varijabli u bazu podataka
      await Camunda.completeTaskForm(id, variables);
      console.log(this.schema)
    },
    async getTaskFormVariables() {
      var key = "PrijavaZavrsnogRada";
      let data = await Camunda.getTaskFormVariables(key);
      this.model = data.model;
      this.schema = data.schema;
      console.log(this.schema)
    }
  }
};
</script>