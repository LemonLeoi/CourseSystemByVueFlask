<template>
  <div class="analysis-process-visualizer">
    
    <!-- 分析步骤时间线 -->
    <div class="process-timeline">
      <div 
        v-for="(step, index) in processSteps" 
        :key="index"
        class="timeline-item"
        :class="{ 'active': currentStep === index, 'completed': index < currentStep }"
      >
        <div class="timeline-dot">{{ index + 1 }}</div>
        <div class="timeline-content">
          <h5 class="step-title">{{ step.title }}</h5>
          <p class="step-description">{{ step.description }}</p>
          <div v-if="step.details" class="step-details">
            <button 
              class="details-toggle"
              @click="toggleDetails(index)"
            >
              {{ showDetails[index] ? '收起详情' : '查看详情' }}
            </button>
            <div v-if="showDetails[index]" class="details-content">
              <pre>{{ JSON.stringify(step.details, null, 2) }}</pre>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 数据流程图 -->
    <div v-if="dataFlow" class="data-flow">
      <h5 class="flow-title">数据流程图</h5>
      <div class="flow-diagram">
        <div class="flow-nodes">
          <div 
            v-for="(node, nodeIndex) in dataFlow.nodes" 
            :key="nodeIndex"
            class="flow-node"
            :class="node.type"
            :style="getNodeStyle(nodeIndex, dataFlow.nodes.length)"
            @mouseenter="hoveredNode = nodeIndex"
            @mouseleave="hoveredNode = null"
          >
            <div class="node-content">
              <div class="node-title">{{ node.name }}</div>
              <div v-if="node.description" class="node-description">{{ node.description }}</div>
            </div>
          </div>
        </div>
        <div class="flow-connections">
          <div 
            v-for="(connection, connIndex) in dataFlow.connections" 
            :key="connIndex"
            class="flow-connection"
            :class="{ 'hovered': hoveredNode === connection.from || hoveredNode === connection.to }"
            :style="getConnectionStyle(connection, dataFlow.nodes)"
          >
            <div class="connection-arrow"></div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 计算过程 -->
    <div v-if="calculations" class="calculations">
      <h5 class="calculations-title">计算过程</h5>
      <div class="calculation-steps">
        <div 
          v-for="(calculation, calcIndex) in calculations" 
          :key="calcIndex"
          class="calculation-step"
        >
          <div class="calc-header">
            <span class="calc-step">{{ calcIndex + 1 }}</span>
            <span class="calc-name">{{ calculation.name }}</span>
          </div>
          <div class="calc-formula">{{ calculation.formula }}</div>
          <div class="calc-result">{{ calculation.result }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue';

export default {
  name: 'AnalysisProcessVisualizer',
  props: {
    processSteps: {
      type: Array,
      default: () => []
    },
    currentStep: {
      type: Number,
      default: 0
    },
    dataFlow: {
      type: Object,
      default: null
    },
    calculations: {
      type: Array,
      default: () => []
    }
  },
  setup(props) {
    const showDetails = ref({});
    const hoveredNode = ref(null);
    
    const toggleDetails = (index) => {
      showDetails.value[index] = !showDetails.value[index];
    };
    
    // 计算节点样式
    const getNodeStyle = (index, totalNodes) => {
      const diagramWidth = 500;
      const nodeWidth = 120;
      const nodeHeight = 80;
      const padding = 20;
      
      // 水平排列节点
      const x = padding + (diagramWidth - 2 * padding - nodeWidth) / (totalNodes - 1) * index;
      const y = 60;
      
      return {
        left: x + 'px',
        top: y + 'px',
        width: nodeWidth + 'px',
        height: nodeHeight + 'px'
      };
    };
    
    // 计算连接样式
    const getConnectionStyle = (connection, nodes) => {
      const nodeWidth = 120;
      const nodeHeight = 80;
      const padding = 20;
      const diagramWidth = 500;
      
      const fromIndex = connection.from || 0;
      const toIndex = connection.to || 1;
      
      const fromX = padding + (diagramWidth - 2 * padding - nodeWidth) / (nodes.length - 1) * fromIndex + nodeWidth;
      const fromY = 60 + nodeHeight / 2;
      const toX = padding + (diagramWidth - 2 * padding - nodeWidth) / (nodes.length - 1) * toIndex;
      const toY = 60 + nodeHeight / 2;
      
      const distance = toX - fromX;
      const angle = Math.atan2(toY - fromY, distance) * 180 / Math.PI;
      
      return {
        left: fromX + 'px',
        top: fromY + 'px',
        width: distance + 'px',
        height: '2px',
        transform: `rotate(${angle}deg)`
      };
    };
    
    return {
      showDetails,
      toggleDetails,
      hoveredNode,
      getNodeStyle,
      getConnectionStyle
    };
  }
};
</script>

<style scoped>
.analysis-process-visualizer {
  background: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #eee;
}

/* 时间线样式 */
.process-timeline {
  position: relative;
  padding-left: 30px;
}

.process-timeline::before {
  content: '';
  position: absolute;
  left: 14px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: #e0e0e0;
}

.timeline-item {
  position: relative;
  margin-bottom: 20px;
  padding-left: 20px;
}

.timeline-dot {
  position: absolute;
  left: -30px;
  top: 2px;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  color: #666;
  transition: all 0.3s ease;
}

.timeline-item.completed .timeline-dot {
  background: #52c41a;
  color: white;
}

.timeline-item.active .timeline-dot {
  background: #1890ff;
  color: white;
  transform: scale(1.1);
  box-shadow: 0 0 0 4px rgba(24, 144, 255, 0.1);
}

.step-title {
  margin: 0 0 5px 0;
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

.step-description {
  margin: 0 0 10px 0;
  font-size: 14px;
  color: #666;
  line-height: 1.5;
}

.step-details {
  margin-top: 10px;
  background: white;
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #e0e0e0;
}

.details-toggle {
  background: #f0f0f0;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.details-toggle:hover {
  background: #e0e0e0;
}

.details-content {
  margin-top: 10px;
  max-height: 300px;
  overflow-y: auto;
  background: #fafafa;
  padding: 10px;
  border-radius: 4px;
}

.details-content pre {
  margin: 0;
  font-size: 12px;
  white-space: pre-wrap;
  word-wrap: break-word;
}

/* 数据流程图样式 */
.data-flow {
  margin-top: 30px;
}

.flow-title {
  margin: 0 0 15px 0;
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

.flow-diagram {
  position: relative;
  height: 200px;
  background: white;
  border-radius: 4px;
  padding: 20px;
  border: 1px solid #e0e0e0;
  overflow: hidden;
}

.flow-nodes {
  position: relative;
  z-index: 2;
  width: 100%;
  height: 100%;
}

.flow-node {
  position: absolute;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  color: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  border: 2px solid transparent;
}

.flow-node:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
}

.flow-node.source {
  background: linear-gradient(135deg, #1890ff, #40a9ff);
}

.flow-node.process {
  background: linear-gradient(135deg, #faad14, #ffc53d);
}

.flow-node.result {
  background: linear-gradient(135deg, #52c41a, #73d13d);
}

.node-content {
  padding: 10px;
  width: 100%;
}

.node-title {
  font-weight: 600;
  margin-bottom: 5px;
}

.node-description {
  font-size: 12px;
  opacity: 0.9;
  line-height: 1.3;
}

.flow-connections {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1;
}

.flow-connection {
  position: absolute;
  background: #e0e0e0;
  transform-origin: left center;
  transition: all 0.3s ease;
  height: 2px;
}

.flow-connection::before {
  content: '';
  position: absolute;
  top: 50%;
  right: 0;
  transform: translateY(-50%);
  width: 0;
  height: 0;
  border-left: 8px solid #e0e0e0;
  border-top: 4px solid transparent;
  border-bottom: 4px solid transparent;
}

.flow-connection.hovered {
  background: #1890ff;
  height: 3px;
}

.flow-connection.hovered::before {
  border-left-color: #1890ff;
}

.connection-arrow {
  position: absolute;
  top: 50%;
  right: -8px;
  transform: translateY(-50%);
  width: 0;
  height: 0;
  border-left: 8px solid #e0e0e0;
  border-top: 4px solid transparent;
  border-bottom: 4px solid transparent;
  transition: all 0.3s ease;
}

.flow-connection.hovered .connection-arrow {
  border-left-color: #1890ff;
  transform: translateY(-50%) scale(1.2);
}

/* 计算过程样式 */
.calculations {
  margin-top: 30px;
}

.calculations-title {
  margin: 0 0 15px 0;
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

.calculation-step {
  background: white;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 10px;
  border: 1px solid #e0e0e0;
}

.calc-header {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.calc-step {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #1890ff;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
  margin-right: 10px;
}

.calc-name {
  font-weight: 500;
  color: #333;
}

.calc-formula {
  margin-bottom: 5px;
  font-family: 'Courier New', Courier, monospace;
  font-size: 14px;
  color: #666;
  background: #fafafa;
  padding: 5px;
  border-radius: 4px;
}

.calc-result {
  font-weight: 500;
  color: #333;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .analysis-process-visualizer {
    padding: 15px;
  }
  
  .process-title {
    font-size: 16px;
  }
  
  .step-title {
    font-size: 14px;
  }
  
  .step-description {
    font-size: 13px;
  }
  
  .flow-diagram {
    height: 150px;
    padding: 10px;
  }
  
  .flow-node {
    font-size: 12px;
    padding: 8px 12px;
  }
  
  .flow-node.source {
    top: 10px;
    left: 10px;
  }
  
  .flow-node.process {
    top: 10px;
    left: 120px;
  }
  
  .flow-node.result {
    top: 10px;
    left: 230px;
  }
  
  .calculation-step {
    padding: 10px;
  }
  
  .calc-formula {
    font-size: 12px;
  }
}

@media (max-width: 480px) {
  .analysis-process-visualizer {
    padding: 10px;
  }
  
  .process-title {
    font-size: 14px;
  }
  
  .process-timeline {
    padding-left: 25px;
  }
  
  .timeline-dot {
    width: 24px;
    height: 24px;
    font-size: 12px;
  }
  
  .step-title {
    font-size: 13px;
  }
  
  .step-description {
    font-size: 12px;
  }
  
  .flow-diagram {
    height: 120px;
  }
  
  .flow-node {
    font-size: 10px;
    padding: 6px 10px;
  }
  
  .flow-node.source {
    left: 5px;
  }
  
  .flow-node.process {
    left: 90px;
  }
  
  .flow-node.result {
    left: 175px;
  }
}
</style>