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
        <v-toolbar-title>Users</v-toolbar-title>
        
        <v-divider
          class="mx-4"
          inset
          vertical
        ></v-divider>
        
        <v-spacer></v-spacer>
        <router-link to="/add-user" class="button is-success"> <v-btn
              color="primary"> Add User </v-btn></router-link>
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
                      v-model="editedItem.email"
                      label="Email"
                      :rules="emailRules"
                    ></v-text-field>
                  </v-col>
                  <v-col
                    cols="12"
                    sm="6"
                    md="6"
                  >
                  <v-select variant="outlined"
                        v-model="editedItem.role_type"
                        :rules="nameRules"
                        :items="roleItems"
                        item-title="name"
                        item-value="code"
                        label="Select Role"
                    ></v-select>
                    <!-- <v-text-field variant="outlined"
                      v-model="editedItem.role_type"
                      label="Role"
                      :rules="nameRules"
                    ></v-text-field> -->
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
      <v-icon
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
    </div>
</template>
<script>
import * as bulmaToast from 'bulma-toast'
import axios from 'axios';
import { VDataTable } from 'vuetify/labs/VDataTable'
export default {
    name:'UserList',
    data: () => ({
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
            roleItems:[
                    { name: 'Super Admin', code: 'super admin' },
                    { name: 'Artist Manager', code: 'artist manager' },
                    { name: 'Artist', code: 'artist' },

            ],
      dialog: false,
      dialogDelete: false,
      headers: [
       
        { title: 'Email', key: 'email' },
        { title: 'Role', key: 'role_type' },
        { title: 'First Name', key: 'first_name' },
        { title: 'Last Name', key: 'last_name' },
        
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
        role_type: '',
        gender: '',
        phone:'',
        address:''
      },
      defaultItem: {
        id: 0,
        first_name: '',
        last_name: '',
        email:'',
        role_type: '',
        gender: '',
        phone:'',
        address:''
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

        await axios.get('api/get/user-list/').then(response=>{
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
                axios.post('/api/update/user/'+this.editedItem.id+'/', this.editedItem).then(response=>{
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