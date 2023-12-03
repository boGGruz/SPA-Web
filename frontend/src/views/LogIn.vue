<template>
  <div class="page-log-in">
    <div class="columns">
      <div class="column is-4 is-offset-4">
        <h1 class="title">Log in</h1>
        <form @submit.prevent="submitForm" class="center-form">
          <div class="field">
            <div class="control">
              <input type="text" class="form-control" placeholder="Username" v-model="username">
            </div>
          </div>

          <div class="field">
            <div class="control">
              <input type="password" class="form-control" id="exampleInputPassword1" placeholder="Password" v-model="password">
            </div>
          </div>

          <div class="notification is-danger" v-if="errors.length">
            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
          </div>

          <div class="field">
            <div class="control">
              <button @click="submitForm" type="button" class="btn btn-outline-secondary">Log in</button>
            </div>
          </div>

          <div>
            Or <router-link to="/sign-up" class="log">sign up</router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import axios from 'axios'
import {defineComponent} from 'vue'

export default defineComponent({
  name: 'LogIn',
  data() {
    return {
      username: '',
      password: '',
      errors: []
    }
  },
  methods: {
    async submitForm() {

      const formData = {
        username: this.username,
        password: this.password
      }

      await axios
          .post("/api/v1/token/login/", formData)
          .then(response => {
            const token = response.data.auth_token

            this.$store.commit('setToken', token)

            this.$store.commit('setUsername', this.username);

            axios.defaults.headers.common["Authorization"] = "Token " + token

            localStorage.setItem("token", token)
            localStorage.setItem('username', this.username);
            console.log("Token:", token);

            const toPath = this.$route.query.to || '/screen-play'

            this.$router.push(toPath as string)
          })
          .catch(error => {
            if (error.response) {
              for (const property in error.response.data) {
                this.errors.push(`${property}: ${error.response.data[property]}` as never)
              }
            } else {
              this.errors.push('Something went wrong. Please try again' as never)

              console.log(JSON.stringify(error))
            }
          })
    }
  }
})
</script>

<style scoped>
.columns{
  margin-top: 25vh;
}

.title{
  display: flex;
  justify-content: center;
  margin-bottom: -20px;
}
.center-form {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-top: 50px;
}

.field {
  margin-bottom: 15px;
}
.form-control{
  width: 30vw;
}
.btn{
  width: 12vw;
}
.log{
  text-decoration: none;
  color: darkcyan;
}
</style>
