<template>
  <v-container class="bg" fill-height fluid>
    <v-row align="center" justify="center">
      <v-col class="col-3"></v-col>
      <v-col class="col-6">
        <div v-if="show">
          <v-sheet elevation="1" tile color="white" class="mt-16 pa-5">
            <vue-form-generator :schema="schema" :model="model" :options="formOptions"></vue-form-generator>
            <v-btn class="ml-2 mt-1" tile depressed @click="SendTaskVariables">Pošalji</v-btn>
          </v-sheet>
          <v-alert :value="success" type="success">Podaci su uspješno poslani.</v-alert>
        </div>
      </v-col>
      <v-col div="col-3"></v-col>
    </v-row>
  </v-container>
</template>

<script>
import { Camunda } from "@/services";
import router from "../router";

export default {
  name: "UserTaskForm",
  data() {
    return {
      username: this.$store.state.username,
      model: {},
      schema: {},
      show: false,
      formOptions: {
        validateAfterLoad: true,
        validateAfterChanged: true,
        validateAsync: true,
      },
      success: false,
    };
  },
  mounted() {
    if (this.$store.state.auth) this.getVariables()
    else this.dialog = true;
  },
  methods: {
    async getVariables() {
      var username = this.username;
      var data = await Camunda.getTaskVariables(username);
      if (typeof data != "string") {
        this.show = true;
        var mentori = await Camunda.getMentors();
        if (data.model.Mentor != null) {
          for (let i = 0; i < data.schema.fields.length; i++) {
            if (data.schema.fields[i].model == "Mentor") {
              delete data.schema.fields[i].inputType;
              data.schema.fields[i].type = "select";
              data.schema.fields[i].values = mentori[0]; //generator zahtijeva array, problem unutarnje pretvorbe?
            }
          }
          this.model = data.model;
          this.schema = data.schema;
        }
      }
    },
    async SendTaskVariables() {
      var temp = {};
      var variables = {};
      Object.entries(this.model).map((fieldM) => {
        Object.entries(this.schema.fields).map((fieldS) => {
          if (typeof fieldM[1] === "boolean") fieldS[1].inputType = "boolean";
          else fieldS[1].inputType = "String";
          temp = {
            [`${fieldM[0]}`]: {
              value: fieldM[1],
              type: fieldS[1].inputType,
            },
          };
        });
        Object.assign(variables, temp);
      });
      variables.Mentor.value = variables.Mentor.value.replace(/ /g, "");
      let username = this.username;
      await Camunda.completeTaskForm(username, variables);
      this.success = true;
      setTimeout(router.push({ name: "Chat" }), 4000);
    },
  },
};
</script>

<style lang="scss">
.vue-form-generator {
  padding: 10px 10px 10px 10px;
}
.form-control {
  border-radius: 0px !important;
}
fieldset {
  border-left-width: 0px;
  border-left-style: solid;
  border-top-width: 0px;
  border-top-style: solid;
  border-right-width: 0px;
  border-right-style: solid;
  border-bottom-width: 0px;
  border-bottom-style: solid;
}
.bg {
  background-image: url("/bg.png");
}
</style>