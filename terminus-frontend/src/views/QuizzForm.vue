<template>
  <div>
    <div class="p-5">
      <div class="container bg-pastel p-5 rounded">
        <div class="row">
          <div class="col">
            <h1 v-if="this.id == null">Création du quiz</h1>
            <h1 v-else>Modification du quiz</h1>
          </div>
          <div class="col">
            <nav aria-label="Question" class="row">
              <h2 class="mr-4 mt-2">Questions</h2>
              <ul class="pagination pagination-lg">
                <li class="page-item" v-on:click="updateForm(numeroQuestion)">
                  <button class="page-link" href="#" aria-label="Previous" :disabled="numeroQuestion < 1"><span aria-hidden="true">&laquo;</span></button>
                </li>
                <li class="page-item" role="button" v-for="index in this.quiz.length" :key="index"
                    v-on:click="updateForm(index)" v-bind:class="{ 'active': index-1 === numeroQuestion}">
                  <span class="page-link" v-if="index-1 >= numeroQuestion - 1 && index-1 <= numeroQuestion + 1">{{ index }}</span>
                </li>
                <li class="page-item" v-on:click="updateForm(numeroQuestion + 2)">
                  <button class="page-link" href="#" aria-label="Next" :disabled="numeroQuestion >= this.quiz.length - 1"><span aria-hidden="true">&raquo;</span></button>
                </li>
              </ul>
            </nav>
          </div>
        </div>
        <hr>
        <div class="row">
          <div class="col-auto">
            <form>
              <input type="text" class="form-control mb-3" required v-model="nomQuizz" placeholder="Nom du quiz">
              <textarea class="form-control mb-3" required rows="3" v-model="form.intitule" placeholder="Intitulé de la question"></textarea>
              <select class="custom-select mb-3" v-model="form.themeChoisi">
                <option v-for="theme in themes" :value="theme.id_tag" :key="theme.id_tag" :style="'background-color: ' + theme.color_tag + '; color: white'">
                  {{ theme.name_tag }}
                </option>
              </select>
              <select class="custom-select" v-model="form.typeChoisi" v-on:change="resetAnswers()" >
                <option v-for="type in typesQuestion" :value="type" :key="type.id_type_question" >
                  {{ type.name_type_question }}
                </option>
              </select>
            </form>
          </div>

          <div class="col">
            <div class="row" v-if="form.typeChoisi">
              <div class="col-12 pt-2">
                <div class="input-group">
                  <div class="input-group-prepend">
                    <div class="input-group-text">
                      <input value="0" v-if="form.typeChoisi.name_type_question === TYPE_QUESTION.MULTIPLE" type="checkbox" v-model="form.checkedAnswers">
                      <input value="0" name="UniqueAnswer" v-if="form.typeChoisi.name_type_question === TYPE_QUESTION.UNIQUE || form.typeChoisi.name_type_question === TYPE_QUESTION.VRAIFAUX" type="radio" v-model="form.checkedAnswers">
                    </div>
                  </div>
                  <input type="text" class="form-control" :disabled="form.typeChoisi.name_type_question === TYPE_QUESTION.VRAIFAUX" v-model="form.answers['0']">
                </div>
              </div>
              <div class="col-12 pt-2">
                <div class="input-group">
                  <div class="input-group-prepend">
                    <div class="input-group-text">
                      <input value="1" v-if="form.typeChoisi.name_type_question === TYPE_QUESTION.MULTIPLE" type="checkbox" v-model="form.checkedAnswers">
                      <input value="1" name="UniqueAnswer" v-if="form.typeChoisi.name_type_question === TYPE_QUESTION.UNIQUE || form.typeChoisi.name_type_question === TYPE_QUESTION.VRAIFAUX" type="radio" v-model="form.checkedAnswers">
                    </div>
                  </div>
                  <input type="text" class="form-control" :disabled="form.typeChoisi.name_type_question === TYPE_QUESTION.VRAIFAUX" v-model="form.answers['1']" >
                </div>
              </div>
              <div v-if="form.typeChoisi.name_type_question !== TYPE_QUESTION.VRAIFAUX" class="col-12 pt-2">
                <div class="input-group ">
                  <div class="input-group-prepend">
                    <div class="input-group-text">
                      <input value="2" v-if="form.typeChoisi.name_type_question === TYPE_QUESTION.MULTIPLE" type="checkbox" v-model="form.checkedAnswers">
                      <input value="2" name="UniqueAnswer" v-if="form.typeChoisi.name_type_question === TYPE_QUESTION.UNIQUE" type="radio" v-model="form.checkedAnswers">
                    </div>
                  </div>
                  <input type="text" class="form-control" v-model="form.answers['2']" >
                </div>
              </div>
              <div v-if="form.typeChoisi.name_type_question !== TYPE_QUESTION.VRAIFAUX" class="col-12 pt-2">
                <div class="input-group">
                  <div class="input-group-prepend">
                    <div class="input-group-text">
                      <input value="3" v-if="form.typeChoisi.name_type_question === TYPE_QUESTION.MULTIPLE" type="checkbox" v-model="form.checkedAnswers">
                      <input value="3" name="UniqueAnswer" v-if="form.typeChoisi.name_type_question === TYPE_QUESTION.UNIQUE" type="radio" v-model="form.checkedAnswers">
                    </div>
                  </div>
                  <input type="text" class="form-control" v-model="form.answers['3']">
                </div>
              </div>
            </div>
          </div>

          <div class="col-auto text-center">
            <div><button v-on:click="validerQuizz()" class="btn btn-primary mb-3">Enregistrer le quiz</button></div>
            <div><button class="btn btn-primary mb-3" v-on:click="ajouterQuestion()">Ajouter une question</button></div>
            <div><button v-if="this.quiz.length > 1" class="btn btn-danger" v-on:click="supprimerQuestion()">Supprimer la question</button></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

const TYPE_QUESTION = {
  MULTIPLE: 'Question à choix multiple',
  UNIQUE: 'Question à choix unique',
  VRAIFAUX: 'Vrai / Faux'
};


const defaultForm = {
    intitule: '',
    checkedAnswers: [],
    answers:[],
    typeChoisi: '',
    themeChoisi: '',
    idQuestion: '',
};

export default {
    props:["id"],
    data () {
        return {
            TYPE_QUESTION,
            nomQuizz: null,
            defaultForm,
            erreurs: [],
            numeroQuestion: 0,
            quiz: [],
            typesQuestion:null,
            form: {},
            themes: null
        };  
    },
    methods: {
        getTypesQuestion: function (){
            axios.get("/api/get_types_question")
            .then((response) => {
                this.$set(this, "typesQuestion", response.data);
                console.log(response.data);
            })
            .catch((errors) => {
                console.log(errors);
                this.$router.push("/terminus");
                this.$root.disconnected = "expired";
            })
        },

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
        resetAnswers: function () {
            this.form.answers = new Array(4);
            this.form.checkedAnswers= [];

            if(this.form.typeChoisi.name_type_question === TYPE_QUESTION.VRAIFAUX){
                this.form.answers = ["Vrai","Faux"];
            }
        },
        validerQuizz: function () {
            // vérifier le quiz complet
            
            this.erreurs = [];
            let i = 0

            if(this.nomQuizz == null || this.nomQuizz === '') {
                this.erreurs.push('Titre du quiz');
            }

            if(this.quiz.length < 3){
               this.erreurs.push('3 questions minimum par quiz');
            }

            this.quiz.forEach(quiz => {
                
                if(!this.checkQuizzValidity(quiz)){
                    this.erreurs.push('Question ' + i)
                }
            })

            if(this.erreurs.length === 0){
                //enregistrer le quiz et rediriger vers la liste des quiz 
                this.quiz.forEach(questionForm => {
                  if(typeof(questionForm.checkedAnswers) == "string" || typeof(questionForm.checkedAnswers) == "number"){
                    questionForm.checkedAnswers = [questionForm.checkedAnswers]
                  }
                })
                if(this.id){
                  const dataToSave = {id_quiz: this.id, nomQuizz: this.nomQuizz, questions: this.quiz}
                  axios.post("/api/update_quiz", dataToSave)
                  .then((response) => {
                      //TODO REDIRECT VERS LA LISTE QUI N'EXISTE PAS (ENCORE)
                      console.log(response.data);
                  })
                  .catch((errors) => {
                      console.log(errors);
                      this.$router.push("/terminus");
                      this.$root.disconnected = "expired";
                  }) 
                }
                else{
                  const dataToSave = {id: this.$root.id, nomQuizz: this.nomQuizz, questions: this.quiz}
                  axios.post("/api/insert_quiz", dataToSave)
                  .then((response) => {
                      this.$router.push("/terminus/my-account");
                      console.log("ici : ",response.data);
                  })
                  .catch((errors) => {
                      console.log(errors);
                      this.$router.push("/terminus");
                      this.$root.disconnected = "expired";
                  }) 
                }
                
            }
            else {
                //TODO Modale indiquant les erreurs
                console.log(this.erreurs)     
            }
        },

        checkQuizzValidity(quiz){
            if(quiz.intitule == null || quiz.intitule == ''){
                return false;
            }

            if(quiz.checkedAnswers.length == 0){
                return false;
            }

            if(quiz.answers.includes(null) || quiz.answers.includes('')){
                return false;
            }

            if(quiz.themeChoisi == '' || quiz.themeChoisi == null){
                return false;
            }

            return true
        },
        ajouterQuestion: function () {
            this.quiz.push(Object.assign({},this.defaultForm));
        },
        supprimerQuestion: function () {
            this.quiz.splice(this.numeroQuestion, 1);
            if(this.numeroQuestion === this.quiz.length) {
            this.numeroQuestion -= 1;
            }
            this.form = this.quiz.at(this.numeroQuestion);
        },
        updateForm: function (index) {
            this.numeroQuestion = index - 1;
            this.form = this.quiz.at(this.numeroQuestion);
        },

        setForm: function() {
            axios.get("/api/get_quiz/" + this.id)
            .then((response) => {
                this.$set(this, "nomQuizz", response.data.name_quiz);
                response.data.questions.forEach(question => {
                    let tmp = Object.assign({},this.defaultForm)
                    let answers = []
                    let validAnswers = []
                    tmp.intitule = question.question_name
                    tmp.themeChoisi = question.question_tag
                    tmp.typeChoisi = question.question_type
                    tmp.idQuestion = question.id_question
                    question.answers.forEach(answer => {
                        answers.push(answer.answer_name)
                        if(answer.is_correct){
                            validAnswers.push(answer.answer_num)
                        }
                    })
                    
                    console.log(question.question_type.name_type_question)
                    if(question.question_type.name_type_question === TYPE_QUESTION.VRAIFAUX || question.question_type.name_type_question === TYPE_QUESTION.UNIQUE){
                      validAnswers = validAnswers[0]
                    }
                    tmp.checkedAnswers = validAnswers
                    tmp.answers = answers
                    this.quiz.push(tmp)
                })
                this.updateForm(1)
                console.log(this.form)
                
            })
            .catch((errors) => {
                console.log(errors);
                this.$router.push("/terminus");
                this.$root.disconnected = "expired";
            })
        }
    },
    mounted() {
        if(this.id){
            this.setForm()
        }
        else{
            this.form = Object.assign({},this.defaultForm)
            this.quiz.push(this.form)
        
        }
        this.getTags()
        this.getTypesQuestion()
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped src="../assets/style.css">
</style>
