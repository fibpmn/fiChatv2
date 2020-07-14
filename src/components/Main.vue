<template>
    <v-main>
        <v-container fluid>
            <!-- <HelloWorld/> -->
            <Chat/>
        </v-container>
    </v-main>
</template>

<script>
import Chat from './Chat'
//import HelloWorld from './HelloWorld';
export default {
    name: 'Main',
    components: {
        Chat,
        // HelloWorld,
  },
}
</script>