import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import Vue3EasyDataTable from 'vue3-easy-data-table';
import '@mdi/font/css/materialdesignicons.css';
import 'vuetify/styles'
import {
    VDataTable,
    VDataTableServer,
    VDataTableVirtual,
  } from "vuetify/labs/VDataTable";
import { createVuetify } from 'vuetify'
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";

import { fa } from "vuetify/iconsets/fa";
import { aliases, mdi } from "vuetify/lib/iconsets/mdi";
import {VueCsvImportPlugin} from "vue-csv-import";
// make sure to also import the coresponding css
import "@mdi/font/css/materialdesignicons.css"; // Ensure you are using css-loader


axios.defaults.baseURL='http://127.0.0.1:8000/'


  const vuetify = createVuetify({
    VDataTable,
    VDataTableServer,
    VDataTableVirtual,
    icons: {
      defaultSet: "mdi",
      aliases,
      sets: {
        mdi,
        fa,
      },
    },
    components,
    directives,
  });

createApp(App).use(store).use(router,axios).use(vuetify).use(VueCsvImportPlugin).mount('#app')
