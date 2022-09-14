<template>
  <div class="modal fade" id="changePasswordModal" tabindex="-1" role="dialog" aria-labelledby="changePasswordModal" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content bg-grey">
        <div class="modal-header">
          <h5 class="modal-title" id="changePasswordModalTitle">Changement de mot de passe</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close" v-on:click="reset">
            <span aria-hidden="true" class="bg-grey">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <form>
            <div class="form-group">
              <label for="inputOldPassword">Ancien mot de passe</label>
              <input type="password" class="form-control bg-grey" id="inputOldPassword" v-model="oldPassword">
            </div>
            <div class="form-group">
              <label for="inputNewPassword1">Nouveau mot de passe</label>
              <input type="password" class="form-control bg-grey" id="inputNewPassword1" v-model="newPassword1">
            </div>
            <div class="form-group">
              <label for="inputNewPassword2">Confirmez votre nouveau mot de passe</label>
              <input type="password" class="form-control bg-grey" id="inputNewPassword2" v-model="newPassword2">
            </div>
            <div class="form-check">
              <input type="checkbox" class="form-check-input" id="checkbox" v-model="checkbox">
              <label class="form-check-label" for="checkbox">Je suis sûr de moi</label>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <div class="alert alert-success" role="alert" v-if="updateDone">
            Mot de passe mis à jour avec succès
          </div>
          <div class="alert alert-danger mt-2" role="alert" v-if="invalidPassword.length > 0">
            {{ this.invalidPassword }}
          </div>
          <button type="button" class="btn" :disabled="!checkbox" v-on:click="updatePassword">Enregistrer</button>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import {sha256} from "js-sha256";
import axios from "axios";

export default {
  name: "SignUpModal",
  data() {
    return {
      oldPassword: "",
      newPassword1: "",
      newPassword2: "",
      invalidPassword: "",
      updateDone: false,
      checkbox: false
    }
  },
  methods: {
    updatePassword: function () {
      let hash = sha256.create();
      hash.update(this.oldPassword);
      let hashedPassword = hash.hex();
      let data = {
        login: this.$root.pseudo,
        pwd: hashedPassword
      }
      axios.post("/api/login", data)
          .then((response) => {
            this.invalidPassword = "";
            if(this.newPassword1.length === 0 && this.newPassword2.length === 0) {
              this.invalidPassword = "Vous n'avez pas rempli tout les champs.";
            } else if(this.newPassword1 !== this.newPassword2) {
              this.invalidPassword = "Les mots de passe doivent être identiques.";
            } else {
              let hash = sha256.create();
              hash.update(this.newPassword1);
              let hashedPassword = hash.hex();
              let data = {
                id: this.$root.id,
                name: "",
                login: "",
                pwd: hashedPassword
              }
              axios.post("/api/user/update", data)
                  .then((response) => {
                    this.reset();
                    this.updateDone = true;
                    console.log(response.data);
                  })
                  .catch((errors) => {
                    console.log(errors);
                    this.reset();
                    this.invalidPassword = "Une erreur s'est produite.";
                  })
            console.log(response.data);
          }})
          .catch((errors) => {
            console.log(errors);
            this.reset();
            this.invalidPassword = "L'ancien mot de passe est incorrect.";
          })
    },
    reset: function () {
      this.oldPassword = "";
      this.newPassword1 = "";
      this.newPassword2 = "";
      this.invalidPassword = "";
      this.updateDone = false;
      this.checkbox = false;
    }
  }
}
</script>

<style scoped src="../assets/style.css">

</style>