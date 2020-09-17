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
        initials: "",
        processRoomId1: "",
        processRoomId2: "",
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
        },
        setProcessRoomId1(state, value){
            state.processRoomId1 = value
        },
        setProcessRoomId2(state, value){
            state.processRoomId2 = value
        },
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
        },
        setProcessRoomId1(context, value){
            context.commit('setProcessRoomId1', value)
        },
        setProcessRoomId2(context, value){
            context.commit('setProcessRoomId2', value)
        },
    }
})