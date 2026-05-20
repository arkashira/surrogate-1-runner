<template>
  <div class="overload-matrix">
    <input v-model="searchQuery" placeholder="Search by method signature" />
    <select v-model="selectedVersion">
      <option v-for="version in versions" :key="version" :value="version">{{ version }}</option>
    </select>
    <table>
      <thead>
        <tr>
          <th>Method</th>
          <th v-for="paramType in paramTypes" :key="paramType">{{ paramType }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="method in filteredMethods" :key="method.signature">
          <td>{{ method.name }}</td>
          <td v-for="paramType in paramTypes" :key="paramType">
            <a v-if="method.overloads[paramType]" :href="method.overloads[paramType].link">
              {{ method.overloads[paramType].signature }}
            </a>
            <span v-else>-</span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: '',
      selectedVersion: 'latest',
      versions: ['latest', 'v1', 'v2'], // Example versions
      methods: [
        {
          name: 'exampleMethod',
          signature: 'exampleMethod(param1: string, param2: number)',
          overloads: {
            'string': { signature: 'exampleMethod(param1: string)', link: '/docs/exampleMethod-string' },
            'number': { signature: 'exampleMethod(param2: number)', link: '/docs/exampleMethod-number' }
          }
        }
      ],
      paramTypes: ['string', 'number'] // Example parameter types
    };
  },
  computed: {
    filteredMethods() {
      return this.methods.filter(method => 
        method.signature.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    }
  }
};
</script>

<style scoped>
.overload-matrix {
  margin: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
}

th {
  background-color: #f2f2f2;
}
</style>