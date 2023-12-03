import {createStore} from 'vuex'

export default createStore({
    state: {
        username: '',
        token: '', // Добавляем хранение токена
    },
    getters: {
        isAuthenticated: (state) => !!state.token, // Проверяем, аутентифицирован ли пользователь
    },
    mutations: {
        setUsername(state, username) {
            state.username = username;
        },
        setToken(state, token) {
            state.token = token;
        },
        clearTokens(state) {
            state.username = '';
            state.token = '';
        },
    },
    actions: {},
    modules: {}
})
