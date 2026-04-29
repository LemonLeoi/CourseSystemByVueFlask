<template>
  <transition name="loading-fade" mode="out-in">
    <div v-if="show" class="loading-animator" :class="[`state-${status}`, size]">
      <div class="loading-container">
        <!-- 加载中状态 -->
        <div v-if="status === 'loading'" class="loading-content">
          <div class="spinner-wrapper">
            <div class="spinner">
              <div class="spinner-circle"></div>
              <div class="spinner-circle delay-1"></div>
              <div class="spinner-circle delay-2"></div>
              <div class="spinner-circle delay-3"></div>
            </div>
            <div class="spinner-core">
              <div class="core-dot"></div>
            </div>
          </div>
          <div class="loading-text">{{ message }}</div>
          <div class="loading-progress">
            <div class="progress-track">
              <div class="progress-fill" :style="{ width: progress + '%' }"></div>
            </div>
            <div class="progress-text">{{ progress }}%</div>
          </div>
          <div class="loading-hints">
            <transition name="hint-fade" mode="out-in">
              <p :key="currentHintIndex" class="hint-text">{{ currentHint }}</p>
            </transition>
          </div>
        </div>

        <!-- 加载成功状态 -->
        <div v-else-if="status === 'success'" class="loading-content success">
          <div class="success-icon">
            <svg class="checkmark" viewBox="0 0 52 52">
              <circle class="checkmark-circle" cx="26" cy="26" r="25" fill="none"/>
              <path class="checkmark-check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
            </svg>
          </div>
          <div class="success-text">{{ successMessage }}</div>
          <div class="success-time" v-if="duration">
            <span class="time-label">耗时</span>
            <span class="time-value">{{ duration }}ms</span>
          </div>
        </div>

        <!-- 加载失败状态 -->
        <div v-else-if="status === 'error'" class="loading-content error">
          <div class="error-icon">
            <svg class="error-circle" viewBox="0 0 52 52">
              <circle class="error-circle-bg" cx="26" cy="26" r="25" fill="none"/>
              <circle class="error-circle-inner" cx="26" cy="26" r="8"/>
            </svg>
            <svg class="error-x" viewBox="0 0 52 52">
              <line x1="18" y1="18" x2="34" y2="34" stroke-width="3"/>
              <line x1="34" y1="18" x2="18" y2="34" stroke-width="3"/>
            </svg>
          </div>
          <div class="error-text">{{ errorMessage }}</div>
          <button v-if="retryable" class="retry-button" @click="handleRetry">
            <span class="retry-icon">↻</span>
            重新加载
          </button>
          <div class="error-details" v-if="errorDetails">
            {{ errorDetails }}
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue';

export default {
  name: 'LoadingAnimator',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    status: {
      type: String,
      default: 'loading',
      validator: (value) => ['loading', 'success', 'error'].includes(value)
    },
    message: {
      type: String,
      default: '正在加载数据...'
    },
    successMessage: {
      type: String,
      default: '数据加载成功'
    },
    errorMessage: {
      type: String,
      default: '数据加载失败'
    },
    errorDetails: {
      type: String,
      default: ''
    },
    retryable: {
      type: Boolean,
      default: true
    },
    size: {
      type: String,
      default: 'medium',
      validator: (value) => ['small', 'medium', 'large'].includes(value)
    },
    hints: {
      type: Array,
      default: () => [
        '正在准备数据...',
        '正在分析成绩...',
        '正在生成报告...',
        '即将完成...'
      ]
    },
    hintInterval: {
      type: Number,
      default: 2000
    },
    autoProgress: {
      type: Boolean,
      default: true
    }
  },
  emits: ['retry'],
  setup(props, { emit }) {
    const progress = ref(0);
    const currentHintIndex = ref(0);
    const duration = ref(0);
    let hintTimer = null;
    let progressTimer = null;
    let startTime = null;

    const currentHint = computed(() => {
      return props.hints[currentHintIndex.value % props.hints.length];
    });

    const startProgressAnimation = () => {
      if (!props.autoProgress) return;

      progress.value = 0;
      startTime = Date.now();

      const progressStep = () => {
        if (progress.value < 90) {
          progress.value += Math.random() * 5 + 2;
          if (progress.value > 90) progress.value = 90;
          progressTimer = setTimeout(progressStep, 200);
        }
      };

      progressTimer = setTimeout(progressStep, 500);
    };

    const setProgressComplete = () => {
      progress.value = 100;
      if (startTime) {
        duration.value = Date.now() - startTime;
      }
    };

    const startHintRotation = () => {
      hintTimer = setInterval(() => {
        currentHintIndex.value++;
      }, props.hintInterval);
    };

    const stopAllTimers = () => {
      if (hintTimer) {
        clearInterval(hintTimer);
        hintTimer = null;
      }
      if (progressTimer) {
        clearTimeout(progressTimer);
        progressTimer = null;
      }
    };

    const handleRetry = () => {
      emit('retry');
    };

    watch(() => props.show, (newVal) => {
      if (newVal) {
        if (props.status === 'loading') {
          progress.value = 0;
          currentHintIndex.value = 0;
          startProgressAnimation();
          startHintRotation();
        }
      } else {
        stopAllTimers();
      }
    });

    watch(() => props.status, (newVal) => {
      if (newVal === 'success') {
        stopAllTimers();
        setProgressComplete();
      } else if (newVal === 'error') {
        stopAllTimers();
      }
    });

    onUnmounted(() => {
      stopAllTimers();
    });

    return {
      progress,
      currentHintIndex,
      currentHint,
      duration,
      handleRetry
    };
  }
};
</script>

<style scoped>
.loading-animator {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  background: #fafafa;
  border-radius: 12px;
  border: 1px solid #e8e8e8;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.loading-animator.small {
  padding: 20px 15px;
}

.loading-animator.large {
  padding: 60px 40px;
}

/* 加载中状态 */
.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  width: 100%;
  max-width: 400px;
}

/* 旋转加载动画 */
.spinner-wrapper {
  position: relative;
  width: 80px;
  height: 80px;
  margin-bottom: 24px;
}

.spinner {
  position: absolute;
  width: 100%;
  height: 100%;
  animation: rotate 2s linear infinite;
}

.spinner-circle {
  position: absolute;
  width: 100%;
  height: 100%;
  border: 3px solid transparent;
  border-top-color: #1890ff;
  border-radius: 50%;
  animation: spinner-circle 1.5s ease-in-out infinite;
}

.spinner-circle.delay-1 {
  border-top-color: #40a9ff;
  animation-delay: 0.1s;
}

.spinner-circle.delay-2 {
  border-top-color: #69c0ff;
  animation-delay: 0.2s;
}

.spinner-circle.delay-3 {
  border-top-color: #91d5ff;
  animation-delay: 0.3s;
}

@keyframes rotate {
  100% {
    transform: rotate(360deg);
  }
}

@keyframes spinner-circle {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.spinner-core {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 24px;
  height: 24px;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(24, 144, 255, 0.3);
}

.core-dot {
  width: 8px;
  height: 8px;
  background: linear-gradient(135deg, #1890ff, #40a9ff);
  border-radius: 50%;
  animation: pulse-dot 1s ease-in-out infinite;
}

@keyframes pulse-dot {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.2);
  }
}

.loading-text {
  font-size: 16px;
  font-weight: 500;
  color: #333;
  margin-bottom: 16px;
}

.loading-progress {
  width: 100%;
  margin-bottom: 16px;
}

.progress-track {
  width: 100%;
  height: 6px;
  background: #e8e8e8;
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #1890ff, #40a9ff);
  border-radius: 3px;
  transition: width 0.3s ease;
  position: relative;
}

.progress-fill::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    transparent
  );
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

.progress-text {
  font-size: 12px;
  color: #999;
  text-align: right;
}

.loading-hints {
  min-height: 24px;
}

.hint-text {
  font-size: 14px;
  color: #666;
  margin: 0;
  animation: fadeInUp 0.5s ease;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 成功状态 */
.success-icon {
  width: 80px;
  height: 80px;
  margin-bottom: 24px;
}

.checkmark {
  width: 100%;
  height: 100%;
}

.checkmark-circle {
  stroke: #52c41a;
  stroke-width: 2;
  stroke-dasharray: 166;
  stroke-dashoffset: 166;
  animation: stroke 0.6s cubic-bezier(0.65, 0, 0.45, 1) forwards;
}

.checkmark-check {
  stroke: #52c41a;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-dasharray: 48;
  stroke-dashoffset: 48;
  animation: stroke 0.3s cubic-bezier(0.65, 0, 0.45, 1) 0.4s forwards;
}

@keyframes stroke {
  100% {
    stroke-dashoffset: 0;
  }
}

.success-text {
  font-size: 16px;
  font-weight: 500;
  color: #52c41a;
  margin-bottom: 12px;
}

.success-time {
  font-size: 14px;
  color: #999;
}

.time-label {
  margin-right: 8px;
}

.time-value {
  color: #52c41a;
  font-weight: 500;
}

/* 失败状态 */
.error-icon {
  width: 80px;
  height: 80px;
  margin-bottom: 24px;
  position: relative;
}

.error-circle {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
}

.error-circle-bg {
  stroke: #ff4d4f;
  stroke-width: 2;
  fill: none;
}

.error-circle-inner {
  fill: #ff4d4f;
  animation: error-pulse 1s ease infinite;
}

.error-x {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  animation: error-appear 0.3s ease 0.2s both;
}

.error-x line {
  stroke: #ff4d4f;
  stroke-linecap: round;
}

@keyframes error-pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.1);
  }
}

@keyframes error-appear {
  from {
    opacity: 0;
    transform: scale(0.5) rotate(-45deg);
  }
  to {
    opacity: 1;
    transform: scale(1) rotate(0deg);
  }
}

.error-text {
  font-size: 16px;
  font-weight: 500;
  color: #ff4d4f;
  margin-bottom: 16px;
}

.retry-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 24px;
  background: linear-gradient(135deg, #1890ff, #40a9ff);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(24, 144, 255, 0.3);
}

.retry-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(24, 144, 255, 0.4);
}

.retry-button:active {
  transform: translateY(0);
}

.retry-icon {
  font-size: 16px;
  animation: rotate-retry 1s linear infinite;
}

@keyframes rotate-retry {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.error-details {
  margin-top: 12px;
  padding: 12px;
  background: #fff2f0;
  border: 1px solid #ffccc7;
  border-radius: 6px;
  font-size: 12px;
  color: #ff7875;
  max-width: 100%;
  word-break: break-all;
}

/* 过渡动画 */
.loading-fade-enter-active,
.loading-fade-leave-active {
  transition: all 0.4s ease;
}

.loading-fade-enter-from,
.loading-fade-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

.hint-fade-enter-active,
.hint-fade-leave-active {
  transition: all 0.3s ease;
}

.hint-fade-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.hint-fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .loading-animator {
    padding: 30px 15px;
  }

  .spinner-wrapper {
    width: 60px;
    height: 60px;
  }

  .loading-text,
  .success-text,
  .error-text {
    font-size: 14px;
  }

  .hint-text {
    font-size: 12px;
  }

  .success-icon,
  .error-icon {
    width: 60px;
    height: 60px;
  }
}

@media (max-width: 480px) {
  .loading-animator {
    padding: 20px 10px;
  }

  .spinner-wrapper {
    width: 50px;
    height: 50px;
  }

  .progress-track {
    height: 4px;
  }

  .retry-button {
    padding: 8px 16px;
    font-size: 13px;
  }
}

/* 性能优化 - 使用 GPU 加速 */
.spinner,
.spinner-circle,
.core-dot,
.progress-fill,
.checkmark-circle,
.checkmark-check,
.error-circle-inner,
.error-x line {
  will-change: transform;
  backface-visibility: hidden;
}
</style>