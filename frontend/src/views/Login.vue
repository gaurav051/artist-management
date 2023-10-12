<template>
    <div class="container mt-10" >
        <div class="columns">
  <div class="column is-8 is-offset-2">
        
            <v-card>
                <v-card-title> Login</v-card-title>
                
           

           <v-card-body>
            <v-container>
            <v-form @submit.prevent="submitForm" ref="form">
                <v-row>
                <v-col>
                    <v-text-field variant="outlined" type="email" v-model="email" label="Email" :rules="emailRules" :error-messages="errors?errors?.email?.length?errors.email[0]:'':''"></v-text-field>
                    

               </v-col>
               </v-row>
               <v-row>
                <v-col>
                    <v-text-field  variant="outlined" v-model="password"  type="password" label="Password" :rules="nameRules" :error-messages="errors?errors?.password?.length?errors.password[0]:'':''"></v-text-field>
                 

               </v-col>
              
               </v-row>
               <div class="notification is-danger" v-if="errorMsg !=''">
                           
                           <p> {{ errorMsg }}</p>
                          
   
                       </div>
                            <v-btn
                    class="me-4"
                    type="submit"
                    >
                    Login
                    </v-btn>

              
                   </v-form>
                   </v-container>
                   </v-card-body>
       </v-card>
    </div>   
</div>
               
            </div>
       
    
        
</template>
<script>
import axios from 'axios'
import * as bulmaToast from 'bulma-toast'


export default {
    name:'Login',
    data(){
        return {
            emailRules: [ 
        v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || 'E-mail must be valid',
        v => !!v || 'This field is required',
      ],
        nameRules: [
        v => !!v || 'This field is required'
      ],
            email :"",
            password:"",
            errors:[],
            errorMsg:''
        }
    },
    methods:{
        async submitForm(){
            this.errorMsg = '';
            const {valid}  = await this.$refs.form.validate();
            console.log(valid);
            if (!valid) {
                return;   
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
                bulmaToast.toast({ message: 'Login success',type:'is-success',position: 'bottom-right' })
                this.$router.push('/')

            }).catch(error=>{
                this.errorMsg = "Invalid username or password";
            })
        }
    }
    }

}
</script>
