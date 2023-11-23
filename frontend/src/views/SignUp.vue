<template>
  <div class="page-sign-up">
    <div class="columns">
      <div class="column is-4 is-offset-4">
        <h1 class="title">Sign up</h1>

        <form @submit.prevent="submitForm" class="center-form">
          <div class="field">
            <div class="control">
              <input type="text" class="form-control" placeholder="Username" v-model="username">
            </div>
          </div>

          <div class="field">
            <div class="control">
              <input type="password" class="form-control" id="exampleInputPassword1" placeholder="Password"
                     v-model="password">
            </div>
          </div>

          <div class="field">
            <div class="control">
              <input type="password" class="form-control" id="exampleInputPassword1" placeholder="Repeat password"
                     v-model="password2">
            </div>
          </div>

          <div class="notification is-danger" v-if="errors.length">
            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
          </div>

          <div class="field">
            <div class="control">
              <button @click="submitForm" type="button" class="btn btn-outline-secondary">Sign up</button>
            </div>
          </div>
          <div>
            Or <router-link to="/" class="log">log in</router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script lang="ts">

import axios from 'axios'
import {toast} from 'bulma-toast'
import {defineComponent} from 'vue'

export default defineComponent({
  name: 'SignUp',
  data() {
    return {
      username: '',
      password: '',
      password2: '',
      errors: [] as string[]
    }
  },
  methods: {
    submitForm() {
      this.errors = []
      if (this.username === '') {
        this.errors.push('The username is missing')
      }

      if (this.password === '') {
        this.errors.push('The password is too short')
      }

      if (this.password !== this.password2) {
        this.errors.push('The passwords doesn\'t match')
      }

      if (!this.errors.length) {
        const formData = {
          username: this.username,
          password: this.password
        }

        axios
            .post("/api/v1/users/", formData)
            .then(response => {
              toast({
                message: 'Account created, please log in!',
                type: 'is-success',
                dismissible: true,
                pauseOnHover: true,
                duration: 2000,
                position: 'bottom-right',
              })

              this.$router.push('/game-wave')
            })
            .catch(error => {
              if (error.response) {
                for (const property in error.response.data) {
                  this.errors.push(`${property}: ${error.response.data[property]}`)
                }

                console.log(JSON.stringify(error.response.data))
              } else if (error.message) {
                this.errors.push('Something went wrong. Please try again')

                console.log(JSON.stringify(error))
              }
            })
      }
    }
  }
})
</script>

<style scoped>
.columns {
  margin-top: 25vh;
}

.title {
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

.form-control {
  width: 30vw;
}

.btn {
  width: 12vw;
}

.log{
  text-decoration: none;
  color: darkcyan;
}
</style>