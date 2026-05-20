<template>
  <div>
    <h1>Region Restriction Panel</h1>
    <ul>
      <li v-for="region in regions" :key="region.id">
        {{ region.name }} ({{ region.enabled ? 'Enabled' : 'Disabled' }})
      </li>
    </ul>
    <button @click="enableRegion">Enable Region</button>
    <button @click="disableRegion">Disable Region</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      regions: []
    }
  },
  mounted() {
    this.getRegions()
  },
  methods: {
    getRegions() {
      fetch('/region/restrictions')
        .then(response => response.json())
        .then(data => this.regions = data.regions)
    },
    enableRegion(region) {
      fetch(`/region/restrictions/enabled/${region.id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ region: region.name })
      })
        .then(response => response.json())
        .then(data => console.log(data))
    },
    disableRegion(region) {
      fetch(`/region/restrictions/enabled/${region.id}`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ region: region.name })
      })
        .then(response => response.json())
        .then(data => console.log(data))
    }
  }
}
</script>