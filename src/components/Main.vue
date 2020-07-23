<template>
    <v-main>
        <v-container fluid>
            <!-- <HelloWorld/> -->
            <!-- <Chat/> -->
            <tojetaforma/>
        </v-container>
    </v-main>
</template>

<script>
// import Chat from './Chat'
import tojetaforma from './forms/Pristup/tojetaforma'
//import HelloWorld from './HelloWorld';
export default {
    name: 'Main',
    components: {
        // Chat,
        tojetaforma,
        // HelloWorld,
  },
}
</script>