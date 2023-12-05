<template>
  <div class="page-log-in">
    <div class="login-container">
      <h1 class="title">Sign Up</h1>

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
            <button @click="submitForm" type="button" class="btn btn-dark">Sign Up</button>
          </div>
        </div>
      </form>
      <div class="signup-link">
        <button @click="click" type="button" class="btn btn-dark btn1">
          Or
          <router-link to="/" class="log">log in</router-link>
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">

import axios from 'axios'
import {toast} from 'bulma-toast'
import {defineComponent} from 'vue'
import {useRouter} from "vue-router";

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

              this.$router.push('/')
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
  },
  setup() {
    const router = useRouter()
    const click = () => {
      router.push({
        path: '/'
      })
    }
    return {
      click
    }
  },
})
</script>

<style scoped>

.login-container{
  margin-top: 70px;
}

* {
  box-sizing: border-box;
}

body, html {
  margin: 0;
  padding: 0;
}

.form-control {
  width: 25vw;
  border: 1px solid black; /* Add a 1px black border around the form control */
  padding: 8px; /* Add some padding for better visual appearance */
  border-radius: 4px; /* Optional: Add border-radius for rounded corners */
}

.page-log-in {
  background-image: url("@/assets/Gc8O6Q-eDU80Qvul88uNW.png");
  background-size: cover;  /* Scale the background image to fit within the container */
  background-repeat: no-repeat;  /* Prevent the background image from repeating */
  background-position: center center; /* Center the background image */
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100vw;
  margin-right: 50px;
}

.title {
  text-align: center;
  color: white;
  margin-left: 30px;
}
.field{
  margin-bottom: 15px;
}
.center-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
  margin-left: 30px;
}

.signup-link {
  text-align: center;
  text-decoration: none;
}

.log {
  text-decoration: none;
  color: white;
}

.btn{
background-color: #141333 !important;
  width: 10vw;
}

.btn1{
  width: 7vw;
  margin-left: 30px;
}

</style>