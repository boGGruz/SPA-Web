<template>
  <div class="game-wrapper">
    <div
        class="main"
        :class="{ 'night': isNightMode, 'evening': isEvening, 'day': isDay, 'morning': isMorning }"
        @keydown="handleKeyDown"
        tabindex="0"
        :style="{ backgroundPosition: `${Math.floor(parallaxOffsets['layer5'])}px 0, ${Math.floor(parallaxOffsets['layer3'])}px 0, ${Math.floor(parallaxOffsets['layer4'])}px 0, ${Math.floor(parallaxOffsets['layer2'])}px 0, 0 0` }"

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
      score: 0 as number,
      obstacles: [] as { bottom: number; left: number; obstacleImage: string; isNinja: boolean }[],
      ninjaFrames: Array.from({length: 8}, (_, index) => require(`@/assets/enemy_run_${index + 1}.png`)),
      characterFrames: Array.from({length: 8}, (_, index) => require(`@/assets/run_${index + 1}.png`)),
      attackFrames: Array.from({length: 3}, (_, index) => require(`@/assets/attack_${index + 1}.png`)),
      attackFrameIndex: 0 as number,
      frameIndex: 0 as number,
      ninjaFrameIndex: 0 as number,
      parallaxOffsetGround: 0 as number,
      parallaxOffsets: {
        layer6: 0,
        layer5: 0,
        layer4: 0,
        layer3: 0,
        layer2: 0,
      },
      parallaxLayerSpeeds: {
        layer2: 0.05,
        layer3: 1,
        layer4: 0.35,
        layer5: 0.5,
        layer6: 0.5,
      },
      isNightMode: false as boolean,
      isEvening: false as boolean,
      isMusic: true as boolean,
      isNinja: false as boolean,
      isDay: false as boolean,
      isMorning: false as boolean,
      isGameOver: false as boolean,
      isJumping: false as boolean,
      isAttacking: false as boolean,
      coef: 1 as number,
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
          this.checkTimeOfDay()
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
          this.checkTimeOfDay()
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

    checkTimeOfDay() {
      const timePercentage = this.score % 100;
      this.isMorning = timePercentage >= 0 && timePercentage < 25;
      this.isDay = timePercentage >= 25 && timePercentage < 50;
      this.isEvening = timePercentage >= 50 && timePercentage < 75;
      this.isNightMode = timePercentage >= 75 && timePercentage < 100;
    },

    startGame() {
      console.log('Игра начинается!');
    },

    parallaxAnimation() {
      setInterval(() => {
        this.parallaxOffsets["layer3"] -= this.parallaxLayerSpeeds["layer3"];
        this.parallaxOffsets["layer4"] += this.parallaxLayerSpeeds["layer4"];
        this.parallaxOffsets["layer2"] += this.parallaxLayerSpeeds["layer2"];
        this.parallaxOffsets["layer5"] -= this.parallaxLayerSpeeds["layer5"];
        const containerWidth = 1280;
        if (this.parallaxOffsets["layer3"] <= -containerWidth) {
          this.parallaxOffsets["layer3"] = 0;
        }

        if (this.parallaxOffsets["layer4"] <= -containerWidth) {
          this.parallaxOffsets["layer4"] = 0;
        }

        if (this.parallaxOffsets["layer5"] <= -containerWidth) {
          this.parallaxOffsets["layer5"] = 0;
        }

        if (this.parallaxOffsetGround <= -containerWidth) {
          this.parallaxOffsetGround = 0;
        }
      }, 20);
    },
  },

  mounted() {
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
      'Layer_5', 'Layer_3', 'Layer_4',
      'Layer_2_morning', 'Layer_1_day',
      'Layer_5_night', 'Layer_3_night', 'Layer_4_night', 'Layer_2_night', 'Layer_1_night',
      'Layer_5_sakura', 'Layer_3_sakura', 'Layer_4_sakura', 'Layer_2_sakura', 'Layer_1_sakura'
    ].map(name => require(`@/assets/${name}.png`)), this.startGame);

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
      this.parallaxLayerSpeeds["layer3"] += 0.01;
      this.parallaxLayerSpeeds["layer2"] += 0.01;
      this.parallaxLayerSpeeds["layer4"] += 0.01;
      this.parallaxLayerSpeeds["layer5"] += 0.01;

      setTimeout(addObstacle, (500 + Math.random() * 2000) + 0.05);
    };
    addObstacle();
    setInterval(this.gameLoop, 15)
    this.animateCharacter();
    this.parallaxAnimation();
    this.animateNinja();
    this.checkTimeOfDay()
    this.playBackgroundMusic();
    window.addEventListener('keydown', this.handleKeyDown);
  }
})
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
}

.game-wrapper {
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-image: url('../assets/bg-grad.jpg');
  background-repeat: no-repeat;
  background-size: cover;
}

.main {
  width: 1280px;
  height: 700px;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
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
