<template>
    <div class="container">
        <div class="column is-multiline">
            <h1 class="title"> Dashboard</h1>
        </div>
    </div>
</template>
<script>
import { mapGetters } from 'vuex';
export default {
    name:'Dashboard',
    computed:{
        ...mapGetters([
            'getIsAuthenticated',
            'getCurrentUser'
        ])
    },
}
</script>