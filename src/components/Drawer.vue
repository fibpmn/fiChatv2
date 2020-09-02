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
    expand-on-hover=""
    src="https://images.unsplash.com/photo-1567346953362-1bb30e3c10ed?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1491&q=80"
  >
    <!-- <v-img src="https://wallpaper-house.com/wallpaper-id-342348.php" height="100%"></v-img> -->
    <!-- mini-variant expand-on-hover blue lighten-5 -->
    <!-- <v-list>
      <v-list-item style="align-center">
        <img class="pa-3" src="/Logo.png" />
      </v-list-item>
    </v-list> -->
        <v-list-item disabled></v-list-item>
    <v-list>
      <v-divider color="blue lighten-5"></v-divider>
      <v-list-item-group>
        <v-list-item>
          <v-avatar size="36" color="blue lighten-2">
            <span class="white--text">{{initials}}</span>
          </v-avatar>
          <v-list-item-content class="justify-center ml-5 white--text">
            <v-list-item-title>{{firstName}}</v-list-item-title>
            <v-list-item-title>{{lastName}}</v-list-item-title>
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
  </v-navigation-drawer>
</template>

<script>

export default {
  name: "Drawer",
  props: ['firstName', 'lastName', 'username', 'auth', 'initials'],
  data() {
    return {
    };
  },
  mounted() {
  },
  methods: {
  }
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