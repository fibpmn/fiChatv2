<template>
    <v-navigation-drawer app bottom mini-variant right background expand-on-hover fixed clipped color="blue lighten-5">
        <v-list>
            <v-list-item>
                <img class="pa-3" src="/Logo.png">
            </v-list-item>
            <v-divider></v-divider>
             <v-list-item two-line>
              <v-list-item-avatar>
                <img :src="'https://randomuser.me/api/portraits/men/81.jpg'" />
              </v-list-item-avatar>
              <v-list-item-content class="justify-center">
                <v-list-item-title> {{"User"}} {{"Name"}}</v-list-item-title>
                <v-list-item-subtitle>Online</v-list-item-subtitle>
              </v-list-item-content>
              <v-btn small fab depressed>
                  <v-icon>mdi-account-edit</v-icon>
                  <!-- EDIT PROFILE -->
              </v-btn>
            </v-list-item>

             <v-divider></v-divider>
            <v-list-item two-line>
              <v-list-item-avatar>
                <img src="/Fi.png"/>
              </v-list-item-avatar>
              <v-list-item-content class="justify-center">
                <v-list-item-title> {{"Fi"}} </v-list-item-title>
                <v-list-item-subtitle>Always Online</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            <v-divider></v-divider>
            <v-list-item>
                <v-treeview hoverable :items="items">OPEN</v-treeview>
            </v-list-item>
            <v-list-item></v-list-item>
            <v-list-item></v-list-item>
        </v-list>
    </v-navigation-drawer>
</template>

<script>
export default {
    name: 'Drawer',
    //photo: null,
    data: () => ({
        items: [{
            id: 1,
            name: "OPEN",
            children: [
                {id: 4, name: "Prvi"},
                {id: 5, name: "Drugi"},
                {id: 6, name: "Treci"}
            ],
        },
        {
            id: 2,
            name: "HISTORY",
            children: [
                {id: 7, name: "Prvi"},
                {id: 8, name: "Drugi"},
                {id: 9, name: "Treci"}
            ],
        },
        {
            id: 3,
            name: "DM?",
            children: [
                {id: 10, name: "Prvi"},
                {id: 11, name: "Drugi"},
                {id: 12, name: "Treci"}
            ],
        }
        ]
})
}
</script>

<style lang="scss">
.nesto {
    color: #BFCFFF !important;
}.v-navigation-drawer {
    z-index: 9999 !important;
}
</style>