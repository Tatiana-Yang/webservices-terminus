<template>
  <div class="modal fade" id="signUpModal" tabindex="-1" role="dialog" aria-labelledby="signUpModal" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content bg-grey">
        <div class="modal-header">
          <h5 class="modal-title" id="signUpModalTitle">Nouvel utilisateur</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close" v-on:click="reset">
            <span aria-hidden="true" class="bg-grey">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <form>
            <div class="form-group">
              <label for="inputName">Nom</label>
              <input type="text" class="form-control bg-grey" id="inputName" v-model="name">
            </div>
            <div class="form-group">
              <label for="inputPseudo">Pseudo</label>
              <input type="text" class="form-control bg-grey" id="inputPseudo" v-model="pseudo">
            </div>
            <div class="form-group">
              <label for="inputPassword">Mot de passe</label>
              <input type="password" class="form-control bg-grey" id="inputPassword" v-model="password1">
            </div>
            <div class="form-group">
              <label for="inputPasswordCheck">Confirmez votre mot de passe</label>
              <input type="password" class="form-control bg-grey" id="inputPasswordCheck" v-model="password2">
            </div>
            <div class="form-check">
              <input type="checkbox" class="form-check-input" id="checkbox" v-model="checkbox">
              <label class="form-check-label" for="checkbox">Je suis sûr de moi</label>
            </div>
          </form>

          <div class="alert alert-warning mt-2" role="alert" v-if="invalidPassword.length > 0">
            {{ this.invalidPassword }}
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn" :disabled="!checkbox" v-on:click="signUp">S'enregistrer</button>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import {sha256} from "js-sha256";
import axios from "axios";
import $ from "jquery";

export default {
  name: "SignUpModal",
  data() {
    return {
      name: "",
      pseudo: "",
      password1: "",
      password2: "",
      invalidPassword: "",
      checkbox: false
    }
  },
  methods: {
    signUp: function () {
      if(this.pseudo.length === 0 && this.password1.length === 0 && this.password2.length === 0) {
        this.invalidPassword = "Vous n'avez pas rempli tout les champs.";
      } else if(this.password1 !== this.password2) {
        this.invalidPassword = "Les mots de passe doivent être identiques.";
      } else {
        let hash = sha256.create();
        hash.update(this.password1);
        let hashedPassword = hash.hex();
        let data = {
          name: this.name,
          login: this.pseudo,
          pwd: hashedPassword
        }
        axios.post("/api/create_user", data)
            .then((response) => {
              this.invalidPassword = "";
              let stringCookie = JSON.stringify(response.data);
              this.$cookies.set('user', stringCookie);
              $('#signUpModal').modal('hide');
              location.reload();
              console.log(response.data);
            })
            .catch((errors) => {
              console.log(errors);
              this.invalidPassword = "Une erreur s'est produite.";
              this.reset();
            })
      }
    },
    reset: function () {
      this.name = "";
      this.pseudo = "";
      this.password = "";
    }
  }
}
</script>

<style scoped src="../assets/style.css">

</style>