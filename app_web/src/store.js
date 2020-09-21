import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

const store = new Vuex.Store({
    state: {
        delete: {
            id: 0,
            index: -1
        },
        messages: [],
        is_login: false,
        user_info: {},
    },

    mutations: {
        MESSAGE(state, message) {
            state.messages.push(message);
        },
        FILTER(state, params) {
            state.filter = params;
        },
        DELETE(state, params) {
            state.delete = params;
        },
        RESET(state) {
            state.filter = {};
            state.delete = {
                id: 0,
                index: -1
            };
        },
        RESET_FILTER(state) {
            state.filter = {};
        },
        RESET_DELETE(state) {
            state.delete = {
                id: 0,
                index: -1
            };
        },
        COLLAPSE(state) {
            state.menu_is_collapse = !state.menu_is_collapse
        },
        LOGIN_STATUS(state, status) {
            state.is_login = status
        },
        USER_INFO(state, info) {
            state.user_info = info
        },
        SET_PLATFORM(state, payload) {
            state.platforms = payload;
        },
        SET_PLATFORM_ID(state, payload) {
            state.platform_id = payload;
        }
    },

    actions: {
    }
});

export default store
