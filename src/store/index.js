import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        auth: false,
        firstName: "",
        lastName: "",
        username: "",
        id: "",
        initials: ""
    },
    mutations: {
        setToTrue(state) {
            state.auth = true;
        },
        setToFalse(state) {
            state.auth = false;
        },
        setFirstName(state, value){
            state.firstName = value
        },
        setLastName(state, value){
            state.lastName = value
        },
        setUsername(state, value){
            state.username = value
        },
        setId(state, value){
            state.id = value
        },
        setInitials(state, value){
            state.initials = value
        }

    },
    actions: {
        setFirstName(context, value){
            context.commit('setFirstName', value)
        },
        setLastName(context, value){
            context.commit('setLastName', value)
        },
        setUsername(context, value){
            context.commit('setUsername', value)
        },
        setId(context, value){
            context.commit('setId', value)
        },
        setInitials(context, value){
            context.commit('setInitials', value)
        }
    }
})