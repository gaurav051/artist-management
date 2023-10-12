<template>
    <div class="container">
        <v-data-table
    :headers="headers"
    :items="UserData"
    :sort-by="[{ key: 'id', order: 'asc' }]"
    class="elevation-1"
  >
  <template v-slot:top>
      <v-toolbar
        flat
      >
        <v-toolbar-title>Songs</v-toolbar-title>
        
        <v-divider
          class="mx-4"
          inset
          vertical
        ></v-divider>
        
        <v-spacer></v-spacer>
        <v-btn @click="getCSV(UserData)" v-if="getCurrentUser.role_type == 'artist'"
              color="success"> <v-tooltip
        activator="parent"
        location="start"
      >Download csv</v-tooltip>  <v-icon
        size="large"
        class="me-2"
        
        icon="mdi-download"
      >
        
      </v-icon> </v-btn >
        
              <v-btn @click="showModal" v-if="getCurrentUser.role_type == 'artist'">  <v-tooltip
        activator="parent"
        location="end"
      >Upload csv</v-tooltip><v-icon
        size="large"
        class="me-2"
       
        icon="mdi-upload"
      >
        
      </v-icon></v-btn>
        <router-link :to="{name:'add.song'}" class="button is-success" v-if="getCurrentUser.role_type == 'artist'"> <v-btn
              color="primary"> Add Songs </v-btn></router-link>
        <v-dialog
          v-model="dialog"
          max-width="500px"
        >
       
       
  
          <!-- <template v-slot:activator="{ props }">
            
            <v-btn
              color="primary"
              dark
              class="mb-2"
              v-bind="props"
            >
              Add User
            </v-btn>
          </template> -->
          <v-card>
           

            <v-card-text>
              <v-container>
                <v-form ref="form">
                <v-row>
                  <v-col
                    cols="12"
                    sm="6"
                    md="6"
                  >
                    <v-text-field variant="outlined"
                      v-model="editedItem.title"
                      label="Title"
                      :rules="nameRules"
                      :error-messages="errors?errors?.title?.length?errors.title[0]:'':''"
                   
                    ></v-text-field>
                  </v-col>
                 
                  <v-col
                    cols="12"
                    sm="6"
                    md="6"
                  >
                    <v-text-field variant="outlined"
                      v-model="editedItem.album_name"
                      label="Album Name"
                      :rules="nameRules"
                      :error-messages="errors?errors?.album_name?.length?errors.album_name[0]:'':''"
                    ></v-text-field>
                  </v-col>
                 
                  <v-col
                    cols="12"
                    sm="6"
                    md="6"
                  >
                  <v-select variant="outlined"
                        v-model="editedItem.genre"
                        :rules="nameRules"
                        :items="genreItems"
                        item-title="name"
                        item-value="code"
                        label="Select Genre"
                        :error-messages="errors?errors?.genre?.length?errors.genre[0]:'':''"
                    ></v-select>
                    
                  </v-col>
                  
                 
                 
                  
                </v-row>
            </v-form>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="blue-darken-1"
                variant="text"
                @click="close"
              >
                Cancel
              </v-btn>
              <v-btn
                color="blue-darken-1"
                variant="text"
                @click="save"
              >
                Save
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <v-dialog v-model="dialogDelete" max-width="500px">
          <v-card>
            <v-card-title class="text-h5">Are you sure you want to delete this item?</v-card-title>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue-darken-1" variant="text" @click="closeDelete">Cancel</v-btn>
              <v-btn color="blue-darken-1" variant="text" @click="deleteItemConfirm">OK</v-btn>
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>
    <template v-slot:item.actions="{ item }" v-if="getCurrentUser.role_type == 'artist'">
      <!-- <v-icon
        size="small"
        class="me-2"
        @click="songItem(item)"
        icon="mdi-music"
      >
        
      </v-icon> -->
      <v-icon v-if="getCurrentUser.role_type == 'artist'"
        size="small"
        class="me-2"
        @click="editItem(item)"
        icon="mdi-pencil"
      >
        
      </v-icon>
      <v-icon
        size="small"
        @click="deleteItem(item)"
        icon="mdi-delete"
      >
        
      </v-icon>
    </template>
    <template v-slot:no-data>
      <v-btn
        color="primary"
        @click="initialize"
      >
        Reset
      </v-btn>
    </template>
    </v-data-table>
    <div id="myModal" class="modal" >

      <!-- Modal content -->
      <div class="modal-content">
        <span @click="closeModal" class="close mr-5">&times;</span>
        
        <div class="modal-header">
          
          <h2>Import Csv File  <v-btn class="ml-10" @click="downloadSample">Download sample</v-btn></h2>
        </div>
        
        <div class="modal-body">
          <input type="file" id="UploadFile" ref="file" accept=".csv"/>
          
          <v-btn @click="importCsv()"
                    color="success"> Preview data </v-btn>
                    <v-form v-if="importedData.length>0" ref="tableform">
                      <table :style="'width:90%'" class="mt-5" >
                        <!-- <tr>
                          <th :style="'border:1px solid black;'" v-for="(item,index) in importedHeader" :key="index" >{{ item }}</th>
                        </tr> -->
                        <br/>
                       
                        <tr v-for="(item,index) in importedData" :key="index">
                          <td> <v-text-field  variant="outlined" color="primary"
                      v-model="item.title"
                      label="Title"
                      :rules="nameRules"
                      
                    ></v-text-field></td>
                          <td ><v-text-field class="ml-5" variant="outlined" color="primary"
                      v-model="item.album_name"
                      label="Album Name"
                      :rules="nameRules"
                    ></v-text-field></td>
                          <td><v-select class="ml-5"
                        v-model="item.genre"
                        :rules="nameRules"
                        :items="genreItems"
                        variant="outlined" color="primary"
                        item-title="name"
                        item-value="code"
                        label="Select Genre"
                      
                    ></v-select></td>

                        </tr>
                        
                      </table>

                    </v-form>
        </div>
        <div class="modal-footer" v-if="importedData.length>0">
          <v-btn @click="SubmitCsv()"
                    color="success"> Submit </v-btn>
        </div>
      </div>

      </div>
    </div>
   
    
</template>
<script>
import * as bulmaToast from 'bulma-toast'
import axios from 'axios';
import { mapGetters } from 'vuex';
import { VDataTable } from 'vuetify/labs/VDataTable'
export default {
    name:'UserList',
    computed:{
        ...mapGetters([
            'getIsAuthenticated',
            'getCurrentUser'
        ])
    },
    data: () => ({
      isModalVisible: false, 
      importedData:[],
      importedHeader:[],
      errors:"",
        emailRules: [ 
        v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || 'E-mail must be valid',
        v => !!v || 'This field is required',
      ],
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
      genreArray : ['rnb', 'country', 'classic', 'rock', 'jazz'],

      
           
      dialog: false,
      dialogDelete: false,
      headers: [
       
        { title: 'Title', key: 'title' },
        { title: 'Album Name', key: 'album_name' },
        { title: 'Genre', key: 'genre' },
        
        { title: 'Actions', key: 'actions', sortable: false },
      ],
      editedIndex: -1,
      UserData:[],
      formError : false,
      editedItem: {
        id: 0,
        title: '',
        album_name: '',
        genre:'',
        

      },
      defaultItem: {
        id: 0,
        title: '',
        album_name: '',
        genre:'',
      },
    }),
    components: {
    VDataTable,
  },
  created () {
      this.initialize();
      if(this.getCurrentUser.role_type == 'artist'){
        this.headers = [{ title: 'Title', key: 'title' },
        { title: 'Album Name', key: 'album_name' },
        { title: 'Genre', key: 'genre' },
        { title: 'Actions', key: 'actions', sortable: false }]
      }
      else{
        this.headers = [{ title: 'Title', key: 'title' },
        { title: 'Album Name', key: 'album_name' },
        { title: 'Genre', key: 'genre' }]
      }
    },


    methods: {
      importCsv(){
        let self = this;
        var file = this.$refs.file.files[0]
        // var file = document.getElementById('UploadFile').files[0];
        if (file) {
            const reader = new FileReader();

            reader.onload = function (e) {
                const contents = e.target.result;
                const lines = contents.split("\n");

                // Assuming the first row contains headers
                const headers = lines[0].split(",");
                self.importedHeader =headers;

                const data = [];

                for (let i = 1; i < lines.length; i++) {
                  if (lines[i]!=''){
                    const values = lines[i].split(",");
                    
                    const entry = {};


                    for (let j = 0; j < headers.length; j++) {
                      console.log(headers[j].trim().toLowerCase());
                      if(headers[j].trim().toLowerCase() !='genre'){
                        entry[headers[j].trim().toLowerCase()] = values[j].trim();
                      }
                      else if((self.genreArray.includes(values[j].trim())) && (headers[j].trim().toLowerCase() =='genre')){
                        entry[headers[j].trim().toLowerCase()] = values[j].trim();
                        }
                        else{
                          entry[headers[j].trim().toLowerCase()] = ""; 
                        }
                    }
                    self.importedData.push(entry);
                  }
                }
                // console.log(data);
                // this.importedData = data;
         

                // Display the parsed CSV data
               // csvDataDisplay.textContent = JSON.stringify(data, null, 2);
            };

         reader.readAsText(file);

        }
        this.$refs.file.value = null;
        // console.log(this.importedData);

      },
      showModal() {
        var modal = document.getElementById("myModal");
        modal.style.display = "block";

      },
      async SubmitCsv(){
        let formData = this.importedData;
        
        const {valid}  = await this.$refs.tableform.validate();
            if (!valid) {
              console.log('error');
                return;
                // this.initialize();
                
            }
            else{
              axios.post('/api/song/bulk-create/'+this.$route.params.id+'/', formData)
              .then(response=>{
                console.log(response);
                this.closeModal();
                this.initialize();
              })
              .catch(res=>{
                console.log(res);

              });
             
              console.log(formData);
            }

      },
      closeModal() {
        this.importedData = [];
        var modal = document.getElementById("myModal");
        modal.style.display = "none";
      },
      async downloadSample(){
        await axios.get('api/get/sample-song/').then(response=>{
            var data = response.data;
            var blob = new Blob([data], { type: 'text/csv;charset=utf-8;' });

                var link = document.createElement('a');
                var url = URL.createObjectURL(blob);
                link.setAttribute('href', url);
                link.setAttribute('download', 'artistsample.csv');
                link.style.visibility = 'hidden';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            // this.UserData = response.data.data
        }).catch(error=>{
            console.log(error)
        });
      },
      
     getCSV(jsonData) {
     
      const arr = typeof jsonData !== 'object' ? JSON.parse(jsonData) : jsonData;
    const str = `${Object.keys(arr[0]).map((value) => `${value}`).join(',')}\r\n`;
    const csvContent = arr.reduce((st, next) => {
      st += `${Object.values(next).map((value) => 
        `${value}`).join(',')}\r\n`;
         return st;
      }, str);
    const element = document.createElement('a');
    element.href = `data:text/csv;charset=utf8,${encodeURI(csvContent)}`;
    element.target = '_blank';
    element.download = 'artist.csv';
    element.click();    
},
        async validate () {
        
      },
      async initialize () {
        const id = this.$route.query?.id??""
      if(id!=''){

        await axios.get('api/get/songs-list/'+id).then(response=>{
            console.log(response.data.data);
            this.UserData = response.data.data
        }).catch(error=>{
            console.log(error)
        });
      }
      else{
        await axios.get('api/get/songs/').then(response=>{
            console.log(response.data.data);
            this.UserData = response.data.data
        }).catch(error=>{
            console.log(error)
        });

      }
        


        
      },
      editItem (item) {
        this.editedIndex = this.UserData.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
      },
      songItem(item){
        this.$router.push({
          name:"songs","params":item.id
        })
      },
      deleteItem (item) {
        this.editedIndex = this.UserData.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialogDelete = true
      },
      deleteItemConfirm () {
        this.UserData.splice(this.editedIndex, 1)
        this.closeDelete()
      },
      close () {
        this.dialog = false
        this.errors ="";
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        })
      },
      closeDelete () {
        this.dialogDelete = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        })
      },
      async save () {
        if (this.editedIndex > -1) {
            const {valid}  = await this.$refs.form.validate();
            console.log(valid);
            if (!valid) {
                return;
                // this.initialize();
                
            }
            else{
               
                axios.post('/api/update/song/'+this.editedItem.id+'/', this.editedItem).then(response=>{
                bulmaToast.toast({ message: 'User successfully updated' })
                Object.assign(this.UserData[this.editedIndex], this.editedItem);

                    this.close();
        }).catch(error=>{
            console.log(error)
            this.error = error.response.data.data
        });
                
                
            }
        } else {
          this.UserData.push(this.editedItem)
          this.close();
        }
     
      },
    },
}
</script>