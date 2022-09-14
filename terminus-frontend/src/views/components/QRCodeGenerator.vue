<template>
  <div>
    <qr-code :text="this.url"></qr-code>
  </div>
</template>

<script>

export default {
  name: "QRCodeGenerator",
  props: ["url"]
}
</script>

<style scoped>

</style>