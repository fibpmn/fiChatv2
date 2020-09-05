<template>
  <v-app-bar app clipped-right dense flat color="#060606">
    <img height="45px" width="auto" src="/Logo.png" />
  </v-app-bar>
</template>

<script>
export default {
  name: "Header",
  props: ["firstName", "lastName", "username", "id", "auth"],
  data() {
    return {};
  },
  methods: {
    logout() {
      localStorage.removeItem("usertoken");
      this.$store.commit("setToFalse");
      this.$store.dispatch("setFirstName", "Anonymous");
      this.$store.dispatch("setLastName", "");
      this.$store.dispatch("setUsername", "Anonymous");
      this.$store.dispatch("setId", "");
      this.$store.dispatch("setInitials", "A");
    },
  },
  mounted() {},
};
</script>

<style lang="scss">
// .v-toolbar__content{
//     box-shadow: 0px 2px #90CAF9 !important;
// }
</style>
