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
        <v-form @submit.prevent="sendVariables">
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
            label="Sazetak"
            placeholder="Unesite sazetak rada"
            row-height="14"
            rows="3"
            auto-grow
            clearable
            dense
          ></v-text-field>
          <v-text-field
            v-model="dispozicija"
            class="my-3 mt-3 ml-4 mr-4 mb-4"
            label="Dispozicija"
            placeholder="Unesi dispoziciju rada"
            row-height="14"
            rows="3"
            auto-grow
            clearable
            dense
          ></v-text-field>
          <v-text-field
            v-model="literatura"
            class="my-3 mt-3 ml-4 mr-4 mb-4"
            label="Popis literature"
            placeholder="Unesi literaturu"
            row-height="14"
            rows="3"
            auto-grow
            clearable
            dense
          ></v-text-field>
          <v-combobox
            class="my-3 ml-4 mr-4 mb-4"
            v-model="selectedMentor"
            :items="items"
            placeholder="Odaberi moguće mentore"
            background-color
            item-color="black"
            auto-grow
            :clearable="true"
            hide-no-data
            label="Odaberi mentore"
            multiple
            dense
            hide-selected
            :rules="rules"
          ></v-combobox>
          <!-- <v-file-input
            label="Obrazac"
            class="my-3 ml-4 mr-4 mb-4"
            placeholder="Unesi ispunjeni obrazac"
            show-size
            clearable
            dense
          ></v-file-input>-->
          <v-checkbox class="my-3 ml-4 mr-4 mb-4" v-model="obrazac" label="Ispunjeni obrazac"></v-checkbox>
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
      dispozicija: "",
      literatura: "",
      obrazac: false,
      loading: false,
      rules: [], //rules predstavljaju validaciju inputa, pr. unos je predug/prekratak, maksimalno 20 char,...
      selectedMentor: [],
      items: [ // treba napuniti array items iz baze
        {
          text: "doc.dr.sc Darko Etinger",
          value: "DarkoID"
        },
        {
          text: "doc.dr.sc Nikola Tanković",
          value: "NikolaID"
        },
        {
          text: "doc.dr.sc Siniša Miličić",
          value: "SinisaID"
        }
      ]
    };
  },
  methods: {
    sendVariables() {
      let mentoriZaSlati = this.selectedMentor.map(mentor => {
        let objekt = {};
        //{"assigneeList": ["NikolaID", "DarkoID", "TihomirID"]}
        objekt["value"] = mentor.value;
        // objekt["type"] = "String";
        return objekt;
      });
      axios.defaults.baseURL = "http://localhost:5000";
      // axios.all([
          axios.post("/api/task/form", {
          id: "bc7e46aa-e140-11ea-8f89-60f262e99a90",
          naslov: this.naslov,
          sazetak: this.sazetak,
          dispozicija: this.dispozicija,
          literatura: this.literatura,
          obrazac: this.obrazac,
          mentori: mentoriZaSlati
        })
        //   axios.post("/api/task/form", {
        //   mentori: mentoriZaSlati
        // })
        //       ])
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
};
</script>

<style lang="scss">
</style>