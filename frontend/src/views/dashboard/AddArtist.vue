<template>
    <div class="container mt-5">
        <v-card class="p-5">
            <v-card-title> Add Artist</v-card-title>
            <v-card-body>
        <v-form @submit.prevent="submitRegisterForm">
            <v-row>
                <v-col>
                    <v-text-field variant="outlined" v-model="email" label="Email" :rules="emailRules" :error-messages="errors?errors?.email?.length?errors.email[0]:'':''"></v-text-field>
                </v-col>
                <v-col>  
                    <v-text-field  variant="outlined" v-model="password"  type="password" label="Password" :rules="nameRules" :error-messages="errors?errors?.password?.length?errors.password[0]:'':''"></v-text-field>
                </v-col>
    
            </v-row>
            <v-row>
                <v-col>
                    <v-text-field variant="outlined" v-model="first_name" label="First Name" :rules="nameRules" :error-messages="errors?errors?.first_name?.length?errors.first_name[0]:'':''" ></v-text-field>
                </v-col>
                <v-col>  
                    <v-text-field  variant="outlined" v-model="last_name"  label="Last Name" :rules="nameRules" :error-messages="errors?errors?.last_name?.length?errors.last_name[0]:'':''"></v-text-field>
                </v-col>
    
            </v-row>
            <v-row>
                <v-col>
                    <v-text-field variant="outlined" v-model="dob" label="Date of Birth" type="date" :rules="nameRules" :error-messages="errors?errors?.dob?.length?errors.dob[0]:'':''"></v-text-field>
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
                    <v-text-field variant="outlined" v-model="phone"  label="Phone" :rules="nameRules" :error-messages="errors?errors?.phone?.length?errors.phone[0]:'':''"></v-text-field>
                </v-col>
                <v-col>
                    <v-text-field variant="outlined" v-model="address" label="Address" :rules="nameRules" :error-messages="errors?errors?.address?.length?errors.address[0]:'':''"></v-text-field>
                </v-col>
    
            </v-row>
           
            <v-row>
                <v-col>  
                    <v-text-field type="number" min="1900" max="2099" step="1" variant="outlined" v-model="first_release_year"  label="First Release Year" :rules="nameRules" :error-messages="errors?errors?.first_release_year?.length?errors.first_release_year[0]:'':''"></v-text-field>
                </v-col>
                <v-col>
                    <v-text-field type="number" variant="outlined" v-model="no_of_albums_releases" label="No of Albums Released" :rules="nameRules" :error-messages="errors?errors?.no_of_albums_releases?.length?errors.no_of_albums_releases[0]:'':''"></v-text-field>
                </v-col>
                
    
            </v-row>
    <v-btn
      class="me-4"
      type="submit"
    >
      submit
    </v-btn>

  
  </v-form>
</v-card-body>
</v-card>
    </div>
        
</template>
<script>
import * as bulmaToast from 'bulma-toast'
import axios from 'axios'


export default {
    name:'AddArtist',
    data(){
        return {
            email :"",
            password:"",
            gender:'',
            dob:"",
            address:"",
            first_name:"",
            last_name:"",
            phone:"",
            first_release_year:"",
            no_of_albums_releases:"",
            errors:"",
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
        }
    },
    
    methods:{
        submitRegisterForm(){
            const formData = {
                email: this.email,
                password: this.password,
                dob: this.dob,
                first_name: this.first_name,
                first_release_year:this.first_release_year,
                no_of_albums_releases:this.no_of_albums_releases,
                last_name: this.last_name,
                gender: this.gender,
                phone: this.phone,
                address: this.address
            }
            axios.post('/api/create/artist/', formData).then(response=>{
                bulmaToast.toast({ message: 'Successfullt registered',type:'is-success',position: 'bottom-right' })
                this.$router.push('/artist')
                

            }).catch(error=>{
                this.errors = error

            })
        }
    }
}
</script>
