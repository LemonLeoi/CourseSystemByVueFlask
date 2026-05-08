<template>
  <div class="course-table-container">
    <div class="table-responsive">
      <table class="table table-bordered">
        <thead class="table-primary">
          <tr>
            <th>节次/时间</th>
            <th v-for="day in weekDays" :key="day">{{ day }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="timeSlot in timeSlots" :key="timeSlot.id">
            <td>{{ timeSlot.name }}</td>
            <td 
              v-for="day in weekDays" 
              :key="day" 
              @click="handleCellClick(day, timeSlot.id)"
            >
              <div v-if="getCourse(day, timeSlot.id)" class="course-cell">
                <div class="course-name">{{ getCourse(day, timeSlot.id)?.name }}</div>
                <div v-if="mode === 'student'" class="course-teacher">
                  {{ getCourse(day, timeSlot.id)?.teacher }}
                </div>
                <div v-if="mode === 'teacher'" class="course-class">
                  {{ getCourse(day, timeSlot.id)?.className }}
                </div>
                <div class="course-classroom">
                  {{ getCourse(day, timeSlot.id)?.classroom }}
                </div>
              </div>
              <div v-else class="empty-cell">
                点击添加课程
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

// 组件属性
interface Props {
  mode: 'student' | 'teacher';
  courses: any[];
  timeSlots: Array<{ id: number; name: string }>;
  weekDays: string[];
}

const props = defineProps<Props>();

// 组件事件
const emit = defineEmits<{
  (e: 'cellClick', day: string, timeSlotId: number): void;
}>();

// 根据模式获取课程
const getCourse = (day: string, timeSlotId: number) => {
  return props.courses.find(course => {
    return course.day === day && course.timeSlot === timeSlotId;
  });
};

// 处理单元格点击事件
const handleCellClick = (day: string, timeSlotId: number) => {
  emit('cellClick', day, timeSlotId);
};
</script>

<style scoped>
.course-table-container {
  margin-top: 20px;
}

.table-responsive {
  overflow-x: auto;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table-bordered th,
.table-bordered td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: center;
}

.table-primary th {
  background-color: #4a6fa5;
  color: white;
  font-weight: 600;
}

.table-bordered tr:nth-child(even) {
  background-color: #f9f9f9;
}

.table-bordered tr:hover {
  background-color: #f1f1f1;
}

.course-cell {
  padding: 8px;
  background-color: #e3f2fd;
  border-radius: 4px;
  min-height: 60px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 4px;
}

.course-name {
  font-weight: 600;
  color: #4a6fa5;
  font-size: 14px;
}

.course-teacher,
.course-class,
.course-classroom {
  font-size: 12px;
  color: #666;
}

.empty-cell {
  min-height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px dashed #e5e5e5;
  border-radius: 4px;
  color: #999;
  cursor: pointer;
  transition: all 0.3s;
}

.empty-cell:hover {
  border-color: #4a6fa5;
  color: #4a6fa5;
  background-color: rgba(74, 111, 165, 0.05);
}

@media (max-width: 768px) {
  .table-responsive {
    font-size: 12px;
  }
  
  .course-cell {
    min-height: 50px;
    padding: 4px;
  }
  
  .course-name {
    font-size: 12px;
  }
  
  .course-teacher,
  .course-class,
  .course-classroom {
    font-size: 10px;
  }
  
  .empty-cell {
    min-height: 60px;
    font-size: 10px;
  }
}
</style>