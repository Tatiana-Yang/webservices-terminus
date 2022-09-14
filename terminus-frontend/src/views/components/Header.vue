<template>
  <div>
    <header role="banner">
      <nav class="navbar navbar-expand-lg fixed-top bg-dark-grey pl-5 pr-5">
        <router-link to="/terminus/home" class="navbar-brand">
          <img src="../../assets/img/logo.png" alt="Terminus" title="Terminus"/>
        </router-link>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo02" aria-controls="navbarTogglerDemo02" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarTogglerDemo02">
          <div class="navbar-nav mr-auto ml-3">
            <router-link to="/terminus/about" type="button" class="btn btn-simple mr-3">À propos</router-link>
          </div>
          <div class="form-inline my-2 my-lg-0">
            <div v-if="$root.id == null">
              <button type="button" class="btn mr-3" data-toggle="modal" data-target="#logInModal">Se connecter</button>
              <button type="button" class="btn" data-toggle="modal" data-target="#signUpModal">S'enregistrer</button>
            </div>
            <div class="dropdown dropleft" v-else>
              <button type="button" class="btn dropdown-toggle" data-toggle="dropdown">
                <b-img :src="this.$root.avatar" class="img-avatar"></b-img>
              </button>
              <div class="dropdown-menu">
                <router-link to="/terminus/my-account" class="dropdown-item" role="button"><i class="fas fa-user mr-2"></i>Mon compte</router-link>
                <a class="dropdown-item" v-on:click="signOut" role="button"><i class="fas fa-power-off mr-2"></i>Se déconnecter</a>
              </div>
            </div>
          </div>
        </div>
      </nav>
    </header>

    <LogInModal/>
    <SignUpModal/>
  </div>
</template>

<script>
import LogInModal from "@/modals/LogInModal";
import SignUpModal from "@/modals/SignUpModal";

export default {
  name: "Header.vue",
  components: {
    LogInModal,
    SignUpModal
  },
  methods: {
    signOut: function () {
      this.$cookies.remove("user");
      location.reload();
    }
  }
}
</script>

<style scoped src="../../assets/style.css">

</style>