<template>
  <div class="modal fade" id="logInModal" tabindex="-1" role="dialog" aria-labelledby="logInModal" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content bg-grey">
        <div class="modal-header">
          <h5 class="modal-title" id="logInModalTitle">Connexion</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close" v-on:click="reset">
            <span aria-hidden="true" class="bg-grey">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <form>
            <div class="form-group">
              <label for="inputPseudo">Pseudo</label>
              <input type="text" class="form-control bg-grey" id="inputPseudo" v-model="pseudo">
            </div>
            <div class="form-group">
              <label for="inputPassword">Mot de passe</label>
              <input type="password" class="form-control bg-grey" id="inputPassword" v-model="password">
            </div>
          </form>

          <div class="alert alert-danger mt-2" role="alert" v-if="invalid.length > 0">
            {{ this.invalid }}
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn" v-on:click="logIn">Se connecter</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import $ from "jquery";
import {sha256} from "js-sha256";
//import bcrypt from "bcryptjs";

export default {
  name: "LogInModal",
  data() {
    return {
      pseudo: "",
      password: "",
      invalid: ""
    }
  },
  methods: {
    logIn: function () {
      let hash = sha256.create();
      hash.update(this.password);
      let hashedPassword = hash.hex();
      let data = {
        login: this.pseudo,
        pwd: hashedPassword
      }
      axios.post("/api/login", data)
          .then((response) => {
            this.invalid = "";
            let stringCookie = JSON.stringify(response.data);
            this.$cookies.set('user', stringCookie);
            $('#logInModal').modal('hide');
            location.reload();
            console.log(response.data);
          })
          .catch((errors) => {
            console.log(errors);
            this.invalid = "Le pseudo ou le mot de passe est incorrect.";
            this.reset();
          })
    },
    reset: function () {
      this.pseudo = "";
      this.password = "";
    }
  }
}
</script>

<style scoped src="../assets/style.css">

</style>