<template>
    <v-main>
        <v-container fluid>
            <!-- <HelloWorld/> -->
            <Chat/>
            <!-- <PrijavaTeme/> -->
            <!-- <tojetaforma/> -->
        </v-container>
    </v-main>
</template>

<script>
import Chat from './Chat'
//import PrijavaTeme from './PrijavaTeme'
//import tojetaforma from './forms/Pristup/tojetaforma'
export default {
    name: 'Main',
    components: {
        Chat,
        // PrijavaTeme
        //tojetaforma,
  },
}
</script>