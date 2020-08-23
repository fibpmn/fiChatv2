<template>
    <v-card>
        <vue-form-generator :schema="schema" :model="model" :options="formOptions"></vue-form-generator>
        <v-btn>Pošalji</v-btn>
    </v-card>
</template>

<script>
import axios from "axios";

export default {
    name: 'UserTaskForm',
    data() {
        return {
            model: {
            },
            schema: {
            },
            formOptions: { 
            }
        }
    },
    methods: {
        //axios post 
    },
    mounted () {
        //var assignee= "ToniID"
        var key = "PrijavaZavrsnogRada"
        axios.defaults.baseURL = "http://localhost:5000";
        axios.all([
            //axios.get(`/api/task/${assignee}`,{}),
            axios.get(`/api/task/xml/${key}`,{})
        ])
        .then(
          response => {
            this.model = response[0].data.model
            this.schema = response[0].data.schema
          },
          error => {
            console.log(error);
          }
        );
    },
}
</script>