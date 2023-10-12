<template>
<div></div>
    <!-- <nav class="navbar is-dark" role="navigation" aria-label="main navigation">
        <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
    </a>
    
        <div id="navbarBasicExample" class="navbar-menu mt-1 ml-2 mr-2">
            <div v-if="getIsAuthenticated" class="navbar-start">
            <router-link  to="/artist" class="navbar-item button is-success" v-if="getCurrentUser.role_type == 'super admin' || getCurrentUser.role_type == 'artist manager'"><string>Artist</string></router-link>
                        <router-link to="/users" class="navbar-item button is-success ml-2" v-if="getCurrentUser.role_type == 'super admin'"><string>Users</string></router-link>
                        <router-link to="/music" class="navbar-item button is-success ml-2" v-if="getCurrentUser.role_type == 'artist'"><string>Songs</string></router-link>
                    </div>
            <div class="navbar-end">
                <div class="navbar-item">
                    <div class="buttons" v-if="!getIsAuthenticated">
                 

                        <router-link to="/register" class="button is-success"><string>Register</string></router-link>
                        <router-link to="/login" class="button is-light"><string>Login</string></router-link>
                    </div>
                    <div class="buttons" v-else>
                       
                    <button @click="logout" class="button is-danger"><strong>Logout</strong></button>
                    </div>
                </div>
            </div>
        </div>

    </nav> -->
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';
export default {
    name:'Navbar',
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
    }
}</script>