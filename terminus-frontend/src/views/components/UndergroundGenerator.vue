<template>
  <div>
    <div class="bg-pastel">
      <svg width="100%" height="70vh">
        <polyline :points="getLinePoints(station, index)" fill="transparent"
                  stroke-width="9" :stroke="getLineColor(index)" v-for="(station, index) in this.stations"
                  :key="'polyline' + index" stroke-linejoin="round"/>
        <circle :cx="station[0]" :cy="height" r="10" stroke="black" stroke-width="5" fill="white"
                v-for="(station, index) in this.stations" :key="'circle' + index"/>
        <image id="TubeWagonMap" xlink:href="../../assets/img/tube_wagon.png" x="-38" :y="height - 60" width="75"  height="auto"/>
      </svg>
    </div>
  </div>
</template>

<script>

export default {
  name: "UndergroundGenerator",
  props: ["undergroundTrail", "numero", "stations"],
  data() {
    return {
      step: window.innerWidth / (this.undergroundTrail.length + 1),
      points: "",
      height: Math.floor(window.innerHeight * .8 / 2)
    }
  },
  methods: {
    getLineColor: function (index) {
      for(let i = 0; i < this.undergroundTrail.length; i++) {
        if(i === index) {
          return this.undergroundTrail[i];
        }
      }
      return "black";
    },
    getLinePoints: function (station, index) {
      let directions = [-1, 1];
      let p;
      if(index === 0) {
        p = '0,' + this.stations[index][1] + ' ' + this.stations[index][0] + ',' + this.stations[index][1] +
            ' ' + this.stations[index + 1][0] + ',' + this.stations[index + 1][1];
      } else if(index === this.stations.length - 1) {
        p = window.innerWidth + ',' + this.stations[index][1] + ' ' + this.stations[index][0] + ',' + this.stations[index][1];
      } else {
        p = this.stations[index][0] + ',' + this.stations[index][1] + ' ' + this.stations[index + 1][0] + ',' + this.stations[index + 1][1];
      }

      let rNbPoints = Math.floor(Math.random() * (7 - 3)) + 3;
      let rY = Math.round(Math.random());
      let rDirectionY = directions[rY];
      let rX = Math.round(Math.random());
      let rDirectionX = directions[rX];
      if(index < this.stations.length - 1) {
        let coord = [this.stations[index + 1][0], this.stations[index + 1][1]];
        for(let i = 0; i < rNbPoints; i++) {
          let newPoint;
          let rGap = Math.random() * (200 - 40) + 40;
          if (i < rNbPoints - 1) {
            if (i % 2 === 0) {
              newPoint = coord[0] + ',' + (coord[1] + rDirectionY * rGap);
              coord = [coord[0], coord[1] + rDirectionY * rGap];
            } else {
              newPoint = (coord[0] + rDirectionX * rGap) + ',' + coord[1];
              coord = [coord[0] + rDirectionX * rGap, coord[1]];
            }
          } else {
            if (i % 2 === 0) {
              newPoint = coord[0] + ',' + (coord[1] + rDirectionY * window.innerHeight);
            } else {
              newPoint = (coord[0] + rDirectionX * window.innerWidth) + ',' + coord[1];
            }
          }
          p += ' ' + newPoint;
        }
      }

      return p;
    },
    moveTube: function () {
      let wagon = document.getElementById("TubeWagonMap");
      wagon.style["-webkit-transform"] = "translate(" + (this.step * this.numero) + "px, 0px)";
      wagon.style["-moz-transform"] = "translate(" + (this.step * this.numero) + "px, 0px)";
      wagon.style["-ms-transform"] = "translate(" + (this.step * this.numero) + "px, 0px)";
      wagon.style["-o-transform"] = "translate(" + (this.step * this.numero) + "px, 0px)";
      wagon.style["transform"] = "translate(" + (this.step * this.numero) + "px, 0px)";
      wagon.style["transition"] = "2s";
    }
  },
  watch: {
    numero: function () {
      this.moveTube();
    }
  }
}
</script>

<style scoped src="../../assets/style.css">
</style>