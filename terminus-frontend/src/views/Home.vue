<template>
  <div>
    <div v-if="$root.id == null">
      <div class="parallax bg-map" style="border-bottom: solid 5px black">
        <div class="text-content p-5">
          <h1 class="display-4">Bienvenue !</h1>
          <p class="lead">Vous voulez faire travailler vos méninges tout en vous amusant ? Vous êtes au bon endroit !</p>
        </div>
      </div>
      <div class="p-5 bg-grey">
        <div class="container">
          <div class="d-flex justify-content-around">
            <div class="col bg-blue p-3 m-3 rounded">
              <h2 class="text-center">Créer</h2>
              <hr>
              <p>Il ne faut que quelques minutes pour créer un jeu d'apprentissage ou un jeu-questionnaire sur n'importe quel sujet.</p>
            </div>
            <div class="col bg-red p-3 m-3 rounded">
              <h2 class="text-center">Organiser & partager</h2>
              <hr>
              <p>Organisez une partie en direct avec des questions sur grand écran ou partagez une partie avec des joueurs distants.</p>
            </div>
            <div class="col bg-green p-3 m-3 rounded">
              <h2 class="text-center">Jouer</h2>
              <hr>
              <p>C'est parti ! Rejoignez une partie avec un code PIN fourni par l'hôte et répondez aux questions sur votre appareil afin de vous rendre au terminus.</p>
            </div>
          </div>
        </div>
      </div>
    </div>


    <div v-else>
      <div class="parallax bg-map" style="border-bottom: solid 5px black">
        <div class="text-content p-5 text-center" style="width: 100%">
          <h1 class="display-4">Bonjour {{ this.$root.username }} !</h1>
        </div>
      </div>
      <div class="d-flex justify-content-center">
        <div class="col bg-yellow-pastel">
          <div class="d-flex justify-content-around">
            <div class="col-auto" style="width: 30%; margin: auto">
              <div class="card text-center mt-5 mb-5">
                <img class="card-img-top" src="../assets/img/london_tube.gif" alt="London tube">
                <div class="card-body">
                  <router-link to="/terminus/quizz/create" class="">
                    <button type="button" class="btn btn-tube btn-lg" style="margin-top: -30%" >Créer</button>
                  </router-link>
                  <p class="card-text text-dark">Créer un quiz de A à Z et inviter vos amis</p>
                </div>
              </div>
            </div>
            <div class="col-auto" style="width: 30%; margin: auto">
              <div class="card text-center mt-5 mb-5">
                <img class="card-img-top" src="../assets/img/tube_animation.gif" alt="London tube">
                <div class="card-body">
                  <router-link to="/terminus/game/join" class="">
                    <button type="button" class="btn btn-tube btn-lg" style="margin-top: -30%" >Rejoindre</button>
                  </router-link>
                  <p class="card-text text-dark">Rejoindre une partie via son code PIN</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-auto bg-red p-3" style="max-height: 70vh; overflow-y: scroll">
          <h3>Rejoindre une partie</h3>
          <div v-for="game in this.games" :key="game.id">
            <hr>
            <div class="d-flex justify-content-around">
              <div class="col">
                <h5>{{ game.title }}</h5>
              </div>
              <div class="col-auto">
                <button type="button" class="btn btn-play"><i class="fas fa-play"></i></button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!--<QRCodeGenerator url="Hello there !"/>-->
  </div>
</template>

<script>
//import QRCodeGenerator from "@/views/components/QRCodeGenerator";

export default {
  name: 'Home',
  /*components: {
    QRCodeGenerator
  },*/
  data() {
    return {
      games: [
        {
          title: "Star Wars Quiz",
          id: "1234"
        },
        {
          title: "Olympic Quiz",
          id: "5678"
        },
        {
          title: "Pumpquiz",
          id: "9123"
        },
        {
          title: "Salade de fruit jolie jolie jolie",
          id: "4567"
        },
        {
          title: "Guess who ?",
          id: "8912"
        },
        {
          title: "The 5W",
          id: "3456"
        }
      ]
    }
  }
}
</script>

<style scoped src="../assets/style.css">
</style>
