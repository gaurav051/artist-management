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
        <v-toolbar-title>Artists</v-toolbar-title>
        
        <v-divider
          class="mx-4"
          inset
          vertical
        ></v-divider>
        
        
        <v-spacer></v-spacer>
        <!-- <v-icon
        size="large"
        class="me-2"
        @click="getCSV(UserData)"
        icon="mdi-excel"
      >
        
      </v-icon> -->
        <v-btn @click="getCSV(UserData)"
              color="success"> <v-tooltip
        activator="parent"
        location="start"
      >Download csv</v-tooltip>  <v-icon
        size="large"
        class="me-2"
        
        icon="mdi-download"
      >
        
      </v-icon> </v-btn>
        
              <v-btn @click="showModal">  <v-tooltip
        activator="parent"
        location="end"
      >Upload csv</v-tooltip><v-icon
        size="large"
        class="me-2"
       
        icon="mdi-upload"
      >
        
      </v-icon></v-btn>
      <router-link to="/add-artist" class="button is-success" v-if="getCurrentUser.role_type == 'artist manager'"><v-btn
              color="primary"> Add Artist</v-btn></router-link>
              
              <!-- <v-btn @click="importCsv()"
              color="success"> Submit </v-btn> -->
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
                <!-- <pre id="csvData"></pre> -->
                <v-form ref="form">
                <v-row>
                  <v-col
                    cols="12"
                    sm="6"
                    md="6"
                  >
                    <v-text-field variant="outlined"
                      v-model="editedItem.email"
                      label="Email"
                      :rules="emailRules"
                      disabled
                    ></v-text-field>
                  </v-col>
                 
                  <v-col
                    cols="12"
                    sm="6"
                    md="6"
                  >
                    <v-text-field variant="outlined"
                      v-model="editedItem.first_name"
                      label="First Name"
                      :rules="nameRules"
                    ></v-text-field>
                  </v-col>
                  <v-col
                    cols="12"
                    sm="6"
                    md="6"
                  >
                    <v-text-field variant="outlined"
                      v-model="editedItem.last_name"
                      :rules="nameRules"
                      label="Last Name"
                    ></v-text-field>
                  </v-col>
                  <v-col
                    cols="12"
                    sm="6"
                    md="6"
                  >
                  <v-select variant="outlined"
                        v-model="editedItem.gender"
                        :rules="nameRules"
                        :items="genderItems"
                        item-title="name"
                        item-value="code"
                        label="Select Gender"
                    ></v-select>
                    
                  </v-col>
                  <v-col
                    cols="12"
                    sm="6"
                    md="6"
                  >
                    <v-text-field variant="outlined"
                      v-model="editedItem.phone"
                      :rules="nameRules"
                      label="Phone"
                    ></v-text-field>
                  </v-col>
                  <v-col
                    cols="12"
                    sm="6"
                    md="6"
                  >
                    <v-text-field variant="outlined"
                      v-model="editedItem.address"
                      :rules="nameRules"
                      label="Address"
                    ></v-text-field>
                  </v-col>
                  <v-col
                    cols="12"
                    sm="6"
                    md="6"
                  >
                  
                  <v-text-field variant="outlined"
                      v-model="editedItem.first_release_year"
                      :rules="nameRules"
                      label="First Release Year"
                      type="number"
                    ></v-text-field>
                  </v-col>
                  <v-col
                    cols="12"
                    sm="6"
                    md="6"
                  >
                  
                  <v-text-field variant="outlined"
                      v-model="editedItem.no_of_albums_releases"
                      :rules="nameRules"
                      label="No of Albums releases"
                      type="number"
                    ></v-text-field>
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
  

    <template v-slot:item.actions="{ item }">
      <v-btn  @click="songItem(item)">
        <v-tooltip
        activator="parent"
        location="start"
      >Songs</v-tooltip>
      <v-icon
        size="small"
        class="me-2"
       
        icon="mdi-music"
      > 
        
      </v-icon>
    </v-btn>
      <v-btn  @click="editItem(item) " v-if="getCurrentUser.role_type == 'artist manager'">
        <v-tooltip
        activator="parent"
        location="bottom"
      >Edit</v-tooltip>
      <v-icon 
        size="small"
        class="me-2"
        icon="mdi-pencil"
      >
     
        
      </v-icon>
    </v-btn>
  <v-btn @click="deleteItem(item)">
    <v-tooltip
        activator="parent"
        location="end"
      >Delete</v-tooltip>
      <v-icon
        size="small"
        
        icon="mdi-delete"
      >
    
      </v-icon>
      </v-btn>
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
          <input type="file" id="UploadFile" accept=".csv"/>
          
          <v-btn @click="importCsv()"
                    color="success"> Preview data </v-btn>
                    <div v-if="importedData.length>0">
                      <table :style="'width:90%'" class="mt-5" >
                        <tr>
                          <th :style="'border:1px solid black;'" v-for="(item,index) in importedHeader" :key="index" >{{ item }}</th>
                        </tr>
                        <tr v-for="(item,index) in importedData" :key="index" >
                          <td :style="'border:1px solid black;'">{{item.name}}</td>
                          <td :style="'border:1px solid black;'">{{item.age}}</td>
                          <td :style="'border:1px solid black;'">{{item.grade}}</td>

                        </tr>
                        
                      </table>

                    </div>
        </div>
        <div class="modal-footer">
          <v-btn @click="SubmitCsv()"
                    color="success"> Submit </v-btn>
        </div>
      </div>

</div>
    </div>
    
</template>
<script>

import { mapGetters } from 'vuex';
import * as bulmaToast from 'bulma-toast'
import axios from 'axios';
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
           
      dialog: false,
      dialogDelete: false,
      headers: [
       
        { title: 'Name', key: 'name' },
        { title: 'Date of Birth', key: 'dob' },
        { title: 'Address', key: 'address' },
        { title: 'No of Album Released', key: 'no_of_albums_releases' },
        { title: 'First Release Year', key: 'first_release_year' },
        
        { title: 'Actions', key: 'actions', sortable: false },
      ],
      editedIndex: -1,
      UserData:[],
      formError : false,
      editedItem: {
        id: 0,
        first_name: '',
        last_name: '',
        email:'',
        gender: '',
        phone:'',
        address:'',
        no_of_albums_releases:'',
        first_release_year:''

      },
      defaultItem: {
        id: 0,
        first_name: '',
        last_name: '',
        email:'',
        gender: '',
        phone:'',
        address:'',
        no_of_albums_releases:'',
        first_release_year:''
      },
    }),
    components: {
    VDataTable,
  },
  created () {
      this.initialize()
    },


    methods: {
        async validate () {
        
      },
      async initialize () {

        await axios.get('api/get/artist/list/').then(response=>{
            console.log(response.data.data);
            this.UserData = response.data.data
        }).catch(error=>{
            console.log(error)
        });
        


        
      },
      editItem (item) {
        this.editedIndex = this.UserData.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
      },
      songItem(item){
        this.$router.push({
          name:"songs",params:{id:item.id}
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
      },SubmitCsv(){
        let formData = this.importedData;

      },
      importCsv(){
        let self = this;
        var file = document.getElementById('UploadFile').files[0];
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
                        entry[headers[j].trim().toLowerCase()] = values[j].trim();
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
        // console.log(this.importedData);

      },
      showModal() {
        var modal = document.getElementById("myModal");
        modal.style.display = "block";

      },
      closeModal() {
        this.importedData = [];
        var modal = document.getElementById("myModal");
        modal.style.display = "none";
      },
      async downloadSample(){
        await axios.get('api/get/sample-artist/').then(response=>{
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
      async save () {
        if (this.editedIndex > -1) {
            const {valid}  = await this.$refs.form.validate();
            console.log(valid);
            if (!valid) {
                return;
                // this.initialize();
                
            }
            else{
                axios.post('/api/update/artist/'+this.editedItem.id+'/', this.editedItem).then(response=>{
                bulmaToast.toast({ message: 'User successfully updated' })
                Object.assign(this.UserData[this.editedIndex], this.editedItem);

                    this.close();
        }).catch(error=>{
            console.log(error)
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
<style>
/* The Modal (background) */
.modal {
  display: none; /* Hidden by default */
  position: fixed; /* Stay in place */
  z-index: 1; /* Sit on top */
  padding-top: 100px; /* Location of the box */
  left: 0;
  top: 0;
  width: 100%; /* Full width */
  height: 100%; /* Full height */
  overflow: auto; /* Enable scroll if needed */
  background-color: rgb(0,0,0); /* Fallback color */
  background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
}

/* Modal Content */
.modal-content {
  position: relative;
  background-color: #fefefe;
  margin: auto;
  padding: 0;
  border: 1px solid #888;
  width: 80%;
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2),0 6px 20px 0 rgba(0,0,0,0.19);
  -webkit-animation-name: animatetop;
  -webkit-animation-duration: 0.4s;
  animation-name: animatetop;
  animation-duration: 0.4s
}

/* Add Animation */
@-webkit-keyframes animatetop {
  from {top:-300px; opacity:0} 
  to {top:0; opacity:1}
}

@keyframes animatetop {
  from {top:-300px; opacity:0}
  to {top:0; opacity:1}
}

/* The Close Button */
.close {
  color: #000;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: #000;
  text-decoration: none;
  cursor: pointer;
}

.modal-header {
  padding: 20px 16px;
  background-color: rgb(238, 238, 238);
  color: rgb(0, 0, 0);
}

.modal-body {padding: 10px 16px;}

.modal-footer {
  padding: 10px 16px;
  background-color: rgb(238, 238, 238);
  color: white;
}
</style>