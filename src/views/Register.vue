<template>
    <v-row>
        <v-col class="col-3">
        </v-col>
        <v-col class="col-6">
            <v-sheet tile class="text-right mt-10">
                <v-form @submit.prevent="register">
                    <v-text-field
                        v-model="email"
                        required
                        label="E-mail"
                        clearable
                        class="ml-4 mr-4"
                    >
                    </v-text-field>
                    <v-text-field
                        v-model="firstName"
                        required
                        label="Ime"
                        clearable
                        class="ml-4 mr-4"
                    >
                    </v-text-field>
                    <v-text-field
                        v-model="lastName"
                        required
                        label="Prezime"
                        clearable
                        class="ml-4 mr-4"
                    >
                    </v-text-field>
                    <v-text-field
                        v-model="password"
                        required
                        label="Lozinka"
                        clearable
                        class="ml-4 mr-4"
                    >
                    </v-text-field>
                    <v-btn tile depressed color="primary" class="text-right" @click="register">
                        Registriraj se
                    </v-btn>
                </v-form>
            </v-sheet>
        </v-col>
        <v-col class="col-3">
        </v-col>
    </v-row>
</template>

<script>
import { Auth } from "@/services";

export default {
    name: "Register",
    data() {
        return {
            email: "",
            firstName: "",
            lastName: "",
            password: "",
        }
    },
    methods: {
        async register() {
            var data = {
                email: this.email,
                firstName: this.firstName,
                lastName: this.lastName,
                password: this.password
            }
            console.log(data)
            await Auth.RegisterUser(data);
        }
    }
}
</script>

<style lang="scss">

</style>