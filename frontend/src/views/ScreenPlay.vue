<template>
  <div class="content"
       :style="{ backgroundPosition: `${Math.floor(parallaxOffsetLayer3)}px 0, ${Math.floor(parallaxOffsetLayer4)}px 0, ${Math.floor(parallaxOffsetLayer2)}px 0, 0 0` }"
  >
    <div class="content-transition">
      <transition name="fade" mode="out-in">
        <div class="cup-container">
          <i class="menu" v-if="!show" @click="show = !show" key="menu"><img src="../assets/cup.png" class="cup"></i>
          <i class="clear" v-else @click="show = !show" key="clear"><img src="../assets/cup.png" class="cup-press cup"></i>
        </div>
      </transition>
      <transition name="fade">
        <div class="leaderboard-container" v-if="show">
          <ol class="leaderbord-list">
            <li :class="{'highlighted': entry.username === user_data }" v-for="(entry, index) in leaderboard"
                :key="index">
              <span class="index">{{ index + 1 }}</span>
              <span class="username">{{
                  entry.username
                }}</span>
              <span class="score">Score: {{ entry.score }}</span>
            </li>
          </ol>
        </div>
      </transition>
    </div>
    <button class="button-play" @click="click">
      <router-link to="/samurai-way" class="log"></router-link>
      <p>Play</p>
    </button>
    <button class="action-button" @click="logout">
      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" height="5em" width="5em">
        <path
            d="M19 21H5a2 2 0 0 1-2-2v-4h2v4h14V5H5v4H3V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2Zm-8-5v-3H3v-2h8V8l5 4-5 4Z"
            fill="white"/>
      </svg>
    </button>
  </div>
</template>

<script lang="ts">
import {defineComponent} from 'vue'
import {useRouter} from "vue-router";
import axios from "axios";

export default defineComponent({
  el: '#app',
  data() {
    return {
      leaderboard: [],
      show: false,
      user_data: '' as any,
      parallaxOffsetGround: 0 as number,
      parallaxOffsetLayer6: 0 as number,
      parallaxOffsetLayer5: 0 as number,
      parallaxOffsetLayer4: 0 as number,
      parallaxOffsetLayer3: 0 as number,
      parallaxOffsetLayer2: 0 as number,
      parallaxLayer2Speed: 0.05 as number,
      parallaxLayer3Speed: 1 as number,
      parallaxLayer4Speed: 0.35 as number,
      parallaxLayer5Speed: 0.5 as number,
      parallaxLayer6Speed: 0.5 as number,
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
  },
  methods: {
    async logout(): Promise<void> {
      try {
        const token = localStorage.getItem("token");
        if (token) {
          axios.defaults.headers.common["Authorization"] = "Token " + token;
          console.log("Authorization Token:", axios.defaults.headers.common["Authorization"]);
          await axios.post("/api/v1/token/logout/");
          this.$store.commit("clearTokens");
          localStorage.removeItem("token");
          axios.defaults.headers.common["Authorization"] = "";
        }
        this.$router.push("/");
      } catch (error) {
        console.error("Error during logout:", error);
      }
    },
    async fetchLeaderboard() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/v1/score/leaderboard/');
        this.leaderboard = response.data;
        this.user_data = localStorage.getItem('username');
      } catch (error) {
        console.error('Error fetching leaderboard:', error);
      }
    },
    parallaxAnimation() {
      setInterval(() => {
        this.parallaxOffsetLayer3 -= this.parallaxLayer3Speed;
        this.parallaxOffsetLayer4 += this.parallaxLayer4Speed;
        this.parallaxOffsetLayer2 += this.parallaxLayer2Speed;
        this.parallaxOffsetLayer5 -= this.parallaxLayer5Speed;
        const containerWidth = 1280;
        if (this.parallaxOffsetLayer3 <= -containerWidth) {
          this.parallaxOffsetLayer3 = 0;
        }

        if (this.parallaxOffsetLayer4 <= -containerWidth) {
          this.parallaxOffsetLayer4 = 0;
        }

        if (this.parallaxOffsetLayer5 <= -containerWidth) {
          this.parallaxOffsetLayer5 = 0;
        }

        if (this.parallaxOffsetGround <= -containerWidth) {
          this.parallaxOffsetGround = 0;
        }
      }, 20);
    },
  },
  created() {

    const token = localStorage.getItem("token");

    if (token) {
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;

    } else {
      console.log("Пользователь не авторизован");
    }
  },
  mounted() {
    this.fetchLeaderboard();
    this.$el.focus();
    this.parallaxAnimation();
    const preloadImages = (imageUrls: string[], callback: () => void) => {
      let loadedImages = 0;

      const checkAllImagesLoaded = () => {
        loadedImages++;
        if (loadedImages === imageUrls.length) {
          callback();
        }
      };

      imageUrls.forEach((url) => {
        const img = new Image();
        img.src = url;
        img.addEventListener('load', checkAllImagesLoaded);
      });
    };

  }
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');

.content {
  display: flex;
  padding: 1rem;
  position: fixed;
  width: 100%;
  height: 100%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-repeat: repeat;
  background-size: cover;
  background-image: url('../assets/Layer_3_night.png'),
  url('../assets/Layer_4_night.png'),
  url('../assets/Layer_2_night.png'),
  url('../assets/Layer_1_night.png');
}

li {
  padding: 1rem;
  background-color: white;
  font-family: Poppins, sans-serif;
  font-weight: 700;
  letter-spacing: 1px;
  border-radius: 15px;
  display: flex;
  justify-content: space-around;
  align-items: center;
  margin: 1rem 10px 1rem 0;
}

.index {
  flex-basis: 10%;
}

.username {
  flex-basis: 60%;
  text-align: center;
}

.score {
  flex-basis: 20%;
  text-align: right;
}

.cup {
  padding-left: 1.5rem;
  padding-top: 1rem;
  width: 16%;
  cursor: pointer;
}

.cup-press {
  opacity: 50%;
}

.button-play {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 1rem 3rem 0rem 3rem;
  font-family: Poppins, sans-serif;
  font-weight: 900;
  font-size: 30px;
  letter-spacing: 1px;
  border: 3px solid #000;
  border-radius: 3rem;
}

.action-button {
  background-color: transparent;
  position: fixed;
  left: 93%;
  top: 5%;
  transform: translate(-50%, -10%);
  width: 100px;
  height: 100px;
  text-decoration: none;
  border: none;
}

.leaderboard-container {
  max-height: 37vh;
  overflow-y: auto;
  scroll-behavior: smooth;
  transition: background-color 0.3s ease-in-out;
  padding-right: 0;
}

.leaderboard-container::-webkit-scrollbar {
  width: 8px;
  margin-left: 10px;
  margin-top: 10px;
}

.leaderboard-container::-webkit-scrollbar-thumb {
  background-color: white;
  border-radius: 10px;
}

.leaderboard-container::-webkit-scrollbar-track {
  background-color: transparent;
  margin: 1rem;
}

.cup-container {
  width: 40vw;
}

.highlighted {
  color: #ffad00;
}
</style>
