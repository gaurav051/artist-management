import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'
import HomeView from '../views/HomeView.vue'
import Register from '../views/Register.vue'
import Login from '../views/Login.vue'
import UserList from '../views/dashboard/UserList.vue'
import ArtistList from '../views/dashboard/ArtistList.vue'
import AddArtist from '../views/dashboard/AddArtist.vue'
import AddSong from '../views/dashboard/AddSong.vue'
import SongList from '../views/dashboard/SongList.vue'
import AddUser from '../views/dashboard/AddUser.vue'
import Dashboard from '../views/dashboard/Dashboard.vue'
import axios from 'axios'


const routes = [

  {
    path: '/register',
    name: 'register',
    component: Register
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/',
    name: 'dashboard',
    component: Dashboard,
    meta:{
      requireLogin:true
    }
  },
  {
    path: '/users',
    name: 'users',
    component: UserList,
    meta:{
      requireLogin:true
    }
  },
  {
    path: '/artist',
    name: 'artists',
    component: ArtistList,
    meta:{
      requireLogin:true
    }
  },
  {
    path: '/add-artist',
    name: 'add.artists',
    component: AddArtist,
    meta:{
      requireLogin:true
    }
  },
  {
    path: '/add-user',
    name: 'user.add',
    component: AddUser,
    meta:{
      requireLogin:true
    }
  },
  {
    path: '/music/:id',
    name: 'songs',
    component: SongList,
    meta:{
      requireLogin:true
    }
  },
  {
    path: '/add-music/:id',
    name: 'add.song',
    component: AddSong,
    meta:{
      requireLogin:true
    }
  },
  
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next)=>{
  console.log(to);
  if(to.matched.some(record=> record.meta.requireLogin)){
    axios.get('api/user/me').then(data=>{
      console.log(data.data.user)
      store.commit('setUser',data.data.user);
      next();


    }).catch(()=>{
      store.commit('removeToken')
      next('login')
    })


   
  }
  else{
   
    next()
  }
})

export default router
