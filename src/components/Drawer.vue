<template>
  <v-navigation-drawer
    app
    bottom
    permanent
    right
    background
    
    fixed
    :clipped="true"
    color="blue lighten-1"
  ><!-- mini-variant expand-on-hover blue lighten-5 -->
    <v-list>
        <v-list-item style="align-center">
          <img class="pa-3" src="/Logo.png" />
        </v-list-item>
        </v-list>
        <v-list>
        <v-divider color="blue lighten-5"></v-divider>
        <v-list-item-group>
        <v-list-item>
          <v-avatar size="36" color="blue lighten-2">
            <span class="white--text">TS</span>  <!-- Get initials -->
          </v-avatar>
          <v-list-item-content class="justify-center ml-5 white--text">
            <v-list-item-title >{{"Ime"}} </v-list-item-title> <!-- Get user first name -->
            <v-list-item-title>{{"Prezime"}}</v-list-item-title> <!-- Get user last name -->
          </v-list-item-content>
          <v-btn color="blue lighten-2" small fab depressed>
            <v-icon color="white">mdi-account-edit</v-icon>
          </v-btn>
        </v-list-item>
      </v-list-item-group>
      <v-divider color="blue lighten-5"></v-divider>
      </v-list>
      <v-list>
      <v-list-item-group two-line>
        <v-list-item>
          <v-list-item-avatar>
            <img src="/Fi.png" />
          </v-list-item-avatar>
          <v-list-item-content class="justify-center white--text">
            <v-list-item-title>{{"Fi"}}</v-list-item-title>
            <v-list-item-title>Always Online</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-list>
    <v-divider color="white"></v-divider>
    <v-list-item disabled></v-list-item>
    <v-list-item disabled></v-list-item>
    <v-list-item disabled></v-list-item>
    <v-list-item disabled></v-list-item>
    <v-divider color="white"></v-divider>
    <v-list>
      <v-btn class="white--text" block large tile depressed @click="showact=!showact" color="blue lighten-1">Aktivni procesi</v-btn>
      <div v-show="showact">
        <v-list-item-group v-model="active" color="primary">
          <v-list-item v-for="(active, i) in active_processes" :key="i">
            <v-list-item-content>
            <v-list-item-title v-text="active.title"></v-list-item-title>
            <v-list-item-subtitle v-text="active.subtitle"></v-list-item-subtitle>
            <v-list-item-subtitle v-text="active.text"></v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </div>
    </v-list>
    <v-divider color="blue lighten-5"></v-divider>
    <v-list>
      <v-btn class="white--text" block large tile depressed @click="showinac=!showinac" color="blue lighten-1">Povijesni procesi</v-btn>
      <div v-show="showinac">
        <v-list-item-group v-model="inactive" color="primary">
          <v-list-item v-for="(inactive, i) in inactive_processes" :key="i" three-line>
            <v-list-item-content>
                <v-list-item-title v-text="inactive.title"></v-list-item-title>
                <v-list-item-subtitle v-text="inactive.subtitle"></v-list-item-subtitle>
                <v-list-item-subtitle v-text="inactive.text"></v-list-item-subtitle>
          </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </div>
    </v-list>
    <v-divider color="blue lighten-5"></v-divider>
  </v-navigation-drawer>
</template>

<script>
export default {
  name: "Drawer",
  //photo: null,
  data: () => ({
    inactive: 0,
    active: 0,
    i: 0,
    showact: false,
    showinac: false,
    active_processes: [
      {
        title: "Title Pepe",
        subtitle: "Subtitle Pepe1",
        text: "Text Pepe"
      },
      {
        title: "Title Pepe",
        subtitle: "Subtitle Pepe1",
        text: "Text Pepe"
      }
    ],
    inactive_processes: [
      {
        title: "Title Pepe",
        subtitle: "Subtitle Pepe1",
        text: "Text Pepe"
      },
      {
        title: "Title Pepe",
        subtitle: "Subtitle Pepe1",
        text: "Text Pepe"
      },
      {
        title: "Title Pepe",
        subtitle: "Subtitle Pepe1",
        text: "Text Pepe"
      }
    ]
  })
};
</script>

<style lang="scss">
.nesto {
  color: #bfcfff !important;
}
.v-navigation-drawer {
  z-index: 9999 !important;
}
.v-list {
    padding: 0px !important;
}
// .v-navigation-drawer__content{
//     box-shadow: 0px 2px #90CAF9 !important;
// }
</style>