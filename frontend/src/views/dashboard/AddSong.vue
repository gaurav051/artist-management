<template>
    <div class="container mt-5">
        <v-card class="p-5">
            <v-card-title> Add Song</v-card-title>
            <v-card-body>
        <v-form @submit.prevent="submitRegisterForm">
            
            <v-row>
                <v-col>
                    <v-text-field variant="outlined" v-model="title" label="Title" :rules="nameRules" :error-messages="errors?errors?.title?.length?errors.title[0]:'':''"></v-text-field>
                </v-col>
                <v-col>  
                    <v-text-field  variant="outlined" v-model="album_name"  label="Album Name" :rules="nameRules" :error-messages="errors?errors?.album_name?.length?errors.album_name[0]:'':''"></v-text-field>
                </v-col>
    
            </v-row>
            <v-row>
              
                <v-col>  
                    <v-select variant="outlined"
                        v-model="genre"
                        :items="genreItems"
                        item-title="name"
                        item-value="code"
                        label="Select Genre"
                        :rules="nameRules" :error-messages="errors?errors?.genre?.length?errors.genre[0]:'':''"
                    ></v-select>
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
            title :"",
            album_name:"",
            genre:"",
            errors:"",
       
        nameRules: [
        v => !!v || 'This field is required'
      ],
            genreItems:[
                    { name: 'R&B', code: 'rnb' },
                    { name: 'Country', code: 'country' },
                    { name: 'Classic', code: 'classic' },
                    { name: 'Rock', code: 'rock' },
                    { name: 'Jazz', code: 'jazz' },
                    ],
        }
    },
    
    methods:{
        submitRegisterForm(){
            const formData = {
                title :this.title,
            album_name:this.album_name,
            genre:this.genre,
            }
            axios.post('/api/create/songs-list/', formData).then(response=>{
                bulmaToast.toast({ message: 'Song Added Successfully' ,type:'is-success',position: 'bottom-right'})
                this.$router.push({
          name:"songs",params:{id:this.$route.params.id}
        })
                

            }).catch(error=>{
                this.errors = error.response.data.data

            })
        }
    }
}
</script>
