<template>
  <div class="decision-tree-path">
    <div class="tree-header">
      <div class="header-icon">🌳</div>
      <div class="header-content">
        <h3 class="tree-title">决策路径分析</h3>
        <p class="tree-subtitle">Decision Path Analysis</p>
      </div>
      <div class="path-length">
        <span>路径长度: {{ currentPath?.path.length || 0 }} 个节点</span>
      </div>
    </div>
    
    <!-- 路径选择器 -->
    <div v-if="paths && paths.length > 1" class="path-selector">
      <div class="selector-label">选择分析路径:</div>
      <div class="path-tabs">
        <button
          v-for="path in paths"
          :key="path.id"
          :class="['path-tab', { active: selectedPathId === path.id }]"
          @click="selectPath(path.id)"
        >
          <span class="tab-icon">{{ getPathIcon(path.impact) }}</span>
          <span class="tab-name">{{ path.name }}</span>
          <span class="tab-confidence">{{ path.confidence }}%</span>
        </button>
      </div>
    </div>
    
    <!-- 当前路径信息 -->
    <div v-if="currentPath" class="path-info">
      <div class="info-row">
        <span class="info-label">置信度:</span>
        <span class="info-value confidence">{{ currentPath.confidence }}%</span>
      </div>
      <div class="info-row">
        <span class="info-label">影响程度:</span>
        <span :class="['info-value', 'impact', currentPath.impact.toLowerCase().replace('中', '')]">{{ currentPath.impact }}</span>
      </div>
      <div class="info-row full-width">
        <span class="info-label">建议:</span>
        <span class="info-value recommendation">{{ currentPath.recommendation }}</span>
      </div>
    </div>
    
    <!-- 缩放控制栏 -->
    <div class="zoom-controls">
      <span class="zoom-label">缩放:</span>
      <input 
        type="range" 
        class="zoom-slider" 
        :min="MIN_SCALE * 100" 
        :max="MAX_SCALE * 100" 
        :step="SCALE_STEP * 100"
        :value="scale * 100"
        @input="handleZoomSliderChange"
      />
      <span class="zoom-level">{{ Math.round(scale * 100) }}%</span>
      <button class="zoom-btn" @click="resetZoom">
        <span>⟲</span>
      </button>
    </div>
    
    <!-- 固定尺寸的SVG容器 -->
    <div 
      ref="containerRef"
      class="tree-container"
    >
      <div 
        class="tree-content"
        :style="{
          transform: `scale(${scale})`,
          transformOrigin: 'center center',
          transition: 'transform 0.1s ease-out'
        }"
      >
        <svg 
          ref="svgRef" 
          class="tree-svg"
          :viewBox="`0 0 ${svgWidth} ${svgHeight}`"
          preserveAspectRatio="xMidYMid meet"
        >
          <!-- 连接线 -->
          <g class="connections">
            <path
              v-for="(connection, index) in connections"
              :key="'conn-' + index"
              :d="connection.path"
              class="connection-line"
              :class="{ 'highlight': hoveredNode === connection.from || hoveredNode === connection.to }"
              @mouseenter="hoveredNode = connection.from"
              @mouseleave="hoveredNode = null"
            />
            <polygon
              v-for="(connection, index) in connections"
              :key="'arrow-' + index"
              :points="connection.arrowPoints"
              class="connection-arrow"
              :class="{ 'highlight': hoveredNode === connection.from || hoveredNode === connection.to }"
            />
          </g>
          
          <!-- 分支选项节点 -->
          <g
            v-for="(branchGroup, groupIndex) in branchOptionsGroups"
            :key="'branch-group-' + groupIndex"
          >
            <g
              v-for="(option, optIndex) in branchGroup.options"
              :key="'branch-' + groupIndex + '-' + optIndex"
              :transform="`translate(${branchGroup.x + getOptionsOffset(branchGroup.options, optIndex)}, ${branchGroup.y})`"
              class="branch-option"
              :class="{ 'selected': option.value === branchGroup.selectedValue }"
              @click="selectBranchOption(groupIndex, option.value)"
            >
              <rect
                :width="option.width"
                height="24"
                rx="4"
                class="branch-option-bg"
              />
              <text
                :x="option.width / 2"
                y="16"
                class="branch-option-text"
                text-anchor="middle"
              >
                {{ option.value }}
              </text>
            </g>
          </g>
          
          <!-- 主节点 -->
          <g
            v-for="(node, index) in nodes"
            :key="'node-' + index"
            :transform="`translate(${node.x}, ${node.y})`"
            class="tree-node"
            :class="{ 
              'hovered': hoveredNode === index,
              'root': index === 0,
              'leaf': node.isLeaf,
              'decision': !node.isLeaf
            }"
            @mouseenter="hoveredNode = index"
            @mouseleave="hoveredNode = null"
          >
            <rect
              :width="nodeWidth"
              :height="nodeHeight"
              :rx="nodeRx"
              :ry="nodeRy"
              class="node-background"
            />
            
            <text
              v-if="node.significance"
              class="node-significance"
              :x="nodeWidth - 8"
              :y="12"
              text-anchor="end"
            >
              {{ node.significance }}
            </text>
            
            <text
              class="node-label"
              :x="nodeWidth / 2"
              :y="nodeHeight / 2 - 8"
              text-anchor="middle"
            >
              {{ node.label }}
            </text>
            
            <text
              v-if="node.value"
              class="node-value"
              :x="nodeWidth / 2"
              :y="nodeHeight / 2 + 10"
              text-anchor="middle"
            >
              {{ node.value }}
            </text>
          </g>
          
          <!-- 分支标签 -->
          <g v-for="(label, index) in branchLabels" :key="'label-' + index">
            <rect
              :x="label.x"
              :y="label.y"
              :width="label.width"
              :height="label.height"
              rx="4"
              class="branch-label-bg"
            />
            <text
              :x="label.x + label.width / 2"
              :y="label.y + label.height / 2 + 4"
              class="branch-label-text"
              text-anchor="middle"
            >
              {{ label.text }}
            </text>
          </g>
        </svg>
      </div>
    </div>
    
    <!-- 影响因素量化评估 -->
    <div v-if="factorImpact && factorImpact.length > 0" class="factor-impact-section">
      <h4 class="impact-title">📊 影响因素量化评估</h4>
      <div class="factor-list">
        <div
          v-for="factor in factorImpact"
          :key="factor.factor"
          class="factor-item"
        >
          <div class="factor-header">
            <span class="factor-name">{{ factor.factor }}</span>
            <span :class="['factor-sign', factor.positive === true ? 'positive' : factor.positive === false ? 'negative' : 'neutral']">
              {{ factor.positive === true ? '+' : factor.positive === false ? '-' : '~' }}
            </span>
          </div>
          <div class="factor-metrics">
            <div class="metric-item">
              <span class="metric-label">权重</span>
              <span class="metric-value">{{ factor.weight.toFixed(4) }}</span>
            </div>
            <div class="metric-item">
              <span class="metric-label">影响分</span>
              <span class="metric-value">{{ factor.impactScore }}</span>
            </div>
            <div class="metric-item">
              <span class="metric-label">显著性</span>
              <span :class="['metric-value', getSignificanceClass(factor.significance)]">{{ factor.significance }}</span>
            </div>
          </div>
          <div class="impact-bar">
            <div 
              class="impact-fill"
              :style="{ width: factor.impactScore + '%' }"
              :class="factor.positive === true ? 'positive' : factor.positive === false ? 'negative' : 'neutral'"
            ></div>
          </div>
          <p class="factor-desc">{{ factor.description }}</p>
        </div>
      </div>
    </div>
    
    <div class="legend">
      <div class="legend-item">
        <div class="legend-node root"></div>
        <span>根节点</span>
      </div>
      <div class="legend-item">
        <div class="legend-node decision"></div>
        <span>决策节点</span>
      </div>
      <div class="legend-item">
        <div class="legend-node leaf"></div>
        <span>叶子节点</span>
      </div>
    </div>
    
    <div v-if="!currentPath || currentPath.path.length === 0" class="empty-state">
      <div class="empty-icon">🌳</div>
      <p class="empty-text">暂无决策路径数据</p>
      <p class="empty-hint">请先进行成绩分析以获取决策路径</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue';

export interface TreePathNode {
  label: string;
  value?: string;
  isLeaf: boolean;
  splitCriteria?: string;
  branchOptions?: { value: string; nextNodeId?: number }[];
  infoGain?: number;
  significance?: string;
}

export interface DecisionTreeBranch {
  id: string;
  name: string;
  description: string;
  path: TreePathNode[];
  confidence: number;
  impact: string;
  recommendation: string;
}

export interface FactorImpact {
  factor: string;
  weight: number;
  impactScore: number;
  significance: string;
  positive: boolean | null;
  description: string;
}

const props = defineProps<{
  nodes?: TreePathNode[];
  paths?: DecisionTreeBranch[];
  factorImpact?: FactorImpact[];
}>();

const selectedPathId = ref<string | null>(null);
const hoveredNode = ref<number | null>(null);
const scale = ref(1);

const MIN_SCALE = 0.5;
const MAX_SCALE = 2;
const SCALE_STEP = 0.1;

const currentPath = computed(() => {
  if (props.paths && props.paths.length > 0) {
    if (selectedPathId.value) {
      return props.paths.find(p => p.id === selectedPathId.value);
    }
    return props.paths[0];
  }
  return null;
});

const nodeWidth = 160;
const nodeHeight = 55;
const nodeRx = 8;
const nodeRy = 8;
const verticalGap = 60;
const horizontalPadding = 80;
const branchOptionBaseWidth = 80;
const branchOptionCharWidth = 10;

const svgWidth = computed(() => {
  // 计算所有分支选项所需的宽度
  let maxBranchOptionsWidth = 0;
  const pathNodes = currentPath.value?.path || props.nodes || [];
  pathNodes.forEach(node => {
    if (node.branchOptions && node.branchOptions.length > 0) {
      const totalWidth = node.branchOptions.reduce((sum, opt) => {
        const textWidth = Math.max(branchOptionBaseWidth, opt.value.length * branchOptionCharWidth + 20);
        return sum + textWidth + 10; // 加上间距
      }, 0);
      maxBranchOptionsWidth = Math.max(maxBranchOptionsWidth, totalWidth);
    }
  });
  
  // 确保足够的宽度容纳主节点和分支选项
  const requiredWidth = nodeWidth + horizontalPadding * 2 + maxBranchOptionsWidth + 50;
  return Math.max(600, requiredWidth);
});

const svgHeight = computed(() => {
  const pathNodes = currentPath.value?.path || props.nodes || [];
  if (pathNodes.length === 0) return 180;
  return (pathNodes.length - 1) * (verticalGap + 10) + nodeHeight + 60;
});

const nodes = computed(() => {
  const pathNodes = currentPath.value?.path || props.nodes || [];
  return pathNodes.map((node, index) => ({
    ...node,
    x: (svgWidth.value - nodeWidth) / 2,
    y: index * (verticalGap + 10) + 30
  }));
});

const connections = computed(() => {
  const result = [];
  const pathNodes = nodes.value;
  for (let i = 0; i < pathNodes.length - 1; i++) {
    const fromNode = pathNodes[i];
    const toNode = pathNodes[i + 1];
    
    const startX = fromNode.x + nodeWidth / 2;
    const startY = fromNode.y + nodeHeight;
    const endX = toNode.x + nodeWidth / 2;
    const endY = toNode.y;
    
    const controlY = (startY + endY) / 2;
    const path = `M ${startX} ${startY} Q ${startX} ${controlY} ${endX} ${endY - 10}`;
    
    const arrowSize = 8;
    const angle = Math.atan2(endY - startY, endX - startX);
    const arrowPoints = [
      endX, endY - 5,
      endX - arrowSize * Math.cos(angle - Math.PI / 6), endY - 5 - arrowSize * Math.sin(angle - Math.PI / 6),
      endX - arrowSize * Math.cos(angle + Math.PI / 6), endY - 5 - arrowSize * Math.sin(angle + Math.PI / 6)
    ].join(' ');
    
    result.push({
      from: i,
      to: i + 1,
      path,
      arrowPoints
    });
  }
  return result;
});

const branchLabels = computed(() => {
  const result = [];
  const pathNodes = currentPath.value?.path || props.nodes || [];
  const pathNodesWithPos = nodes.value;
  
  for (let i = 0; i < pathNodes.length - 1; i++) {
    const fromNode = pathNodesWithPos[i];
    const toNode = pathNodesWithPos[i + 1];
    
    const labelX = toNode.x - 80;
    const labelY = (fromNode.y + nodeHeight + toNode.y) / 2 - 15;
    const labelWidth = 160;
    const labelHeight = 30;
    
    const splitCriteria = pathNodes[i].splitCriteria || '';
    
    result.push({
      x: labelX,
      y: labelY,
      width: labelWidth,
      height: labelHeight,
      text: splitCriteria
    });
  }
  return result;
});

const branchOptionsGroups = computed(() => {
  const result = [];
  const pathNodes = currentPath.value?.path || props.nodes || [];
  const pathNodesWithPos = nodes.value;
  
  pathNodesWithPos.forEach((node, index) => {
    if (node.branchOptions && node.branchOptions.length > 1) {
      const nextNode = pathNodesWithPos[index + 1];
      if (nextNode) {
        const groupY = (node.y + nodeHeight + nextNode.y) / 2 - 12;
        const groupX = node.x + nodeWidth + 15;
        
        // 为每个选项计算合适的宽度
        const optionsWithWidth = node.branchOptions.map(opt => ({
          ...opt,
          width: Math.max(branchOptionBaseWidth, opt.value.length * branchOptionCharWidth + 20)
        }));
        
        result.push({
          x: groupX,
          y: groupY,
          options: optionsWithWidth,
          selectedValue: pathNodes[index]?.value?.replace('是', '').replace('?', '') || ''
        });
      }
    }
  });
  
  return result;
});

const selectPath = (pathId: string) => {
  selectedPathId.value = pathId;
  scale.value = 1;
};

const selectBranchOption = (groupIndex: number, value: string) => {
  console.log('Selected branch option:', groupIndex, value);
};

const getOptionsOffset = (options: any[], index: number) => {
  let offset = 0;
  for (let i = 0; i < index; i++) {
    offset += (options[i].width || branchOptionBaseWidth) + 10;
  }
  return offset;
};

const getPathIcon = (impact: string) => {
  switch (impact) {
    case '高': return '🔥';
    case '中高': return '💡';
    case '中等': return '📊';
    default: return '📈';
  }
};

const getSignificanceClass = (significance: string) => {
  if (significance.includes('< 0.001')) return 'high-significant';
  if (significance.includes('< 0.01')) return 'significant';
  if (significance.includes('< 0.05')) return 'moderate';
  return 'not-significant';
};

const zoomIn = () => {
  if (scale.value < MAX_SCALE) {
    scale.value = Math.min(MAX_SCALE, scale.value + SCALE_STEP);
  }
};

const zoomOut = () => {
  if (scale.value > MIN_SCALE) {
    scale.value = Math.max(MIN_SCALE, scale.value - SCALE_STEP);
  }
};

const resetZoom = () => {
  scale.value = 1;
};

const handleZoomSliderChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  scale.value = parseFloat(target.value) / 100;
};

onMounted(() => {
  if (props.paths && props.paths.length > 0 && !selectedPathId.value) {
    selectedPathId.value = props.paths[0].id;
  }
});

onUnmounted(() => {
});

watch(() => props.paths, () => {
  if (props.paths && props.paths.length > 0 && !selectedPathId.value) {
    selectedPathId.value = props.paths[0].id;
  }
}, { immediate: true });

const svgRef = ref<SVGSVGElement | null>(null);
</script>

<style scoped>
.decision-tree-path {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  padding: 20px;
}

.tree-header {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.header-icon {
  font-size: 24px;
  margin-right: 10px;
}

.header-content {
  flex: 1;
}

.tree-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

.tree-subtitle {
  margin: 2px 0 0 0;
  font-size: 12px;
  color: #9ca3af;
}

.path-length {
  background: #f3f4f6;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 12px;
  color: #6b7280;
}

.path-selector {
  margin-bottom: 16px;
  padding: 12px;
  background: #f8fafc;
  border-radius: 8px;
}

.selector-label {
  font-size: 12px;
  color: #6b7280;
  margin-bottom: 8px;
}

.path-tabs {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.path-tab {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 12px;
}

.path-tab:hover {
  border-color: #667eea;
  background: #f0f5ff;
}

.path-tab.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: #667eea;
  color: #fff;
}

.tab-icon {
  font-size: 14px;
}

.tab-name {
  font-weight: 500;
}

.tab-confidence {
  opacity: 0.8;
  font-size: 11px;
}

.path-info {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  padding: 12px 16px;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border-radius: 8px;
  margin-bottom: 16px;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 6px;
}

.info-row.full-width {
  width: 100%;
}

.info-label {
  font-size: 12px;
  color: #059669;
  font-weight: 500;
}

.info-value {
  font-size: 13px;
  font-weight: 600;
}

.info-value.confidence {
  color: #16a34a;
}

.info-value.impact.high {
  color: #dc2626;
}

.info-value.impact.medium {
  color: #f59e0b;
}

.info-value.recommendation {
  color: #065f46;
  font-weight: 500;
}

.zoom-controls {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  margin-bottom: 12px;
  padding: 8px 12px;
  background: #f8fafc;
  border-radius: 6px;
}

.zoom-label {
  font-size: 12px;
  font-weight: 500;
  color: #6b7280;
  margin-right: 8px;
}

.zoom-slider {
  flex: 1;
  max-width: 200px;
  height: 6px;
  -webkit-appearance: none;
  appearance: none;
  background: #e5e7eb;
  border-radius: 3px;
  cursor: pointer;
}

.zoom-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 16px;
  height: 16px;
  background: #667eea;
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
  transition: all 0.2s ease;
}

.zoom-slider::-webkit-slider-thumb:hover {
  background: #7c3aed;
  box-shadow: 0 2px 6px rgba(102, 126, 234, 0.3);
}

.zoom-slider::-moz-range-thumb {
  width: 16px;
  height: 16px;
  background: #667eea;
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
  transition: all 0.2s ease;
}

.zoom-slider::-moz-range-thumb:hover {
  background: #7c3aed;
  box-shadow: 0 2px 6px rgba(102, 126, 234, 0.3);
}

.zoom-level {
  font-size: 12px;
  font-weight: 500;
  color: #6b7280;
  min-width: 50px;
  text-align: center;
  margin-left: 8px;
}

.zoom-btn {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  color: #4b5563;
  transition: all 0.2s ease;
  margin-left: 8px;
}

.zoom-btn:hover {
  background: #667eea;
  border-color: #667eea;
  color: #fff;
}

.tree-container {
  background: #fafafa;
  border-radius: 8px;
  padding: 16px;
  min-height: 280px;
  max-height: 500px;
  overflow: auto;
  border: 2px solid #e5e7eb;
  position: relative;
}

.tree-container::before {
  content: '';
  position: absolute;
  top: 4px;
  left: 4px;
  right: 4px;
  bottom: 4px;
  border: 1px dashed #d1d5db;
  border-radius: 4px;
  pointer-events: none;
}

.tree-content {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 240px;
}

.tree-svg {
  width: auto;
  height: auto;
  min-width: 100%;
}

.connection-line {
  fill: none;
  stroke: #cbd5e1;
  stroke-width: 2;
  transition: all 0.3s ease;
}

.connection-line.highlight {
  stroke: #667eea;
  stroke-width: 3;
}

.connection-arrow {
  fill: #cbd5e1;
  transition: all 0.3s ease;
}

.connection-arrow.highlight {
  fill: #667eea;
}

.branch-option {
  cursor: pointer;
  transition: all 0.3s ease;
}

.branch-option:hover .branch-option-bg {
  fill: #e0e7ff;
}

.branch-option.selected .branch-option-bg {
  fill: #667eea;
}

.branch-option.selected .branch-option-text {
  fill: #fff;
}

.branch-option-bg {
  fill: #f3f4f6;
  stroke: #e5e7eb;
  stroke-width: 1;
  transition: all 0.3s ease;
}

.branch-option-text {
  fill: #6b7280;
  font-size: 11px;
  font-weight: 500;
  pointer-events: none;
  white-space: nowrap;
}

.tree-node {
  cursor: pointer;
  transition: all 0.3s ease;
}

.tree-node:hover,
.tree-node.hovered {
  filter: drop-shadow(0 4px 12px rgba(102, 126, 234, 0.3));
}

.node-background {
  transition: all 0.3s ease;
}

.tree-node.root .node-background {
  fill: #667eea;
}

.tree-node.decision .node-background {
  fill: #f59e0b;
}

.tree-node.leaf .node-background {
  fill: #10b981;
}

.node-label {
  fill: #fff;
  font-size: 13px;
  font-weight: 600;
  pointer-events: none;
}

.node-value {
  fill: rgba(255, 255, 255, 0.9);
  font-size: 11px;
  pointer-events: none;
}

.node-significance {
  fill: rgba(255, 255, 255, 0.8);
  font-size: 9px;
  pointer-events: none;
}

.branch-label-bg {
  fill: #fff;
  stroke: #e5e7eb;
  stroke-width: 1;
}

.branch-label-text {
  fill: #374151;
  font-size: 10px;
  font-weight: 500;
}

.factor-impact-section {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #e5e7eb;
}

.impact-title {
  margin: 0 0 12px 0;
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
}

.factor-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.factor-item {
  padding: 12px;
  background: #f8fafc;
  border-radius: 8px;
}

.factor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.factor-name {
  font-size: 13px;
  font-weight: 600;
  color: #1f2937;
}

.factor-sign {
  font-size: 14px;
  font-weight: 700;
}

.factor-sign.positive {
  color: #10b981;
}

.factor-sign.negative {
  color: #ef4444;
}

.factor-sign.neutral {
  color: #9ca3af;
}

.factor-metrics {
  display: flex;
  gap: 16px;
  margin-bottom: 8px;
}

.metric-item {
  display: flex;
  gap: 4px;
}

.metric-label {
  font-size: 11px;
  color: #6b7280;
}

.metric-value {
  font-size: 11px;
  font-weight: 600;
  color: #374151;
}

.metric-value.high-significant {
  color: #dc2626;
}

.metric-value.significant {
  color: #f59e0b;
}

.metric-value.moderate {
  color: #3b82f6;
}

.metric-value.not-significant {
  color: #9ca3af;
}

.impact-bar {
  height: 6px;
  background: #e5e7eb;
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 8px;
}

.impact-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.5s ease;
}

.impact-fill.positive {
  background: linear-gradient(90deg, #10b981, #34d399);
}

.impact-fill.negative {
  background: linear-gradient(90deg, #ef4444, #f87171);
}

.impact-fill.neutral {
  background: linear-gradient(90deg, #9ca3af, #d1d5db);
}

.factor-desc {
  margin: 0;
  font-size: 12px;
  color: #6b7280;
  line-height: 1.5;
}

.legend {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #e5e7eb;
}

.legend-item {
  display: flex;
  align-items: center;
  font-size: 12px;
  color: #6b7280;
}

.legend-node {
  width: 16px;
  height: 16px;
  border-radius: 4px;
  margin-right: 8px;
}

.legend-node.root {
  background: #667eea;
}

.legend-node.decision {
  background: #f59e0b;
}

.legend-node.leaf {
  background: #10b981;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 20px;
  text-align: center;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-text {
  margin: 0 0 8px 0;
  font-size: 16px;
  color: #6b7280;
}

.empty-hint {
  margin: 0;
  font-size: 14px;
  color: #9ca3af;
}

@media (max-width: 768px) {
  .decision-tree-path {
    padding: 16px;
  }
  
  .tree-container {
    padding: 10px;
    max-height: 350px;
  }
  
  .tree-header {
    flex-wrap: wrap;
  }
  
  .path-length {
    margin-top: 8px;
    order: 3;
  }
  
  .legend {
    gap: 16px;
  }
  
  .factor-metrics {
    flex-wrap: wrap;
  }
  
  .zoom-controls {
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .tree-title {
    font-size: 14px;
  }
  
  .legend {
    flex-wrap: wrap;
  }
  
  .legend-item {
    margin-bottom: 8px;
  }
  
  .path-info {
    flex-direction: column;
  }
  
  .zoom-hint {
    display: none;
  }
}
</style>