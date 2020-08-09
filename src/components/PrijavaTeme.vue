<template>
    <v-row class="justify-center">
      <v-col class="col-3"></v-col>
      <v-col class="col-4">
        <v-sheet class="pa-12 mt-10 mb-10" elevation="4" tile >
          <v-row class="justify-center align-center mb-4">
            <v-avatar tile height="auto" width="150px" class="mb-3">
              <img src="/1961V2.png" alt="LOGO">
            </v-avatar>
          </v-row>
          <v-form @submit.prevent="login">
          <v-text-field
            v-model="Naslov"
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
            v-model="Sazetak"
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
            v-model="Mentori"
            class="my-3 mt-3 ml-4 mr-4 mb-4"
            label="Mentori"
            placeholder="Unesite potencijalne mentore"
            row-height="14"
            rows="3"
            auto-grow
            clearable
            dense
          ></v-text-field>
            <div class="text-center pt-0 pb-0 my-3">
              <v-btn tile depressed @click.prevent="" type="submit" class="ma-2 signbtn" outlined> POSALJI </v-btn>
            </div>        
          </v-form>
        </v-sheet>
      </v-col>
      <v-col class="col-3"></v-col>
    </v-row>
</template>

<script>
export default {
    name: 'PrijavaTeme',
    data() {
        return {
            Naslov: "",
            Sazetak: "",
            Mentori: [],
        }
    }
}
</script>

<style lang="scss">

</style>