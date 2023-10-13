<template>
    <v-app>
       
     
  
      <v-toolbar app>
        <span class="hidden-sm-and-up">
          <v-toolbar-side-icon @click="sidebar = !sidebar">
          </v-toolbar-side-icon>
        </span>
  
        <v-spacer></v-spacer>
        <v-toolbar-items class="hidden-xs-only">
          <v-btn v-if="getCurrentUser.role_type == 'artist' && getIsAuthenticated"
            flat
          
            :to="'/music'">
          
            Music
          </v-btn>
          <v-btn v-if="(getCurrentUser.role_type == 'super admin' || getCurrentUser.role_type == 'artist manager' || getCurrentUser.is_superuser) && getIsAuthenticated"
            flat
          
            :to="'/artist'">
           
            Artist
          </v-btn>
          <v-btn v-if="(getCurrentUser.role_type == 'super admin' || getCurrentUser.is_superuser)  && getIsAuthenticated"
            flat
          
            :to="'/users'">
            
            Users
          </v-btn>
          <v-btn v-if="!getIsAuthenticated"
            flat
          
            :to="'/login'">
            
            Login 
          </v-btn>
          <v-btn v-if="!getIsAuthenticated"
            flat
          
            :to="'/register'">
          
            Register
          </v-btn>
          <v-btn v-if="getIsAuthenticated"
            flat
          
            @click="logout">
          
            Logout
          </v-btn>
          
        </v-toolbar-items>
      </v-toolbar>
      <v-content>
    <router-view/>
  </v-content>
  </v-app>

</template>
<script>
import axios from 'axios';
import { mapGetters } from 'vuex';
import Navbar from './components/layout/Navbar';

export default {
  name:'App',
  components:{
    Navbar
  },
  data(){
        sidebar: false
    },
    computed:{
        ...mapGetters([
            'getIsAuthenticated',
            'getCurrentUser'
        ])
    },
    methods:{

        async logout(){
            // await axios.post('/api/logout/').then(response=>{
            //     console.log('logged out')
            // }).catch(error=>{
            //     console.log(JSON.stringify(error))
            // })
            axios.defaults.headers.common['Authorization'] = ''
            localStorage.removeItem('token')
            this.$store.commit('removeToken')
            this.$router.push('/')
        }
    },
  beforeCreate(){
    this.$store.commit('initializeStore')
    if(this.$store.state.token){
      axios.defaults.headers.common["Authorization"] = "Bearer " + this.$store.state.token
    }
    else{
      axios.defaults.headers.common["Authorization"] = ""
    }

  }
}
</script>
<style lang="scss">
@import '../node_modules/bulma';
</style>

<style lang="scss">
.container{
  margin-top:2rem;
}
</style>

