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
  expand-on-hover
    src="https://images.unsplash.com/photo-1567346953362-1bb30e3c10ed?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1491&q=80"
  >
  <!--    -->
    <!-- <div v-show="auth"> -->
    <v-list>
      <v-list-item-group>
        <v-list-item class="pl-2">
          <v-avatar size="40" color="blue lighten-2">
            <span class="white--text">{{initials}}</span>
          </v-avatar>
          <v-list-item-content class="justify-center white--text ml-3 pt-2 pb-2">
            <v-list-item-title>{{firstName}} {{lastName}}</v-list-item-title>
            <v-list-item-title></v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
      <v-divider color="white"></v-divider>
    </v-list>
    <v-list>
      <v-list-item-group two-line>
        <v-list-item class="pl-2">
          <v-avatar size="40">
            <img src="/Fi.png" />
          </v-avatar>
          <v-list-item-content class="justify-center ml-3 white--text pt-2 pb-2">
            <v-list-item-title>{{"FI"}}</v-list-item-title>
            <v-list-item-title>{{"BOT"}}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-list>
<!-- </div> -->

    <v-divider color="white"></v-divider>
    <v-list-item v-show="auth" class="justify-center ml-5 white--text">
      <v-btn tile text color="white" class="pl-0" to="/startproces">Start Process Instance</v-btn>
    </v-list-item>
    <v-list-item v-show="auth" class="justify-center ml-5 white--text">
      <v-btn tile text color="white" class="pl-0" to="/usertaskform">First User Task Form</v-btn>
    </v-list-item>
    <v-list-item disabled></v-list-item>
    <v-list-item disabled></v-list-item>
    <v-list-item disabled></v-list-item>

    <!-- <div v-show="auth"> -->
    <v-divider color="white"></v-divider>
    <v-list-item class="white--text pl-2">
      <v-list-item-avatar>
        <v-btn color="blue lighten-2" small fab depressed>
          <v-icon color="white">mdi-home</v-icon>
        </v-btn>
      </v-list-item-avatar>
      <v-list-item-content class="pt-0 pb-0">
        <v-btn tile text color="white" class="pl-0" to="/home">IDI DOMA</v-btn>
      </v-list-item-content>
    </v-list-item>
    <v-divider color="white"></v-divider>
    <v-list-item class="white--text pl-2">
      <v-list-item-avatar>
        <v-btn color="blue lighten-2" small fab depressed>
          <v-icon color="white">mdi-account-edit</v-icon>
        </v-btn>
      </v-list-item-avatar>
      <v-list-item-content class="pt-0 pb-0">
        <v-btn tile text color="white" class="pl-0">MOJ PROFIL</v-btn>
      </v-list-item-content>
    </v-list-item>
  <!-- </div> -->

   <!-- <div v-show="!auth"> -->
    <v-divider color="white"></v-divider>
    <v-list-item class="white--text pl-2">
      <v-list-item-avatar>
        <v-btn color="blue lighten-2" small fab depressed>
          <v-icon color="white">mdi-account-plus</v-icon>
        </v-btn>
      </v-list-item-avatar>
      <v-list-item-content class="pt-0 pb-0">
        <v-btn tile text color="white" class="pl-0" to="/register">Registriraj se</v-btn>
      </v-list-item-content>
    </v-list-item>
    <v-divider color="white"></v-divider>
    <v-list-item class="white--text pl-2">
      <v-list-item-avatar>
        <v-btn color="blue lighten-2" small fab depressed>
          <v-icon color="white">mdi-login</v-icon>
        </v-btn>
      </v-list-item-avatar>
      <v-list-item-content class="pt-0 pb-0">
        <v-btn tile text color="white" class="pl-0" to="/login">Logiraj se</v-btn>
      </v-list-item-content>
    </v-list-item>
    <v-divider color="white"></v-divider>
  <!-- </div> -->
    
    <!-- <div v-show="auth" > -->
    <v-divider color="white"></v-divider>
    <v-list-item class="white--text pl-2">
      <v-list-item-avatar>
        <v-btn color="blue lighten-2" small fab depressed>
          <v-icon color="white">mdi-logout</v-icon>
        </v-btn>
      </v-list-item-avatar>
      <v-list-item-content class="pt-0 pb-0">
        <v-btn tile text color="white" class="pl-0" @click="logout">Odlogiraj se</v-btn>
      </v-list-item-content>
    </v-list-item>
    <v-divider color="white"></v-divider>
    <!-- </div> -->

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