<template>
  <div class="main" :class="{ 'night-mode': isNightMode, 'sakura': isSakura }" @keydown="handleKeyDown" tabindex="0"
       :style="{ backgroundPosition: `${parallaxOffsetLayer5}px 0, ${parallaxOffsetLayer3}px 0, ${parallaxOffsetLayer4}px 0, ${parallaxOffsetLayer2}px 0, 0 0` }">
    <audio id="backgroundMusic" loop>
      <source src="@/assets/soundtrack.mp3" type="audio/mp3">
      Your browser does not support the audio tag.
    </audio>

    <h1 class="score">Очки: {{ score }}</h1>
    <div class="game-area">
      <div class="character"
           :style="{ bottom: `${dinoBottom}px`, left: `${dinoLeft}px`, backgroundImage: `url(${characterFrames[frameIndex]})` }">
      </div>
      <div v-for="(obstacle, index) in obstacles" :key="index" class="obstacle"
           :style="{ bottom: `${obstacle.bottom}px`, left: `${obstacle.left}px`, backgroundImage: `url(${require('@/assets/spike_1.png')})` }"></div>
      <div class="ground" :style="{ backgroundPosition: `${parallaxOffsetGround}px 0` }"></div>
    </div>
  </div>
</template>

<script lang="ts">
import {defineComponent} from 'vue'


export default defineComponent({
  data() {
    return {
      dinoBottom: 0 as number,
      dinoLeft: 20 as number,
      isJumping: false as boolean,
      score: 0 as number,
      obstacles: [] as { bottom: number; left: number }[],
      coef: 1 as number,
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
      frameIndex: 0 as number,
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
      isSakura: false as boolean,
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
        this.frameIndex = (this.frameIndex + 1) % this.characterFrames.length;
      }, 100);
    },
    handleKeyDown(event: KeyboardEvent) {
      if (event.key === " " && !this.isJumping) {
        this.isJumping = true;
        this.jump();
      }
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
      for (let i = 0; i < this.obstacles.length; i++) {
        this.obstacles[i].left -= (5 * this.coef);
        if (this.obstacles[i].left < -7) {
          this.obstacles.splice(i, 1);
          this.score++;
          this.checkNightMode();
          this.checkSakura();
        }
      }
    },
    checkCollisions() {
      const dino = {
        bottom: this.dinoBottom,
        left: this.dinoLeft,
        right: this.dinoLeft + 50,
        top: this.dinoBottom + 50,
      };

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
          alert("Game Over! Your score: " + this.score);
          window.location.reload();
          this.resetGame();
        }
      }
    },

    resetGame() {
      this.obstacles = [];
      this.score = 0;
      this.isNightMode = false;
      this.$el.classList.remove('night-mode');
    },
    gameLoop() {
      this.moveObstacles();
      this.checkCollisions();
    },

    checkSakura() {
      if (this.score >= 25 && this.score < 50 && !this.isSakura) {
        this.isSakura = true;
      } else if (this.score >= 50) {
        this.isSakura = false;
      }
    },

    checkNightMode() {
      if (this.score >= 50 && this.score < 100 && !this.isNightMode) {
        this.isNightMode = true;
      } else if (this.score > 100) {
        this.isNightMode = false;
      }
    },
    parallaxAnimation() {
      setInterval(() => {
        this.parallaxOffsetLayer3 -= this.parallaxLayer3Speed;
        this.parallaxOffsetLayer4 += this.parallaxLayer4Speed;
        this.parallaxOffsetLayer2 += this.parallaxLayer2Speed;
        this.parallaxOffsetLayer5 -= this.parallaxLayer5Speed;
        this.parallaxOffsetGround -= 5 * this.coef;
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
    const addObstacle = () => {
      this.obstacles.push({
        bottom: 0,
        left: 1270,
      });
      this.coef += 0.05
      this.parallaxLayer3Speed += 0.01
      this.parallaxLayer2Speed += 0.01
      this.parallaxLayer4Speed += 0.01
      this.parallaxLayer5Speed += 0.01
      setTimeout(addObstacle, (500 + Math.random() * 2000) + 0.05);
    };
    addObstacle();
    setInterval(this.gameLoop, 15)
    this.animateCharacter();
    this.parallaxAnimation();
  },
})
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
}

.main {
  width: 1280px;
  height: 700px;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-image: url('../assets/Layer_5.png'), url('../assets/Layer_3.png'), url('../assets/Layer_4.png'), url('../assets/Layer_2.png'), url('../assets/Layer_1.png');
  background-repeat: repeat;
  background-size: cover;
  transition: background-image 2s ease;
}

.main.night-mode {
  background-image: url('../assets/Layer_5_night.png'), url('../assets/Layer_3_night.png'), url('../assets/Layer_4_night.png'), url('../assets/Layer_2_night.png'), url('../assets/Layer_1_night.png');
}

.main.sakura {
  background-image: url('../assets/Layer_5_sakura.png'), url('../assets/Layer_3_sakura.png'), url('../assets/Layer_4_sakura.png'), url('../assets/Layer_2_sakura.png'), url('../assets/Layer_1_sakura.png');
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
  width: 100%;
  background-image: url('../assets/Tile_22.png');
  background-repeat: repeat;
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
  width: 140px;
  height: 140px;
  background-size: cover;
}

</style>