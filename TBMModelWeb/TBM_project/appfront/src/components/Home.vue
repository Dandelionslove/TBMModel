<template>
  <div>
    {{string_from_api}}
  </div>
</template>

<script>
export default{
    name: 'home',
    data () {
        return {
            string_from_api: ''
        }
    },
    mounted () {
    this.$axios
    .get('http://127.0.0.1:8000/api/1',{
      params:{
        i:2,
        j:3
      }
    })
    .then(response => (this.string_from_api = response.data))
    
    }
}
</script>
