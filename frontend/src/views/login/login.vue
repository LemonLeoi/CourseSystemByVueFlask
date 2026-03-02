<template>
  <div class="teacher-login">
    <div class="login-container">
      <div class="login-header">
        <h1>教师登录</h1>
        <p>欢迎回来，请登录您的账号</p>
      </div>
      <form class="login-form" @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">用户名</label>
          <input 
            type="text" 
            id="username" 
            v-model="formData.username" 
            placeholder="请输入用户名" 
            required
          />
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input 
            type="password" 
            id="password" 
            v-model="formData.password" 
            placeholder="请输入密码" 
            required
          />
        </div>
        <div class="form-group remember">
          <input type="checkbox" id="remember" v-model="formData.remember" />
          <label for="remember">记住我</label>
        </div>
        <button type="submit" class="login-btn" :disabled="isLoading">
          {{ isLoading ? '登录中...' : '登录' }}
        </button>
        <div class="form-footer">
          <a href="#" class="forgot-password">忘记密码？</a>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

// 表单数据
const formData = ref({
  username: '',
  password: '',
  remember: false
});

// 加载状态
const isLoading = ref(false);

// 登录处理
const handleLogin = async () => {
  isLoading.value = true;
  try {
    // 模拟登录请求
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // 简单的登录验证（实际项目中应该调用API）
    if (formData.value.username && formData.value.password) {
      // 保存登录状态（实际项目中应该使用localStorage或cookie）
      localStorage.setItem('teacherLoggedIn', 'true');
      localStorage.setItem('teacherUsername', formData.value.username);
      
      // 跳转到首页
      router.push('/admin');
    } else {
      alert('请输入用户名和密码');
    }
  } catch (error) {
    console.error('登录失败:', error);
    alert('登录失败，请重试');
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
@import '../../styles/common/variables.css';
@import '../../styles/login/TeacherLogin.css';
</style>