<template>
    <div class="container">
        <div class="columns">
  <div class="column is-4 is-offset-4">
        
                <h1 class="title"> Login
                </h1>
                <form @submit.prevent="submitForm">
                    <div
                class="notification is-danger"
            
                v-if="errorMsg != ''"
              >
                {{ errorMsg }}
              </div>
                 
                    
                    <div class="field">
                        <label>Email</label>
                        <div class="control">
                            <input type="email" name="email" class="input" v-model="email"/>
                        </div>
                        <div class="notification is-danger" v-if="errors['email']">
                           
                           <p> {{ errors["email"] }}</p>
                          
   
                       </div>
                        
                   
                    </div>
               
               
                    <div class="field">
                        <label>Password</label>
                        <div class="control">
                            <input type="password" name="password" class="input" v-model="password"/>
                        </div>
                      
                    </div>
                    <!-- <span
                  v-if="errors['username'] && username == ''"
                  class="text-danger"
                >
                  {{ errors["username"] }}
                </span> -->
                    <div class="notification is-danger" v-if="errors['password']">
                           
                        <p> {{ errors["password"] }}</p>
                       

                    </div>
                    <div class="field">
                       
                       <div class="control">
                           <button class="button is=success">Login</button>
                       </div>
                   </div>

                    
                </form>
            </div>
        </div>
    </div>
        
</template>
<script>
import axios from 'axios'


export default {
    name:'Login',
    data(){
        return {
            email :"",
            password:"",
            errors:[],
            errorMsg:''
        }
    },
    methods:{
        submitForm(){
            this.errors = [];
      this.errorMsg = "";
      if (this.password == "" || this.email == "") {
        if (this.password == "" && this.email == "") {
          this.errors.password = "This field is required";
          this.errors.email = "This field is required";
        } else if (this.email == "") {
          this.errors.email = "This field is required";
        } else if (this.password == "") {
          this.errors.password = "This field is required";
        }
      }
      else{
            axios.defaults.headers.common["Authorization"] = ""
            localStorage.removeItem('token')
            const formData = {
                email: this.email,
                password: this.password
            }
            axios.post('/api/get-token', formData).then(response=>{
                const token = response.data.token
                this.$store.commit('setToken', token)
                axios.defaults.headers.common['Authorization'] = 'Bearer '+ token
                localStorage.setItem('token', token)
                this.$router.push('/')

            }).catch(error=>{
                this.errorMsg = "Invalid username or password";

            })
        }
    }
    }

}
</script>
