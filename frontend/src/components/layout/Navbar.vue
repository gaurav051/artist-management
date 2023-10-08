<template>
    <nav class="navbar is-dark">
        <div>
            <router-link to="/" class="navbar-items">
                <strong>Artist Management {{ getIsAuthenticated }}</strong>
                </router-link>
        </div>
        <div class="navbar-menu">
            <div class="navbar-end">
                <div class="navbar-items">
                    <div class="buttons" v-if="!getIsAuthenticated">

                        <router-link to="/register" class="button is-success"><string>Register</string></router-link>
                        <router-link to="/login" class="button is-light"><string>Login</string></router-link>
                    </div>
                    <div class="buttons" v-else>
                        <router-link to="/artist" class="button is-success"><string>Artist</string></router-link>
                        <router-link to="/users" class="button is-success"><string>Users</string></router-link>

<button @click="logout" class="button is-danger"><strong>Logout</strong></button>
</div>
                </div>
            </div>
        </div>

    </nav>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';
export default {
    name:'Navbar',
    computed:{
        ...mapGetters([
            'getIsAuthenticated'
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