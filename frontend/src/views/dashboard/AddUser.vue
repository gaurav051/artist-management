<template>
    <div class="container mt-5">
        <v-card class="p-5">
            <v-card-title> Add User</v-card-title>
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
                    <v-text-field variant="outlined" v-model="first_name" label="First Name" :rules="nameRules" :error-messages="errors?errors?.first_name?.length?errors.first_name[0]:'':''"></v-text-field>
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
                    ></v-select>
                </v-col>
    
            </v-row>
            <v-row>
                <v-col>
                    <v-select variant="outlined"
                        v-model="role_type"
                        :items="roleItems"
                        item-title="name"
                        item-value="code"
                        label="Select Role"
                    ></v-select>
                </v-col>
                <v-col>  
                    <v-text-field variant="outlined" v-model="phone"  label="Phone" :rules="nameRules" :error-messages="errors?errors?.phone?.length?errors.phone[0]:'':''"></v-text-field>
                </v-col>
    
            </v-row>
           
            <v-row>
                <v-col>
                    <v-text-field variant="outlined" v-model="address" label="Address"  :rules="nameRules" :error-messages="errors?errors?.address?.length?errors.address[0]:'':''"></v-text-field>
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
        <!-- <div class="columns">
  <div class="column is-6 is-offset-2">
        
                <h1 class="title"> Add User
                </h1>
                <form  @submit.prevent="submitRegisterForm">
                    <div class="columns">
            <div class="column">
                    
                    <div class="field">
                        <label>Email</label>
                        <div class="control">
                            <input type="email" name="email" class="input" v-model="email"/>
                        </div>
                   
                    </div>
                </div>
                <div class="column">
                    <div class="field">
                        <label>Password</label>
                        <div class="control">
                            <input type="password" name="password" class="input" v-model="password"/>
                        </div>
                    </div>
                </div>
                </div>
                <div class="columns">
            <div class="column">
                    <div class="field">
                        <label>First Name</label>
                        <div class="control">
                            <input type="text" name="first_name" class="input" v-model="first_name"/>
                        </div>
                    </div>
                </div>
                    <div class="column">
                    <div class="field">
                        <label>Last Name</label>
                        <div class="control">
                            <input type="text" name="last_name" class="input" v-model="last_name"/>
                        </div>
                    </div>
                </div>
            </div>
                <div class="columns">
            
                <div class="column">
                      
                      <label>Role</label>
                      <br/>
                          <div class="select">
  
                            <select v-model="role_type">
                                  <option value="super admin">Super Admin</option>
                                  <option value="artist manager">Artist Manager</option>
                                  <option value="artist">Artist</option>
                              </select>
                          </div>
                       
                      </div>
              
                    <div class="column">
                      
                      <label>Gender</label>
                      <br/>
                          <div class="select">
  
                              <select v-model="gender">
                                  <option value="m">Male</option>
                                  <option value="f">Female</option>
                                  <option value="o">Other</option>
                              </select>
                          </div>
                       
                      </div>
                      <div class="column">
                    <div class="field">
                        <label>Date of Birth</label>
                        <div class="control">
                            <input type="date" name="dob" class="input" v-model="dob"/>
                        </div>
                    </div>
                </div>
                     
                
                   
            </div>
           
            <div class="columns">
                <div class="column">
                    <div class="field">
                        <label>Phone</label>
                        <div class="control">
                            <input type="number" name="phone" class="input" v-model="phone"/>
                        </div>
                    </div>
                </div>
         
               
          
                    <div class="column">
                    <div class="field">
                        <label>Address</label>
                        <div class="control">
                            <input type="text" name="address" class="input" v-model="address"/>
                        </div>
                    </div>
                </div>
                
              

                </div>
                    <div class="field">
                       
                        <div class="control">
                            <button class="button is=success">Submit</button>
                        </div>
                    </div>
                    
                </form>
            </div>
        </div> -->
    </div>
        
</template>
<script>
import * as bulmaToast from 'bulma-toast'
import axios from 'axios'


export default {
    name:'AddUser',
    data(){
        return {
            emailRules: [ 
        v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || 'E-mail must be valid',
        v => !!v || 'This field is required',
      ],
        nameRules: [
        v => !!v || 'This field is required'
      ],
            errors:"",
            email :"",
            password:"",
            gender:'',
            dob:"",
            address:"",
            first_name:"",
            last_name:"",
            phone:"",
            role_type:"",
            errorMsg:'',
            genderItems:[
                    { name: 'Male', code: 'm' },
                    { name: 'Female', code: 'f' },
                    { name: 'Other', code: 'o' },
                    ],
            roleItems:[
                    { name: 'Super Admin', code: 'super admin' },
                    { name: 'Artist Manager', code: 'artist manager' },
                    { name: 'Artist', code: 'artist' },

            ]
        }
    },
    
    methods:{
        submitRegisterForm(){
            const formData = {
                email: this.email,
                password: this.password,
                dob: this.dob,
                first_name: this.first_name,
                last_name: this.last_name,
                gender: this.gender,
                role_type: this.role_type,
                phone: this.phone,
                address: this.address
            }
            axios.post('/api/add/user/', formData).then(response=>{
                bulmaToast.toast({ message: 'Successfullt registered' })
                this.$router.push('/users')
                

            }).catch(error=>{
                console.log(error)
                this.errors = error.response.data.data

            })
        }
    }
}
</script>
