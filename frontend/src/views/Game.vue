<template>
  <div
      class="main"
      :class="{ 'night': isNightMode, 'evening': isEvening, 'day': isDay, 'morning': isMorning }"
      @keydown="handleKeyDown"
      tabindex="0"
      :style="{ backgroundPosition: `${Math.floor(parallaxOffsetLayer5)}px 0, ${Math.floor(parallaxOffsetLayer3)}px 0, ${Math.floor(parallaxOffsetLayer4)}px 0, ${Math.floor(parallaxOffsetLayer2)}px 0, 0 0` }"
  >
    <audio id="backgroundMusic" loop>
      <source src="@/assets/soundtrack.mp3" type="audio/mp3"/>
      Your browser does not support the audio tag.
    </audio>

    <h1 class="score">Очки: {{ score }}</h1>
    <div class="guide">
      <h1 class="guide-space">Прыжок: Пробел</h1>
      <h1 class="guide-attack">Атака: Левый Ctrl</h1>
    </div>

    <div class="game-area">
      <div
          class="character"
          :style="{ bottom: `${dinoBottom}px`, left: `${dinoLeft}px`, backgroundImage: `url(${
            isJumping
            ? require('@/assets/run_6_clear.png')
            : isAttacking
            ? attackFrames[attackFrameIndex]
            : characterFrames[frameIndex]
          })`
      }"
      ></div>
      <div
          v-for="(obstacle, index) in obstacles"
          :key="index"
          class="obstacle"
          :class="{ 'ninja': obstacle.isNinja }"
          :style="{
            bottom: `${obstacle.bottom}px`,
            left: `${obstacle.left}px`,
            backgroundImage: `url(${obstacle.obstacleImage})`}"
      ></div>
      <div class="ground" :style="{ backgroundPosition: `${Math.floor(parallaxOffsetGround)}px 0` }"></div>
    </div>
    <div v-if="isGameOver" class="overlay"></div>

    <div v-if="isGameOver" class="game-over-screen">
      <h1 class="game-over__header">Game Over</h1>
      <h2 class="game-over__score">Score: {{ score }}</h2>
      <button @click="resetGame" class="game-over__button">Restart</button>
      <router-link class="game-over_router-link" to="/screen-play">
        <button class="game-over__button-menu">Back to menu</button>
      </router-link>
    </div>
  </div>
</template>


<script lang="ts">
import {defineComponent} from 'vue'
import axios from "axios";

export default defineComponent({
  data() {
    return {
      dinoBottom: 0 as number,
      dinoLeft: 20 as number,
      isJumping: false as boolean,
      score: 0 as number,
      obstacles: [] as { bottom: number; left: number; obstacleImage: string; isNinja: boolean }[],
      coef: 1 as number,
      ninjaFrames: [
        require('@/assets/enemy_run_1.png'),
        require('@/assets/enemy_run_2.png'),
        require('@/assets/enemy_run_3.png'),
        require('@/assets/enemy_run_4.png'),
        require('@/assets/enemy_run_5.png'),
        require('@/assets/enemy_run_6.png'),
        require('@/assets/enemy_run_7.png'),
        require('@/assets/enemy_run_8.png'),
      ],
      characterFrames: [
        require('@/assets/run_1.png'),
        require('@/assets/run_2.png'),
        require('@/assets/run_3.png'),
        require('@/assets/run_4.png'),
        require('@/assets/run_5.png'),
        require('@/assets/run_6.png'),
        require('@/assets/run_7.png'),
        require('@/assets/run_8.png'),
      ],
      attackFrames: [
        require('@/assets/attack_1.png'),
        require('@/assets/attack_2.png'),
        require('@/assets/attack_3.png'),
      ],
      isAttacking: false as boolean,
      attackFrameIndex: 0 as number,
      frameIndex: 0 as number,
      ninjaFrameIndex: 0 as number,
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
      isNightMode: false as boolean,
      isEvening: false as boolean,
      isMusic: true as boolean,
      isNinja: false as boolean,
      isDay: false as boolean,
      isMorning: false as boolean,
      isGameOver: false as boolean
    };
  },
  methods: {
    playBackgroundMusic() {
      const backgroundMusic = document.getElementById('backgroundMusic') as HTMLAudioElement;
      backgroundMusic.play();
      backgroundMusic.volume = 0.5;
    },
    animateCharacter() {
      setInterval(() => {
        if (!this.isJumping) {
          this.frameIndex = (this.frameIndex + 1) % this.characterFrames.length;
        }
      }, 100);
    },
    animateNinja() {
      setInterval(() => {
        this.ninjaFrameIndex = (this.ninjaFrameIndex + 1) % this.ninjaFrames.length;
      }, 100);
    },
    handleKeyDown(event: KeyboardEvent) {
      if (event.key === ' ' && !this.isJumping) {
        this.isJumping = true;
        this.jump();
      } else if (event.code === 'ControlLeft') {
        this.attackNearbyEnemy();
      }
    },

    attackNearbyEnemy() {
      if (!this.isAttacking) {
        this.isAttacking = true;
        this.animateAttack();
      }
      const playerPosition = {
        left: this.dinoLeft,
        right: this.dinoLeft + 200,
        bottom: this.dinoBottom + 200,
      };

      for (let i = 0; i < this.obstacles.length; i++) {
        const obstacle = this.obstacles[i];
        const enemyNinjaPosition = {
          left: obstacle.left,
          right: obstacle.left + (obstacle.isNinja ? 70 : 50),
          bottom: obstacle.bottom + (obstacle.isNinja ? 70 : 38),
        };

        if (
            playerPosition.right > enemyNinjaPosition.left &&
            playerPosition.left < enemyNinjaPosition.right &&
            playerPosition.bottom > enemyNinjaPosition.bottom && obstacle.isNinja
        ) {
          this.obstacles.splice(i, 1);
          this.score += 3;
          this.checkNightMode();
          this.checkEvening();
          this.checkDay();
          this.checkMorning();
          break;
        }
      }
    },
    animateAttack() {
      const attackInterval = setInterval(() => {
        this.attackFrameIndex = (this.attackFrameIndex + 1) % this.attackFrames.length;
      }, 80);

      setTimeout(() => {
        clearInterval(attackInterval);
        this.isAttacking = false;
      }, this.attackFrames.length * 80);
    },
    jump() {
      const jumpHeight: number = 100;
      const jumpDuration: number = 500;
      const initialBottom: number = this.dinoBottom;

      let startTime: number | null = null;

      const jumpAnimation = (timestamp: number) => {
        if (!startTime) startTime = timestamp;

        const progress: number = timestamp - startTime;

        this.dinoBottom = initialBottom + Math.sin((progress / jumpDuration) * Math.PI) * jumpHeight;

        if (progress < jumpDuration) {
          requestAnimationFrame(jumpAnimation);
        } else {
          this.isJumping = false;
          this.dinoBottom = initialBottom;
        }
      };

      requestAnimationFrame(jumpAnimation);
    },
    moveObstacles() {
      const obstacleSpeed = 5 * this.coef;
      for (let i = 0; i < this.obstacles.length; i++) {
        const obstacle = this.obstacles[i];


        if (obstacle.isNinja) {
          obstacle.obstacleImage = this.ninjaFrames[this.ninjaFrameIndex];
        }

        obstacle.left -= obstacleSpeed;
        if (obstacle.left < -7) {
          this.obstacles.splice(i, 1);
          this.score++;
          this.checkNightMode();
          this.checkEvening();
          this.checkDay();
          this.checkMorning();
        }
      }
      this.parallaxOffsetGround -= obstacleSpeed;
    },


    async checkCollisions() {
      const dino = {
        bottom: this.dinoBottom,
        left: this.dinoLeft,
        right: this.dinoLeft + 50,
        top: this.dinoBottom + 50,
      };
      const username = localStorage.getItem('username');

      for (const obstacle of this.obstacles) {
        const obs = {
          bottom: obstacle.bottom,
          left: obstacle.left,
          top: obstacle.bottom + 28,
          right: obstacle.left + 40,
        };

        if (dino.bottom < obs.top &&
            dino.right > obs.left &&
            dino.left < obs.right) {
          this.isGameOver = true;
          const finalScore = this.score;
          const token = localStorage.getItem('token');
          if (token) {
            axios.defaults.headers.common['Authorization'] = `Token ${token}`;
            const response = await axios.get('http://127.0.0.1:8000/api/v1/score/leaderboard', {
              params: {
                username,
              }
            });
            const UserScore: any[] = response.data;
            let UserScore1: number = 0;
            for (const tuple of UserScore) {
              if (tuple.username == username) {
                UserScore1 = tuple.score;
              }
            }
            if (UserScore1 <= finalScore) {
              axios.patch('http://127.0.0.1:8000/api/v1/score/', {score: finalScore})
            }
          }
        }
      }
    },

    resetGame() {
      this.isGameOver = false;
      this.obstacles = [];
      this.score = 0;
      window.location.reload();
    },

    gameLoop() {
      if (!this.isGameOver) {
        this.moveObstacles();
        this.checkCollisions();
      }
    },
    checkMorning() {
      if (this.score % 100 >= 0 && this.score % 100 < 25 && !this.isMorning) {
        this.isMorning = true;
      } else if (this.score % 100 >= 25) {
        this.isMorning = false;
      }
    },
    checkDay() {
      if (this.score % 100 >= 25 && this.score % 100 < 50 && !this.isDay) {
        this.isDay = true;
      } else if (this.score % 100 >= 50) {
        this.isDay = false;
      }
    },
    checkEvening() {
      if (this.score % 100 >= 50 && this.score % 100 < 75 && !this.isEvening) {
        this.isEvening = true;
      } else if (this.score % 100 >= 75) {
        this.isEvening = false;
      }
    },
    checkNightMode() {
      if (this.score % 100 >= 75 && this.score % 100 < 100 && !this.isNightMode) {
        this.isNightMode = true;
      } else if (this.score % 100 < 75) {
        this.isNightMode = false;
      }
    },
    startGame() {
      console.log('Игра начинается!');
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

  mounted() {
    this.playBackgroundMusic();
    this.$el.focus();
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

    preloadImages([
      require('@/assets/Layer_5.png'),
      require('@/assets/Layer_3.png'),
      require('@/assets/Layer_4.png'),
      require('@/assets/Layer_2_morning.png'),
      require('@/assets/Layer_1_day.png'),
      require('@/assets/Layer_5_night.png'),
      require('@/assets/Layer_3_night.png'),
      require('@/assets/Layer_4_night.png'),
      require('@/assets/Layer_2_night.png'),
      require('@/assets/Layer_1_night.png'),
      require('@/assets/Layer_1_night.png'),
      require('@/assets/Layer_5_sakura.png'),
      require('@/assets/Layer_3_sakura.png'),
      require('@/assets/Layer_4_sakura.png'),
      require('@/assets/Layer_2_sakura.png'),
      require('@/assets/Layer_1_sakura.png')
    ], this.startGame);
    const addObstacle = () => {
      const isNinja = Math.random() < 0.15;
      const obstacleImage = isNinja ? this.ninjaFrames[this.ninjaFrameIndex] : require('@/assets/spike_1.png');
      this.obstacles.push({
        bottom: 0,
        left: 1270,
        obstacleImage: obstacleImage,
        isNinja: isNinja,
      });
      this.coef += 0.05;
      this.parallaxLayer3Speed += 0.01;
      this.parallaxLayer2Speed += 0.01;
      this.parallaxLayer4Speed += 0.01;
      this.parallaxLayer5Speed += 0.01;

      setTimeout(addObstacle, (500 + Math.random() * 2000) + 0.05);
    };
    addObstacle();
    setInterval(this.gameLoop, 15)
    this.animateCharacter();
    this.parallaxAnimation();
    this.animateNinja();
    window.addEventListener('keydown', this.handleKeyDown);
    this.checkMorning();
  }
})
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
}

.main {
  width: 100%;
  height: 100%;
  position: fixed;
  background-repeat: repeat;
  background-size: cover;
  transition: background-image 2s ease;
}

.main.morning {
  background-image: url('../assets/Layer_5.png'), url('../assets/Layer_3.png'), url('../assets/Layer_4_morning.png'), url('../assets/Layer_2_morning.png'), url('../assets/Layer_1_morning.png');
}

.main.day {
  background-image: url('../assets/Layer_5.png'), url('../assets/Layer_3.png'), url('../assets/Layer_4.png'), url('../assets/Layer_2.png'), url('../assets/Layer_1_day.png');
}

.main.night {
  background-image: url('../assets/Layer_5_night.png'), url('../assets/Layer_3_night.png'), url('../assets/Layer_4_night.png'), url('../assets/Layer_2_night.png'), url('../assets/Layer_1_night.png');
}

.main.evening {
  background-image: url('../assets/Layer_5_sakura.png'), url('../assets/Layer_3_sakura.png'), url('../assets/Layer_4_sakura.png'), url('../assets/Layer_2_sakura.png'), url('../assets/Layer_1_sakura.png');
}

.guide {
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  flex-direction: column;
  color: white;
  justify-content: right;
}

.guide-space {
  font-size: 30px
}

.guide-attack {
  font-size: 30px
}

.obstacle.ninja {
  width: 70px;
  height: 70px;

}

.game-area {
  position: relative;
  width: 1280px;
  height: 600px;
  margin-top: 20px;
}

.ground {
  position: relative;
  height: 40px;
  width: 1280px;
  background-image: url('../assets/Tile_22.png');
  top: 100%;
}

.obstacle {
  position: absolute;
  width: 50px;
  height: 38px;
  background-size: cover;
}

.score {
  display: flex;
  justify-content: center;
  color: white;
  margin-top: 10px;
  padding: 0;
  border: none;

}

.character {
  position: absolute;
  width: 150px;
  height: 150px;
  background-size: cover;
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(15px);
  z-index: 999;
}

.game-over-screen {
  display: flex;
  flex-direction: column;
  justify-content: center;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  z-index: 1000;
  color: white;
}

.game-over__button {
  border-radius: 3rem;
  font-size: 20px;
  text-decoration: none;
  color: black;
  font-weight: 700;
  padding: 1rem 2rem;
  margin: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30vw;
}

.game-over__button:hover {
  background-color: darkcyan;
}

.game-over_router-link {
  text-decoration: none;
}

.game-over__header {
  font-weight: 900;
  font-size: 70px;
}

.game-over__button-menu {
  border-radius: 3rem;
  font-size: 20px;
  text-decoration: none;
  color: black;
  font-weight: 700;
  padding: 1rem 2rem;
  margin: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30vw;
}

.game-over__button-menu:hover {
  background-color: darkcyan;
}
</style>
