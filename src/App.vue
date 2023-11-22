<template>
  <div class="main" @keydown="handleKeyDown" tabindex="0">
    <h1 class="score">Очки: {{ score }}</h1>
    <div class="game-area">
      <div class="character"
           :style="{ bottom: `${dinoBottom}px`, left: `${dinoLeft}px`, backgroundImage: `url(${characterFrames[frameIndex]})` }"></div>
      <div v-for="(obstacle, index) in obstacles" :key="index" class="obstacle"
           :style="{ bottom: `${obstacle.bottom}px`, left: `${obstacle.left}px`, backgroundImage: 'url(src/assets/spike_1.png)' }"></div>
      <div class="ground"></div>
    </div>
  </div>
</template>

<script lang="ts">
export default {
  data() {
    return {
      dinoBottom: 0 as number,
      dinoLeft: 20 as number,
      isJumping: false as boolean,
      score: 0 as number,
      obstacles: [] as { bottom: number; left: number }[],
      coef: 1 as number,
      characterFrames: [
        'src/assets/run_1.png',
        'src/assets/run_2.png',
        'src/assets/run_3.png',
        'src/assets/run_4.png',
        'src/assets/run_5.png',
        'src/assets/run_6.png',
        'src/assets/run_7.png',
        'src/assets/run_8.png',
      ],
      frameIndex: 0 as number,
    };
  },
  methods: {
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
        }
      }
    },
    checkCollisions() {
      const dino = {
        bottom: this.dinoBottom,
        left: this.dinoLeft,
        right: this.dinoLeft + 30,
        top: this.dinoBottom + 30,
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
    },
    gameLoop() {
      this.moveObstacles();
      this.checkCollisions();
    },
  },
  mounted() {
    this.$el.focus();

    const addObstacle = () => {
      this.obstacles.push({
        bottom: 0,
        left: 1270,
      });
      this.coef += 0.05
      setTimeout(addObstacle, (500 + Math.random() * 2000));
    };
    addObstacle();
    setInterval(this.gameLoop, 15)
    this.animateCharacter();
  },
};
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
  background-image: url(assets/mount1.png);
  background-repeat: no-repeat;
  background-size: cover;
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
  background-image: url(assets/Tile_22.png);
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
}

.character {
  position: absolute;
  width: 120px;
  height: 120px;
  background-size: cover;
}

</style>