<template>
  <div id="MyAccount">
    <div class="parallax bg-tube" style="border-bottom: solid 5px black">
      <div class="text-content-red p-5">
        <h1 class="display-4 about-title rounded">Mon compte</h1>
      </div>
    </div>

    <div class="bg-white">
      <div class="d-flex justify-content-between">
        <div class="col-auto bg-yellow-pastel p-5">
          <div class="nav flex-column nav-pills" id="v-pills-tab" role="tablist" aria-orientation="vertical">
            <a class="nav-link active" id="v-pills-my-quiz-tab" data-toggle="pill" href="#v-pills-my-quiz" role="tab" aria-controls="v-pills-my-quiz" aria-selected="true">Mes quiz</a>
            <a class="nav-link" id="v-pills-settings-tab" data-toggle="pill" href="#v-pills-settings" role="tab" aria-controls="v-pills-settings" aria-selected="false">Paramètres</a>
          </div>
        </div>

        <div class="col p-5">
          <div class="tab-content" id="v-pills-tabContent">
            <div class="tab-pane fade show active" id="v-pills-my-quiz" role="tabpanel" aria-labelledby="v-pills-my-quiz-tab">
              <div class="d-flex justify-content-between">
                <div class="col-auto"><h2>Mes quiz</h2></div>
                <div class="col-auto">
                  <router-link to="/terminus/quizz/create">
                    <button type="button" class="btn btn-danger">Créer un quiz</button>
                  </router-link>
                  <router-link to="/terminus/quiz/generate_quiz">
                    <button type="button" class="btn btn-danger">Générer un quiz</button>
                  </router-link>
                </div>
              </div>
              <div class="col-auto bg-red m-5 p-3 rounded border-black" style="max-height: 70vh; overflow-y: scroll" v-if="this.quiz.length > 0">
                <div v-for="(quiz, index) in this.quiz" :key="quiz.id_quiz">
                  <hr v-if="index > 0">
                  <div class="d-flex justify-content-around">
                    <div class="col">
                      <h5>{{ quiz.name_quiz }}</h5>
                    </div>
                    <div class="col-auto">
                      <router-link :to="{ name: 'QuizzUpdate', params: { id: quiz.id_quiz }}">
                        <button type="button" class="btn btn-play mr-3"><i class="fas fa-pencil-alt"></i></button>
                      </router-link>
                      <router-link :to="{ name: 'CreateGame', params: { quiz }}">
                        <button type="button" class="btn btn-play"><i class="fas fa-play"></i></button>
                      </router-link>
                    </div>
                  </div>
                </div>
              </div>

              <div v-else class="m-5">
                <div class="alert alert-info" role="alert">Vous n'avez pas encore créé de quiz.</div>
              </div>
            </div>

            <div class="tab-pane fade" id="v-pills-settings" role="tabpanel" aria-labelledby="v-pills-settings-tab">
              <div class="d-flex justify-content-center">
                <div class="col-4 mr-3 text-center">
                  <b-img :src="this.$root.avatar" :alt="this.$root.username" class="img-avatar"/>
                  <h2 class="mt-3">{{ this.$root.username }}</h2>
                </div>
                <div class="col-auto bg-pastel rounded border-black p-4">
                  <div class="d-flex justify-content-around p-5">
                    <div class="col-auto mr-5">
                      <form>
                        <div class="form-group">
                          <label for="usernameInput">Nom</label>
                          <input type="text" class="form-control" id="usernameInput" :placeholder="this.$root.username" readonly>
                        </div>
                        <div class="form-group">
                          <label for="pseudoInput">Pseudo</label>
                          <input type="text" class="form-control" id="pseudoInput" v-model="pseudo">
                        </div>
                        <hr>
                        <button type="button" class="btn mr-3" v-on:click="reset" :disabled="show">Annuler</button>
                        <button type="button" class="btn btn-danger" :disabled="show" v-on:click="updateAccount">Sauvegarder</button>
                      </form>
                    </div>
                    <div class="col-auto">
                      <div class="nav flex-column nav-pills text-left" role="tablist" aria-orientation="vertical">
                        <label>Changer mon mot de passe</label>
                        <button type="button" class="btn w-75" data-toggle="modal" data-target="#changePasswordModal">Changer</button>
                        <hr>
                        <label>Supprimer mon compte</label>
                        <button type="button" class="btn btn-danger w-75" v-on:click="deleteAccount">Supprimer</button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <ChangePassword/>
  </div>
</template>

<script>
import ChangePassword from "@/modals/ChangePassword";
import axios from "axios";

export default {
  name: "MyAccount",
  components: {
    ChangePassword
  },
  data() {
    return {
      quiz: [],
      avatar: "",
      pseudo: this.$root.pseudo,
      oldPassword: "",
      newPassword1: "",
      newPassword2: "",
      show: true
    }
  },
  methods: {
    getQuiz: function () {
      axios.get("/api/get_user_quiz/" + this.$root.id.toString())
          .then((response) => {
            this.$set(this, "quiz", response.data);
            console.log(response.data);
          })
          .catch((errors) => {
            console.log(errors);
            this.$router.push("/terminus");
            this.$root.disconnected = "expired";
          })
    },
    updateAccount: function () {
      let data = {
        id: this.$root.id,
        name: "",
        login: this.pseudo,
        pwd: ""
      }
      axios.post("/api/user/update", data)
          .then((response) => {
            let stringCookie = JSON.stringify(response.data);
            this.$cookies.set('user', stringCookie);
            console.log(response.data);
          })
          .catch((errors) => {
            console.log(errors);
            this.reset();
          })
    },
    deleteAccount: function () {
      axios.get("/api/user/delete/" + this.$root.id.toString())
          .then((response) => {
            this.$cookies.remove('user');
            location.reload();
            console.log(response.data);
          })
          .catch((errors) => {
            console.log(errors);
            this.reset();
          })
    },
    reset: function () {
      this.pseudo = this.$root.pseudo;
      this.show = true;
    }
  },
  mounted() {
    this.getQuiz();
  },
  watch: {
    pseudo: function () {
      this.show = false;
    }
  }
}
</script>

<style scoped src="../assets/style.css">
</style>