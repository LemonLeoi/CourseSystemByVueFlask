<template>
  <div class="class-selector">
    <select 
      v-model="selectedClass" 
      class="filter-select class-select"
      @change="handleClassChange"
      :disabled="isLoading"
    >
      <option value="">请选择班级</option>
      <option v-for="classItem in classes" :key="classItem" :value="classItem">
        {{ classItem }}
      </option>
    </select>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import { studentApi } from '../../services/api/apiService';

export default {
  name: 'ClassSelector',
  props: {
    modelValue: {
      type: String,
      default: ''
    }
  },
  emits: ['update:modelValue', 'change'],
  setup(props, { emit }) {
    const selectedClass = ref(props.modelValue);
    const classes = ref([]);
    const isLoading = ref(false);

    const loadClasses = async () => {
      isLoading.value = true;
      try {
        const data = await studentApi.getClasses();
        const grades = data.grades || ['高一', '高二', '高三'];
        const classNums = data.classes || ['1班', '2班', '3班', '4班', '5班'];
        
        const fullClasses = [];
        grades.forEach(grade => {
          classNums.forEach(classNum => {
            const num = classNum.match(/\d+/) ? classNum.match(/\d+/)[0] : classNum;
            fullClasses.push(`${grade}${num}班`);
          });
        });
        classes.value = fullClasses;
      } catch (error) {
        console.error('获取班级列表失败:', error);
        const grades = ['高一', '高二', '高三'];
        const classNums = ['1班', '2班', '3班', '4班', '5班'];
        const fullClasses = [];
        grades.forEach(grade => {
          classNums.forEach(classNum => {
            const num = classNum.match(/\d+/) ? classNum.match(/\d+/)[0] : classNum;
            fullClasses.push(`${grade}${num}班`);
          });
        });
        classes.value = fullClasses;
      } finally {
        isLoading.value = false;
      }
    };

    const handleClassChange = () => {
      emit('update:modelValue', selectedClass.value);
      emit('change', selectedClass.value);
    };

    watch(() => props.modelValue, (newVal) => {
      selectedClass.value = newVal;
    });

    onMounted(() => {
      loadClasses();
    });

    return {
      selectedClass,
      classes,
      isLoading,
      handleClassChange
    };
  }
};
</script>

<style scoped>
.class-selector {
  display: inline-block;
}

.class-select {
  padding: 10px 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  min-width: 180px;
  background: #fff;
  cursor: pointer;
  transition: all 0.3s ease;
}

.class-select:focus {
  border-color: #409eff;
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(64, 158, 255, 0.25);
}

.class-select:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>