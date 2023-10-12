<template>
    <div class="container">
        <div class="columns">
  <div class="column is-8 is-offset-2">

    <v-card>
                <v-card-title> Register</v-card-title>
                
           

           <v-card-body>
            <v-container>
            <v-form @submit.prevent="submitRegisterForm" ref="form">
                <v-row>
                <v-col>
                    <v-text-field variant="outlined" type="email" v-model="email" label="Email" :rules="emailRules" :error-messages="errors?errors?.email?.length?errors.email[0]:'':''"></v-text-field>
                    

               </v-col>
               <v-col>
                    <v-text-field  variant="outlined" v-model="password"  type="password" label="Password" :rules="nameRules" :error-messages="errors?errors?.password?.length?errors.password[0]:'':''"></v-text-field>
                 

               </v-col>
               </v-row>
               <v-row>
                <v-col>
                    <v-text-field variant="outlined" type="text" v-model="first_name" label="First Name" :rules="nameRules" :error-messages="errors?errors?.first_name?.length?errors.first_name[0]:'':''"></v-text-field>
                    

               </v-col>
               <v-col>
                    <v-text-field  variant="outlined" v-model="last_name"  type="text" label="Last Name" :rules="nameRules" :error-messages="errors?errors?.last_name?.length?errors.last_name[0]:'':''"></v-text-field>
                 

               </v-col>
            </v-row>
               <v-row>
                <v-col>
                    <v-text-field variant="outlined" type="date" v-model="dob" label="Date of Birth" :rules="nameRules" :error-messages="errors?errors?.dob?.length?errors.dob[0]:'':''"></v-text-field>
                    

               </v-col>
               <v-col>
                <v-select variant="outlined"
                        v-model="gender"
                        :items="genderItems"
                        item-title="name"
                        item-value="code"
                        label="Select Gender"
                        :rules="nameRules" :error-messages="errors?errors?.gender?.length?errors.gender[0]:'':''"
                    ></v-select>                 

               </v-col>
            </v-row>
               <v-row>
                <v-col>
                    <v-text-field variant="outlined" type="number" v-model="phone" label="Phone" :rules="nameRules" :error-messages="errors?errors?.phone?.length?errors.phone[0]:'':''"></v-text-field>
                    

               </v-col>
               <v-col>
                    <v-text-field  variant="outlined" v-model="address"  type="text" label="Address" :rules="nameRules" :error-messages="errors?errors?.address?.length?errors.address[0]:'':''"></v-text-field>
                 

               </v-col>
                
              
               </v-row>
               <div class="notification is-danger" v-if="errorMsg !=''">
                           
                           <p> {{ errorMsg }}</p>
                          
   
                       </div>
                            <v-btn
                    class="me-4"
                    type="submit"
                    >
                    Register
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
import * as bulmaToast from 'bulma-toast'
import axios from 'axios'


export default {
    name:'Register',
    data(){
        return {
            emailRules: [ 
        v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || 'E-mail must be valid',
        v => !!v || 'This field is required',
      ],
        nameRules: [
        v => !!v || 'This field is required'
      ],
            genderItems:[
                    { name: 'Male', code: 'm' },
                    { name: 'Female', code: 'f' },
                    { name: 'Other', code: 'o' },
                    ],
            email :"",
            password:"",
            dob:"",
            address:"",
            first_name:"",
            last_name:"",
            phone:"",
            gender:"",
            errors:[],
            errorMsg:''
        }
    },
    
    methods:{
        async submitRegisterForm(){
           
            axios.defaults.headers.common["Authorization"] = ""
            localStorage.removeItem('token')
            this.errorMsg = '';
            const {valid}  = await this.$refs.form.validate();
            console.log(valid);
            if (!valid) {
                return;   
            }
      else{
            const formData = {
                email: this.email,
                password: this.password,
                dob: this.dob,
                first_name: this.first_name,
                last_name: this.last_name,
                gender: this.gender,
                phone: this.phone,
                address: this.address
            }
            axios.post('/api/register', formData).then(response=>{
                bulmaToast.toast({ message: 'Successfullt registered',type:'is-success',position: 'bottom-right' })
                this.$router.push('/login')
                

            }).catch(error=>{
                this.errors = error

            })
        }
    }

}
}
</script>
