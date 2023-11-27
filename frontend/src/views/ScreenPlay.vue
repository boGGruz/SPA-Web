<template>
  <div class="content">
    <div class="content-transition">
      <transition name="fade" mode="out-in">
        <div>
          <i class="menu" v-if="!show" @click="show = !show" key="menu"><img src="../assets/cup.png" class="cup"></i>
          <i class="clear" v-else @click="show = !show" key="clear"><img src="../assets/cup.png" class="cup-press cup"></i>
        </div>
      </transition>
      <transition name="fade">
        <ol v-if="show">
          <li v-for="item in items">{{ item }}</li>
        </ol>
      </transition>
    </div>
    <button class="button-play" @click="click"><router-link to="/samurai-way" class="log"></router-link>
      <p>Play</p>
    </button>
  </div>
</template>

<script lang="ts">
import {defineComponent} from 'vue'
import {useRouter} from "vue-router";
export default defineComponent ({
  el:'#app',
  data() {
    return {
      items: [
          'Abobus: 127',
          'Bobik: 123',
          'Cema: 99',
          'HerPsini: 28',
          'Bot: 1',
      ],
      show: false
    }
  },
  setup() {
        const router = useRouter()
        const click = () => {
            router.push({
                path: 'samurai-way'
            })
        }
        return {
            click
        }
    }
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');

.content {
  display: flex;
  padding: 1rem;
}

li {
  width: 50%;
  padding: 1rem;
  margin: 1rem;
  border: 2px solid #000;
  background-color: #efefef;
  font-family: Poppins, sans-serif;
  font-weight: 700;
  letter-spacing: 1px;
}

.cup {
  padding-left: 1.5rem;
  padding-top: 1rem;
  width: 12%;
}

.cup-press {
  opacity: 50%;
}

.button-play {
  height: 50%;
  margin-top: 18%;
  margin-left: 9%;
  padding: 1rem 3rem 0rem 3rem;
  font-family: Poppins, sans-serif;
  font-weight: 900;
  font-size: 30px;
  letter-spacing: 1px;
  border: 3px solid #000;
  border-radius: 3rem;
}
</style>
