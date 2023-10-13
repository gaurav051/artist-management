import { createStore } from 'vuex'

export default createStore({
  state: {
    isLoading: false,
    isAuthenticated:false,
    token: '',
    user:{}
  },
  getters: {
    getIsAuthenticated: (state) =>{
      return state.isAuthenticated
    },
     getCurrentUser: (state)=>{
      return state.user
    },

  },
  mutations: {
    initializeStore(state){
      if(localStorage.getItem('token')){
        state.token = localStorage.getItem('token');
        state.isAuthenticated = true
      }
      else{
        state.token=''
        state.isAuthenticated = false
      }
    },
    setIsLoading(state, status){
      state.isLoading = status
    },
    setToken(state, token){
      state.token = token
      state.isAuthenticated = true
    },
    setUser(state, user){
      state.user = user
    },
    removeToken(state){
      state.token = ''
      state.isAuthenticated = false

    }
  },
  actions: {
  },
  modules: {
  }
})
