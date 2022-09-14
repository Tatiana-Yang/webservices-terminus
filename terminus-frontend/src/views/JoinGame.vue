<template>
  <div>
    <div class="bg-grey" v-if="play.question == null">

      <!-- JOIN A GAME -->
      <div v-if="join.pseudos === null">
        <div class="row justify-content-center bg-pastel" style="border-bottom: solid 5px black">
          <div class="col-auto pt-5">
            <h2 class="">Rejoindre une partie</h2>
          </div>
          <div class="col-3" style="margin-left: -120px">
            <svg width="100%" height="100%">
              <image id="TubeWagon" xlink:href="../assets/img/tube_wagon.png" x="0" y="90" width="75"  height="auto"/>
            </svg>
          </div>
        </div>
        <!-- INPUT PSEUDO -->
        <div v-if="join.gamePass === null || join.pseudoIncorrect === true" class="d-flex justify-content-center p-5">
          <div class="col-auto text-center">
            <div class="d-flex">
              <div class="col text-left">
                <label for="PseudoInput">Pseudo</label>
                <input id="PseudoInput" type="text" class="form-control" v-bind:class="{ 'is-invalid': join.pseudoIncorrect }"
                       placeholder="Pseudo" v-model="join.pseudo" style="width: max-content">
              </div>
              <button class="col ml-2 btn" v-on:click="validatePseudo">Valider mon pseudo</button>
            </div>
            <div class="mt-2 alert alert-danger" role="alert" v-if="join.pseudoIncorrect">Erreur : pseudo déjà existant.</div>
          </div>
        </div>
        <!-- INPUT CODE PIN -->
        <div v-else class="row justify-content-center p-5">
          <div class="col-auto text-center">
            <div class="d-flex">
              <div class="col text-left">
                <label for="PinInput">Code PIN</label>
                <input id="PinInput" type="text" class="form-control" v-bind:class="{ 'is-invalid': join.pinIncorrect }"
                       placeholder="Code" v-model="join.gamePass" style="width: max-content">
              </div>
              <button class="col ml-2 btn" v-on:click="validatePass">Rejoindre la partie</button>
            </div>
            <div class="mt-2 alert alert-danger" role="alert" v-if="join.pinIncorrect">Erreur : pin incorrect.</div>
          </div>
        </div>
      </div>

      <!-- EN ATTENTE DU LANCEMENT DE PARTIE -->
      <div v-else-if="play.status === 0" >
        <div class="parallax bg-tube" style="border-bottom: solid 5px black">
          <div class="text-content-red p-5">
            <h1 class="display-4 about-title rounded text-dark">Embarquement</h1>
          </div>
        </div>
        <div class="p-5">
          <div class="d-flex justify-content-around">
            <div v-for="pseudo in join.pseudos" :key="pseudo" class="col-auto">
              <h2><span class="badge badge-secondary">{{ pseudo }}</span></h2>
            </div>
          </div>
        </div>
        <div class="d-flex justify-content-center">
          <div class="spinner-grow text-white" role="status" style="width: 3rem; height: 3rem;">
            <span class="sr-only">Loading...</span>
          </div>
        </div>
      </div>

      <!-- JOUEUR PASSE À LA QUESTION SUIVANTE -->
      <div v-else-if="play.status === 1 && play.question == null && play.end === 0" class="text-white">
        <div class="row justify-content-center bg-pastel" style="border-bottom: solid 5px black">
          <div class="col-auto pt-5">
            <h2 class="">Le contrôleur vous autorise à passer à la station suivante</h2>
          </div>
          <div class="col-3" style="margin-left: -120px">
            <svg width="100%" height="100%">
              <image id="TubeWagon" xlink:href="../assets/img/tube_wagon.png" x="0" y="90" width="75"  height="auto"/>
            </svg>
          </div>
        </div>
        <div class="d-flex justify-content-center mt-5">
          <div class="spinner-grow text-white" role="status" style="width: 3rem; height: 3rem;">
            <span class="sr-only">Loading...</span>
          </div>
        </div>
      </div>

      <!-- JOUEUR A GAGNÉ / CLASSEMENT / TOP 10 -->
      <div v-else-if="play.end === 1" class="text-white">
        <div class="row justify-content-center bg-yellow-pastel" style="border-bottom: solid 5px black">
          <div class="col-auto pt-5">
            <h2 v-if="play.status === 1">Félicitations, vous avez rejoint le TERMINUS</h2>
            <h2 v-else>Vous aurez plus de chance la prochaine fois</h2>
          </div>
          <div class="col-3" style="margin-left: -120px">
            <svg width="100%" height="100%">
              <image id="TubeWagon" xlink:href="../assets/img/tube_wagon.png" x="0" y="90" width="75"  height="auto"/>
            </svg>
          </div>
        </div>
        <!-- CLASSEMENT -->
        <div class="container bg-pastel p-4 mt-5" style="border-top-left-radius: 10px; border-top-right-radius: 10px">
          <h3>Classement de la partie :</h3>
          <div class="d-flex justify-content-around">
            <div class="col">
              <div v-for="pseudo in this.score.gameScore" :key="pseudo">
                <h5 v-if="pseudo[1] === join.pseudo"><span class="badge bg-yellow-pastel mr-3 mb-2">
                  {{ pseudo[0] }}. {{ pseudo[1] }} - {{ pseudo[2] }}
                </span></h5>
                <h5 v-else><span class="badge badge-secondary mr-3 mb-2">
                  {{ pseudo[0] }}. {{ pseudo[1] }} - {{ pseudo[2] }}
                </span></h5>
              </div>
            </div>
          </div>
        </div>
        <!-- TOP 10 -->
        <div class="container bg-red-pastel p-4" style="border-bottom-left-radius: 10px; border-bottom-right-radius: 10px">
          <button class="btn btn-danger btn-lg" v-on:click="display_score" v-if="score.displayScore !== 1">Afficher les meilleurs joueurs</button>
          <div v-if="score.displayScore === 1">
            <h3>TOP 10 :</h3>
            <div class="d-flex justify-content-around">
              <div class="col">
                <h5><span class="badge badge-secondary mr-3 mb-2" v-for="player in this.score.topPlayer" :key="player">
                  {{ player['position'] }}. {{ player['nickname'] }} - {{ player['score'] }}
                </span></h5>
              </div>
            </div>
          </div>
        </div>

        <div class="row justify-content-center mt-5">
          <div class="col-auto">
            <button type="button" class="btn" v-on:click="reloadPage">Rejoindre une autre partie</button>
          </div>
          <div class="col-auto">
            <router-link to="/terminus/home" type="button" class="btn">Retourner à l'accueil</router-link>
          </div>
        </div>
      </div>

      <!-- JOUEUR ÉLIMINÉ -->
      <div v-else-if="play.status === -1 && play.end === 0" class="text-white">
        <div class="row justify-content-center bg-red-pastel" style="border-bottom: solid 5px black">
          <div class="col-auto pt-5">
            <h2 class="">Le contrôleur vous a éjecté. Vous êtes éliminé</h2>
          </div>
          <div class="col-3" style="margin-left: -120px">
            <svg width="100%" height="100%">
              <image id="TubeWagon" xlink:href="../assets/img/tube_wagon.png" x="0" y="90" width="75"  height="auto"/>
            </svg>
          </div>
        </div>
        <div class="d-flex justify-content-center mt-5">
          <div class="spinner-grow text-white" role="status" style="width: 3rem; height: 3rem;">
            <span class="sr-only">Loading...</span>
          </div>
        </div>
      </div>
    </div>

    <!-- QUESTION -->
    <div v-else-if="play.status === 1 || play.status === -1 || play.status === 2">
      <div class="row justify-content-center bg-yellow-pastel" style="border-bottom: solid 5px black">
        <div class="col-auto pt-5">
          <h2>{{ play.question }}</h2>
        </div>
        <div class="col-3" style="margin-left: -120px">
          <svg width="100%" height="100%">
            <image id="TubeWagon" xlink:href="../assets/img/tube_wagon.png" x="0" y="90" width="75"  height="auto"/>
          </svg>
        </div>
        <div class="col-auto">
          <div class="bg-red mt-4 p-3 text-center" style="border-radius: 400px; width: 75px; height: 75px">
            <h3 class="mt-1" id="timer">20</h3>
          </div>
        </div>
      </div>

      <div id="wait" style="display:none">
        <h3><span class="badge badge-secondary m-3">Attente du vote du public</span></h3>
      </div>

      <div class="container mt-4">
        <div class="d-flex justify-content-center">
          <div class="col-auto mr-1">
            <button class="btn" id="5050" :disabled="(play.fifty_available === false) || (play.fifty_used === true)" v-on:click="request_bonus(0)">50/50</button>
          </div>
          <div class="col-auto ml-1" v-if="join.pseudos.length > 1">
            <button class="btn" id="public" :disabled="(play.public_call === false) || (play.public_used === true)" v-on:click="request_bonus(1)">Appel au public</button>
          </div>
        </div>

        <div class="bg-pastel rounded mt-4 p-3">
          <div v-if="play.num_ans > 1 && this.play.bonus_activated === false">
            <div v-for="answer in play.answers" :key='answer' class="m-3">
              <div class="row">
                <input type="checkbox" v-model="play.checked_ans" :value ="answer"/>&nbsp;{{ answer }}
                <div v-if="play.print_public === 1 && play.public_ans[answer] > 0" class="ml-5">
                  <span class="badge badge-secondary">{{ play.public_ans[answer] }} vote(s)</span>
                </div>
              </div>
            </div>
            <button :disabled="play.status === -1" class="col-auto mt-2 btn btn-danger" v-on:click="sendAnswer(play.correctness)">Valider</button>
          </div>

          <div v-else-if="play.num_ans > 1 && (play.bonus_activated === true)">
            <div v-for="answer in play.answers" :key='answer' class="m-3">
              <div class="row">
                <input type="checkbox" v-model="play.checked_ans" :value ="answer"/>&nbsp;{{ answer }}
                <div v-if="play.print_public === 1 && play.public_ans[answer] > 0" class="ml-5">
                  <span class="badge badge-secondary">{{ play.public_ans[answer] }} vote(s)</span>
                </div>
              </div>
            </div>
            <button :disabled="play.status === -1" class="col-auto mt-2 btn btn-danger" v-on:click="sendAnswer(answer)">Valider</button>
          </div>

          <div v-else class="d-flex justify-content-around">
            <div v-for="answer in play.answers" :key='answer' class="col m-3 text-center">
              <button :disabled="play.status === -1" class="btn btn-danger" v-on:click="sendAnswer(answer)">
                {{ answer }}
              </button>
              <div v-if="play.print_public === 1 && play.public_ans[answer] > 0"><span class="badge badge-secondary m-2">{{ play.public_ans[answer] }} vote(s)</span></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      socket: {
        isConnected: false,
        message: "",
      },
      join:{
        pseudo: null,
        gamePass: null,
        pseudoIncorrect: false,
        pinIncorrect: false,
        pseudos: null,
      },

      play:{
        question: null,
        answers:null,
        correctness: null,
        end : 0,
        timer:null,
        timertick:null,
        checked_ans:[],
        num_ans:null,
        public_used:false,
        fifty_available:true,
        fifty_used:false,
        bonus_activated:false,
        public_ans:{},
        print_public:0,
        wait_ans:false,
        status : 0 //Status 0 : on est connecté
                   //Status -1 : on est éliminé
                   //Status 1 : on est dans la partie
                   //Status 2 : on est dans le mode bonus
      },
      score:{
        gameScore: [],
        topPlayer: null,
        displayScore: 0,
      }
    }
  },
  methods: {
    reloadPage: function () {
      window.location.reload();
    },
    validatePseudo: function () {
      if(this.join.pseudo){
        this.join.gamePass = "";
        this.join.pseudoIncorrect = false;
      }
    },
    validatePass: function () {
      if(this.join.gamePass){
        this.$socket.emit("join_game",{ pin: this.join.gamePass,pseudo: this.join.pseudo})
      }
    },
    sendAnswer: function(answer){
      if(this.play.status === 2){
        if(this.play.num_ans  > 1){
          let answer_num = []
          for( let i = 0;i<this.play.checked_ans.length;i++){
            answer_num.push(this.play.answers.indexOf(this.play.checked_ans[i],0))
          }
          this.$socket.emit("send_answer_bonus_call",{ pin: this.join.gamePass,pseudo: this.join.pseudo,answer_num:answer_num})
        }else{
          this.$socket.emit("send_answer_bonus_call",{ pin: this.join.gamePass,pseudo: this.join.pseudo,answer_num:[this.play.answers.indexOf(answer,0)]})
        }
        //console.log('send public')
        this.play.answers = []
        this.play.checked_ans = []
        this.play.question =null
        this.play.answers=null
        this.play.correctness= null
        this.play.status = -1 //reset the rank of the player once he send his answer
      }
      else if(this.play.bonus_activated){
        this.$socket.emit("send_answer_bonus",{ pin: this.join.gamePass,pseudo: this.join.pseudo,"answer":answer})
        //console.log('send 50/50')
        this.play.question =null
        this.play.answers=null
        this.play.correctness= null
      }else{
        if(this.play.num_ans  > 1){
          let answer_num = []
          for( let i = 0;i<this.play.checked_ans.length;i++){
            answer_num.push(this.play.answers.indexOf(this.play.checked_ans[i],0))
          }
          this.$socket.emit("send_answer",{ pin: this.join.gamePass,pseudo: this.join.pseudo,answer_num:answer_num})
          this.play.answers = []
          this.play.checked_ans = []

        }else{
          this.$socket.emit("send_answer",{ pin: this.join.gamePass,pseudo: this.join.pseudo,answer_num:[this.play.answers.indexOf(answer,0)]})
        }
        //console.log('normal ans')
        this.play.question =null
        this.play.answers=null
        this.play.correctness= null
      }
      this.play.bonus_activated = false
      //console.log('reset the timer')
      clearInterval(this.play.timer);//reset the timer
      this.play.timertick = 20
    },
    questiontimer: function(){
      if(this.play.timertick === 0 && this.play.wait_ans === false){ //Si on a rien envoyé à la fin du timer
        //console.log('reset the timer question timer')
        clearInterval(this.play.timer);
        this.$socket.emit("send_answer",{ pin: this.join.gamePass,pseudo: this.join.pseudo,answer_num:-1})
        this.play.question =null
        this.play.answers=null
        this.play.correctness= null
      }
      if(document.getElementById("timer") != null){
        document.getElementById("timer").innerHTML = this.play.timertick;
        if(!this.play.wait_ans){
          this.play.timertick -=1;
        }else{
          this.play.timertick = 20
        }
      }

    },
    display_score: function(){
      this.score.displayScore = 1;
    },
    request_bonus: function(type){
      this.$socket.emit("request_bonus",{ pin: this.join.gamePass,pseudo: this.join.pseudo,bonus:type})
      if(type === 0){
        this.play.fifty_used = true
      }else{
        this.play.public_used = true
      }
      this.play.bonus_activated = false
    },
    get_call_answers: function(){
      this.$socket.emit("get_public_answers",{ pin: this.join.gamePass,pseudo: this.join.pseudo})
      //console.log("clear answer in get_call ? ")
      clearInterval(this.play.timer)
      this.play.timertick = 20
      this.play.timer = setInterval(this.questiontimer,1000)
      this.play.wait_ans = false
      document.getElementById("wait").style.display = "none"
    }
  },
  sockets: {
    connect(){
      this.socket.isConnected = true
    },

    disconnect(){
      this.socket.isConnected = false
    },
    message(data){
      this.socket.message = data
    },

    set_question(data){
      if(this.play.status !== -1){ //if not eliminated
        this.play.status = 1
      }else{
        this.play.fifty_used = true
        this.play.public_used = true
      }
      this.play.bonus_activated = false
      this.play.print_public = 0
      //console.log("reset timer set question")
      clearInterval(this.play.timer);
      this.play.timertick = 20;
      this.play.timer = setInterval(this.questiontimer,1000);
      this.play.question = data["question"]
      this.play.answers = []
      this.play.correctness = []
      this.play.fifty_available = true
      for(var i=0;i<data['answers'].length;i++){
        if(data['answers'][0]['answer'] === "Vrai"){
          this.play.fifty_available = false
        }
        this.play.answers.push(data['answers'][i]['answer'])
        this.play.correctness.push(data['answers'][i]['correct'])
      }
      let cpt = 0;
      for(var j =0;j<this.play.correctness.length;j++){
        if(this.play.correctness[j] === 1){
          cpt += 1;
        }
      }
      if(cpt >1){
        this.play.fifty_available = false
      }
      this.play.public_call = data['eliminated'] !== 0;
      this.play.num_ans = cpt;
    },
    set_status(data){
      this.play.status = data
    },
    set_users_pseudo(data){
      this.join.pseudos = data
    },
    on_connect_failed(data){
      if(data === '-1' || data ==='-3'){
        this.join.pinIncorrect = true
      }
      if(data === '-2'){
        this.join.pseudoIncorrect = true
      }
    },
    game_end(data){
      this.play.end = data[0];
      this.score.gameScore = data[1];
      this.score.topPlayer = data[2];
      clearInterval(this.play.timer);
    },
    bonus_request(data){
      let bonus = "called the public"
      if(data['bonus_type'] === 0 ){
        bonus = " asked for a fifty fifty"
      }
      else if(this.play.status === -1){
        console.log(data['pseudo'] + " " + bonus)
        //console.log('reset interval for public call only')
        clearInterval(this.play.timer)
        this.play.timer = setInterval(this.questiontimer,1000)
        this.play.timertick = 20
      }
    },
    bonus_time(data){
      if(data["bonus"] === "fifty" ){
        //console.log("It's bonus time 50/50!",data)
        //this.play.timertick = 20
        this.play.answers = []
        this.play.correctness = []
        this.play.answers.push(data['correct']['answer'])
        this.play.answers.push(data['not']['answer'])
        this.play.correctness.push(1)
        this.play.correctness.push(0)
        this.play.fifty_used = true
        this.play.bonus_activated = true
      }else{
        //console.log('BONUS TIME CALL')
        this.play.public_used = true
        this.play.bonus_activated = true
        setTimeout(this.get_call_answers,20000)
        this.play.wait_ans = true
        document.getElementById("wait").style.display = "block"
      }
    },
    public_call(){
      if(this.play.status === -1){
        this.play.status = 2
      }
    },
    public_ans(data){
      this.play.public_ans = data
      this.play.print_public = 1
    },
  }
}
</script>



<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped src="../assets/style.css">
</style>
