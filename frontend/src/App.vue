<template>
  <div>
  <Navbar/>
  <router-view/>
</div>

</template>
<script>
import axios from 'axios';
import Navbar from './components/layout/Navbar';

export default {
  name:'App',
  components:{
    Navbar
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
