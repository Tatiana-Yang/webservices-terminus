<template>
  <div id="Layout">
    <Header/>
    <router-view class="body-routes" style="min-height: 100vh"/>
    <Footer/>
  </div>
</template>

<script>
import Header from "../views/components/Header";
import Footer from "../views/components/Footer";

export default {
  name: "Layout",
  components: {
    Header,
    Footer
  }
}
</script>

<style scoped src="../assets/style.css">
</style>
