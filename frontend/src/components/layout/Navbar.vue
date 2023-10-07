<template>
    <nav class="navbar is-dark">
        <div>
            <router-link to="/" class="navbar-items">
                <strong>Artist Management</strong>
                </router-link>
        </div>
        <div class="navbar-menu">
            <div class="navbar-end">
                <div class="mavbar-items">
                    <div class="buttons">
                        <router-link to="/register" class="button is-success"><string>Register</string></router-link>
                        <router-link to="/login" class="button is-light"><string>Login</string></router-link>
                    </div>
                </div>
            </div>
        </div>

    </nav>
</template>

<script>
export default {
    name:'Navbar'
}</script>