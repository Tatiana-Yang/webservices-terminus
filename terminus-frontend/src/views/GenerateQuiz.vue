<template>
  <div>
    <div class="p-5">
      <div class="container bg-pastel p-5 rounded">
        <div class="row">
          <div class="col">
            <h1>Générer un quiz</h1>
          </div>
        </div>
        <hr>
        <div class="row" id="app">
          <div class="col-auto">
            <form>
              <input type="text" class="form-control mb-3" required v-model="nomQuiz" :placeholder="'Mon Quiz #'+
                     random">
              <select class="custom-select mb-3" v-model="themeChoisi">
                <option value="" selected disabled hidden>--Choix du thème--</option>
                <option value="0">Tous les thèmes</option>
                <option v-for="theme in themes" :value="theme.id_tag" :key="theme.id_tag" :style="'background-color: ' + theme.color_tag + '; color: white'">
                  {{ theme.name_tag }}
                </option>
              </select>
              <input type="number" min="0" class="form-control mb-3" required v-model="nbQuestion" placeholder="Nombre de question">
            </form>
          </div>

          <div class="col">
          </div>

          <div class="col-auto text-center">
            <div><button v-on:click="genererQuiz()" class="btn btn-primary mb-3">Générer le quiz</button></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

const defaultForm = {
  difficulty: '',
  id_question: '',
  name_tag:'',
  intitule: ''
};

export default {
  data () {
    return {
      nomQuiz: "",
      defaultForm,
      nbQuestion: '',
      themeChoisi: '',
      quiz: [],
      form: {},
      random:"",
      themes: null
    };
  },
  methods: {
    getTags: function () {
      axios.get("/api/get_tags")
          .then((response) => {
            this.$set(this, "themes", response.data);
            console.log(response.data);
          })
          .catch((errors) => {
            console.log(errors);
            this.$router.push("/terminus");
            this.$root.disconnected = "expired";
          })
    },
    generateRandom : function(){
      return Math.ceil(Math.random()*10000);
    },
    genererQuiz: function (){
      if(this.themeChoisi === ""){
        this.themeChoisi = 0;
      }
      if(this.nbQuestion === ""){
        this.nbQuestion = 0;
      }
      axios.get("/api/generate_quiz/tag="+ this.themeChoisi + "&nb=" + this.nbQuestion)
          .then((response) => {
            this.$set(this, "quiz", response.data);
            this.sendData();
            console.log(response.data);
          })
          .catch((errors) => {
            console.log(errors);
            this.$router.push("/terminus");
            this.$root.disconnected = "expired";
          })
    },
    sendData : function(){
      if(this.nomQuiz === ""){
        this.nomQuiz = "Mon Quiz #" + this.random;
      }
      //enregistrer le quiz et rediriger vers la liste des quiz
      const dataToSave = {id: this.$root.id, nomQuizz: this.nomQuiz, questions: this.quiz}

      axios.post("/api/insert_quiz_generate", dataToSave)
          .then((response) => {
            console.log(response.data);
            this.$router.push("/terminus/my-account");
          })
          .catch((errors) => {
            console.log(errors);
            this.$router.push("/terminus");
            this.$root.disconnected = "expired";
          })
    }
  },
  mounted() {
    this.form = Object.assign({},this.defaultForm);
    this.quiz.push(this.form);
    this.getTags();
    this.random = this.generateRandom();
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped src="../assets/style.css">
</style>
