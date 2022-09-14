<template>
 <div>
   <div class="parallax bg-tube" style="border-bottom: solid 5px black">
     <div class="text-content-red p-5">
       <h1 class="display-4 about-title rounded">À propos</h1>
     </div>
   </div>

   <div class="bg-white">
     <div class="d-flex justify-content-center p-5">
       <div class="col">
         <h3 class="display-4 pt-5">Des thèmes pour tout le monde !</h3>
       </div>
       <div class="col">
         <div class="card bg-light mb-3">
           <h5 class="card-header">Lignes</h5>
           <div class="card-body">
             <div class="card-text">
               <div class="row">
                 <div class="col-6" v-for="route in this.routes" :key="route.id_tag">
                   <div class="row">
                     <div class="col-auto">
                       <div :style="{ 'background-color': route.color_tag }" style="width: 20px; height: 5px; margin-top: 10px"></div>
                     </div>
                     <div class="col">
                       <p>{{ route.name_tag }}</p>
                     </div>
                   </div>
                 </div>
               </div>
             </div>
           </div>
         </div>
       </div>
     </div>

     
     <div class="bg-pastel">
       <div class="p-5 developer-section ml-5 mr-5">
         <h3 class="display-4 text-center">Des développeurs au top !</h3>
         <hr>
         <div class="row justify-content-around">
           <div class="col text-center">
             <img src="../assets/img/guillaume_avatar.png" alt="Guillaume avatar">
             <h5 class="mt-2">Guillaume HASENEYER</h5>
           </div>
           <div class="col text-center">
             <img src="../assets/img/clemence_avatar.jpg" alt="Clémence avatar">
             <h5 class="mt-2">Clémence LE ROUX</h5>
           </div>
           <div class="col text-center">
             <img src="../assets/img/mathilde_avatar.png" alt="Mathilde avatar">
             <h5 class="mt-2">Mathilde LERAY</h5>
           </div>
           <div class="col text-center">
             <img src="../assets/img/tatiana_avatar.jpg" alt="Tatiana avatar">
             <h5 class="mt-2">Tatiana YANG</h5>
           </div>
         </div>
       </div>
     </div>
   </div>
 </div>
</template>

<script>
//import routes from '../underground/Routes.json';
import axios from "axios";

export default {
  name: "About",
  data() {
    return {
      routes: []
    }
  },
  methods: {
    getTags: function () {
      axios.get("/api/get_tags")
          .then((response) => {
            this.$set(this, "routes", response.data);
            console.log(response.data);
          })
          .catch((errors) => {
            console.log(errors);
            this.$router.push("/terminus");
            this.$root.disconnected = "expired";
          })
    }
  },
  mounted() {
    this.getTags();
  }
}
</script>

<style scoped src="../assets/style.css">

</style>