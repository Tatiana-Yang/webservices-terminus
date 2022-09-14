<template>
  <div>
    <div class="bg-grey pt-2">
      <div class="d-flex justify-content-between" style="border-bottom: solid 5px black">
        <div class="col p-5 bg-yellow-pastel" v-if="launched == null">
          <h1 class="ml-5 pl-5">{{ quiz.name_quiz }}</h1>
        </div>
        <div class="col-auto p-5 bg-yellow-pastel" v-else>
          <h5 class="mt-3 pl-5">{{ quiz.name_quiz }}</h5>
        </div>
        <div class="col-auto p-5 bg-white text-dark" v-if="launched == null">
          <h2 class="mt-1"><small>Pour rejoindre :</small> <b class="text-danger">{{pin}}</b></h2>
        </div>
        <div class="col p-5 bg-white text-dark" v-else-if="end === 1">
          <h3 class="mt-2">Fin de la partie</h3>
        </div>
        <div class="col p-5 bg-white text-dark" v-else>
          <h3 class="mt-2">{{ question }}</h3>
        </div>
      </div>
      <div class="text-center p-5" v-if="launched == null">
        <button class="col-auto ml-3 btn btn-lg" v-on:click="launch_game" :disabled="pseudos.length === 0">Lancer le quiz</button>
        <div class="container bg-pastel rounded p-4 mt-5 d-flex justify-content-around">
          <div class="alert alert-info mt-2" role="alert" v-if="pseudos.length === 0">
            Aucun joueur présent pour l'instant
          </div>
          <div class="mt-1" v-else>
            <h3 class="col" v-for="pseudo in this.pseudos" :key="pseudo"><span class="badge badge-secondary">{{ pseudo }}</span></h3>
          </div>
        </div>
      </div>
      <div class="text-center p-5" v-else-if="end === 1 && launched != null">
        <div class="container bg-pastel rounded p-4 mt-5 d-flex justify-content-around">
          <div class="alert alert-info mt-2" role="alert" style="width:70%">
            Classement de la partie :
            <div class="mt-1">
              <h3 class="col" v-for="pseudo in this.gameScore" :key="pseudo"><span class="badge badge-secondary">{{ pseudo[0] }}. {{ pseudo[1] }} - {{ pseudo[2] }}</span></h3>
            </div>
          </div>
        </div>
        <div class="container bg-pastel rounded p-4 mt-5 d-flex justify-content-around">
          <button class="btn btn-danger btn-lg" v-on:click="display_score" v-if="displayScore !== 1">Afficher les meilleurs joueurs</button>
          <div class="alert alert-info mt-2" role="alert" style="width:70%" v-if="displayScore === 1">
            TOP 10 :
            <div class="mt-1">
              <h3 class="col" v-for="player in this.topPlayer" :key="player"><span class="badge badge-secondary">{{ player['position'] }}. {{ player['nickname'] }} - {{ player['score'] }}</span></h3>
            </div>
          </div>
        </div>
      </div>
      <div class="text-center bg-pastel" v-else>
        <div class="d-flex justify-content-between p-3" style="height: 10vh">
          <div class="col-auto">
            <div class="bg-red p-3" style="border-radius: 400px; width: 75px; height: 75px">
              <h3 class="mt-1" id="timer">20</h3>
            </div>
          </div>
          <div class="col-auto">
            <button class="btn btn-danger btn-lg" :disabled="timerover" v-on:click="next_question">Question Suivante</button>
          </div>
        </div>
        <underground-generator style="margin-top: -10vh" :undergroundTrail="undergroundTrail" :numero="numero" :stations="stations"/>
      </div>
    </div>
    <div class="position-fixed bottom-0 right-0 p-3" style="z-index: 5; right: 0; bottom: 0;">
      <div class="toast" role="alert" aria-live="assertive" aria-atomic="true">
          <div class="toast-header">
            <strong class="mr-auto">Bonus time !</strong>
            <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div  class="toast-body">
              <p id="public_call"></p>
          </div>
      </div>
    </div>
  </div>

</template>

<script>
import UndergroundGenerator from './components/UndergroundGenerator.vue'
import axios from "axios";
import $ from 'jquery'

export default {
  props: ["quiz"],
  end: null,
  components:{UndergroundGenerator},
  data() {
    return {
      pin: null,
      quizzTitle: "Mon super Quiz",
      pseudos: [],
      launched:null,
      question:null,
      stations: [],
      undergroundTrail:[],
      numero: 0,
      timertick:0,
      timer:null,
      timerover:false,
      end: null,
      gameScore: [],
      topPlayer: null,
      displayScore: 0,
    }
  },
  methods: {
    getQuiz: async function () {
      await axios.get("/api/get_quiz/" + this.quiz.id_quiz)
          .then((response) => {
            let questions = response.data.questions;
            for(let i = 0; i < questions.length; i++) {
              this.undergroundTrail.push(questions[i].question_tag);
            }
            axios.get("/api/get_tags")
                .then((response) => {
                  let routes = response.data;
                  for(let i = 0; i < routes.length; i++) {
                    for(let j = 0; j < this.undergroundTrail.length; j++) {
                      if(routes[i].id_tag === this.undergroundTrail[j]) {
                        this.undergroundTrail[j] = routes[i].color_tag;
                      }
                    }
                  }
                })
                .catch((errors) => {
                  console.log(errors);
                  this.$router.push("/terminus");
                  this.$root.disconnected = "expired";
                })
          })
          .catch((errors) => {
            console.log(errors);
            this.$router.push("/terminus");
            this.$root.disconnected = "expired";
          })
      this.generateStations();
    },
    generateStations: function () {
      this.step = window.innerWidth / (this.undergroundTrail.length + 1);
      let height = Math.floor(window.innerHeight * .8 / 2)
      for(let i = 0; i < this.undergroundTrail.length; i++) {
        this.stations.push([(i + 1) * this.step, height]);
      }
    },
    getPinAndTitle: function () {
        this.$socket.emit("create_game",{"id":this.quiz.id_quiz})
    },

    launch_game: function(){
        this.$socket.emit('launch_game', {"pin": this.pin})
        this.launched = 1
    },
    next_question: function(){
        this.$socket.emit('next_question', {"pin": this.pin})
        clearInterval(this.timer);     
        this.timerover = false;
        this.timertick = 20

    },questiontimer: function(){
      if(this.timertick <= 0){ //Si on a rien envoyé à la fin du timer
        //console.log('here end of timer')
        clearInterval(this.timer);     
        this.timerover = false;
        this.timertick = 20
      }if(this.timertick == 21){
        document.getElementById('public_call').innerHTML =""; //Reset
      }
      document.getElementById("timer").innerHTML = this.timertick;
      this.timertick -=1;
    },
    display_score: function(){
      this.displayScore = 1;
    },
    trigger_bonus:function(){
        $(".toast").toast({
          delay: 20000
        });
        $(".toast").toast('show'); 
    }
  },

  sockets: {
    connect(){
      this.isConnected = true
    },
    disconnect(){
      this.isConnected = false
    },
    message(data){
      console.log(data)
    },
    set_question(data){
      this.question = data['question']
      this.numero += 1;
      clearInterval(this.timer);
      this.timerover = true;
      this.timertick = 20;
      this.timer = setInterval(this.questiontimer,1000);
    },
    set_pin(data){
        this.pin = data
    },
    set_users_pseudo(data){
      this.pseudos = data
      //console.log(this.pseudos)
    },
    bonus_request(data){
      let bonus = " a fait un appel au public"
      if(data['bonus_type'] === 0 ){
        bonus = " a demandé un 50/50"
      }else{
        clearInterval(this.timer)
        this.timer = setInterval(this.questiontimer,1000)
        this.timertick = 40
        document.getElementById('public_call').innerHTML += (data['pseudo'] + bonus);
        this.trigger_bonus()
      }
      //console.log("The player ",data['pseudo'], bonus)
    },
    all_answers_recieved(){
      this.timerover = false;
    },
    game_end(data){
      this.end = data[0];
      this.gameScore = data[1];
      this.topPlayer = data[2];
      clearInterval(this.timer);
    }
  },
  mounted: function() {
      this.getQuiz()
      this.getPinAndTitle()
  },
}
</script>

<style scoped src="../assets/style.css">
</style>
