<template>
  <div class="visualizer-container">
    <div class="visualizer-header">
      <h3 class="visualizer-title">决策树可视化</h3>
      <div class="visualizer-actions">
        <button class="action-btn" @click="zoomIn">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
        </button>
        <button class="action-btn" @click="zoomOut">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="19" x2="12" y2="5"></line>
          </svg>
        </button>
        <button class="action-btn" @click="resetZoom">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 21l-6-6m2-5a7 7 0 1 1-14 0 7 7 0 0 1 14 0z"></path>
          </svg>
        </button>
      </div>
    </div>
    
    <div class="visualizer-body" ref="chartContainer">
      <div v-if="loading" class="loading-state">
        <svg class="loading-icon" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <path d="M12 6v6l4 2"></path>
        </svg>
        <p>正在生成决策树...</p>
      </div>
      
      <div v-else-if="!visualizationData" class="empty-state">
        <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <polyline points="12 6 12 12 16 14"></polyline>
        </svg>
        <p>暂无数据，请选择班级进行分析</p>
      </div>
      
      <div v-else class="tree-container">
        <svg ref="treeSvg" class="tree-svg" @click="handleSvgClick">
          <defs>
            <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
              <polygon points="0 0, 10 3.5, 0 7" fill="#999"/>
            </marker>
            <marker id="arrowhead-highlight" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
              <polygon points="0 0, 10 3.5, 0 7" fill="#1890ff"/>
            </marker>
            <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
              <feDropShadow dx="2" dy="2" stdDeviation="2" flood-opacity="0.2"/>
            </filter>
          </defs>
          
          <g v-for="(edge, index) in edges" :key="'edge-' + index">
            <path
              :d="edge.path"
              :stroke="edge.highlighted ? '#1890ff' : '#d9d9d9'"
              stroke-width="2"
              fill="none"
              :marker-end="edge.highlighted ? 'url(#arrowhead-highlight)' : 'url(#arrowhead)'"
            />
            <text
              :x="edge.labelX"
              :y="edge.labelY"
              class="edge-label"
              :class="{ 'highlighted': edge.highlighted }"
            >
              {{ edge.label }}
            </text>
          </g>
          
          <g v-for="node in nodes" :key="node.id">
            <g :transform="`translate(${node.x}, ${node.y})`" @click.stop="handleNodeClick(node)">
              <rect
                :width="node.width"
                :height="node.height"
                :x="-node.width / 2"
                :y="-node.height / 2"
                :rx="8"
                :fill="node.isLeaf ? '#f6ffed' : '#e6f7ff'"
                :stroke="node.highlighted ? '#1890ff' : (node.isLeaf ? '#b7eb8f' : '#91d5ff')"
                stroke-width="2"
                :filter="node.selected ? 'url(#shadow)' : ''"
                class="node-rect"
                :class="{ 'selected': node.selected, 'highlighted': node.highlighted }"
              />
              <text
                :y="-8"
                text-anchor="middle"
                class="node-label"
              >{{ node.label }}</text>
              <text
                :y="8"
                text-anchor="middle"
                class="node-info"
              >{{ node.info }}</text>
            </g>
          </g>
        </svg>
      </div>
    </div>
    
    <!-- 节点详情弹窗 -->
    <div v-if="selectedNode" class="node-detail-modal" @click="selectedNode = null">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h4>节点详情</h4>
          <button class="close-btn" @click="selectedNode = null">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <div class="detail-row">
            <span class="detail-label">节点类型</span>
            <span class="detail-value">{{ selectedNode.isLeaf ? '叶子节点' : '分裂节点' }}</span>
          </div>
          <div class="detail-row" v-if="!selectedNode.isLeaf">
            <span class="detail-label">分裂属性</span>
            <span class="detail-value">{{ selectedNode.attributeName }}</span>
          </div>
          <div class="detail-row" v-if="selectedNode.infoGain !== undefined">
            <span class="detail-label">信息增益</span>
            <span class="detail-value">{{ selectedNode.infoGain.toFixed(4) }}</span>
          </div>
          <div class="detail-row" v-if="selectedNode.gainRatio !== undefined">
            <span class="detail-label">信息增益比</span>
            <span class="detail-value">{{ selectedNode.gainRatio.toFixed(4) }}</span>
          </div>
          <div class="detail-row" v-if="selectedNode.entropyBefore !== undefined">
            <span class="detail-label">分裂前熵值</span>
            <span class="detail-value">{{ selectedNode.entropyBefore.toFixed(4) }}</span>
          </div>
          <div class="detail-row" v-if="selectedNode.entropyAfter !== undefined">
            <span class="detail-label">分裂后熵值</span>
            <span class="detail-value">{{ selectedNode.entropyAfter.toFixed(4) }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">样本数量</span>
            <span class="detail-value">{{ selectedNode.sampleCount }}</span>
          </div>
          <div class="detail-row" v-if="selectedNode.classDistribution">
            <span class="detail-label">类别分布</span>
            <div class="distribution-box">
              <div v-for="(count, label) in selectedNode.classDistribution" :key="label" class="distribution-item">
                <span class="dist-label">{{ label }}</span>
                <span class="dist-count">{{ count }}</span>
              </div>
            </div>
          </div>
          <div class="detail-row" v-if="selectedNode.isLeaf">
            <span class="detail-label">预测类别</span>
            <span class="detail-value result">{{ selectedNode.result }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">import { ref, computed, watch, onMounted, nextTick } from 'vue';
interface VisualizationNode {
 id: string;
 label: string;
 type: 'leaf' | 'node';
 depth: number;
 attribute?: number;
 attributeName?: string;
 infoGain?: number;
 gainRatio?: number;
 entropyBefore?: number;
 entropyAfter?: number;
 sampleCount: number;
 classDistribution?: Record<string, number>;
 result?: string;
 children?: Array<{
 id: string;
 parent_id: string;
 edge_label: string;
 data: VisualizationNode;
 }>;
}
interface TreeNode {
 id: string;
 x: number;
 y: number;
 width: number;
 height: number;
 label: string;
 info: string;
 isLeaf: boolean;
 attributeName?: string;
 infoGain?: number;
 gainRatio?: number;
 entropyBefore?: number;
 entropyAfter?: number;
 sampleCount: number;
 classDistribution?: Record<string, number>;
 result?: string;
 selected: boolean;
 highlighted: boolean;
 children?: TreeNode[];
}
interface Edge {
 path: string;
 label: string;
 labelX: number;
 labelY: number;
 highlighted: boolean;
}
const props = defineProps<{
 visualizationData: VisualizationNode | null;
}>();
const chartContainer = ref<HTMLElement | null>(null);
const treeSvg = ref<SVGSVGElement | null>(null);
const loading = ref(false);
const selectedNode = ref<TreeNode | null>(null);
const scale = ref(1);
const translateX = ref(0);
const translateY = ref(0);
const nodes = ref<TreeNode[]>([]);
const edges = ref<Edge[]>([]);
const nodeWidth = 140;
const nodeHeight = 60;
const horizontalGap = 180;
const verticalGap = 120;
const layoutTree = (data: VisualizationNode, x: number, y: number, depth: number): {
 node: TreeNode;
 edges: Edge[];
 totalWidth: number;
} => {
 const isLeaf = data.type === 'leaf';
 let label = '';
 let info = '';
 if (isLeaf) {
 label = `类别: ${data.result}`;
 info = `样本: ${data.sampleCount}`;
 }
 else {
 label = data.attributeName || `属性${data.attribute}`;
 info = data.infoGain !== undefined ? `增益: ${data.infoGain.toFixed(4)}` : '';
 }
 const childrenData: TreeNode[] = [];
 const childrenEdges: Edge[] = [];
 let childrenTotalWidth = 0;
 if (!isLeaf && data.children) {
 const childCount = data.children.length;
 const childWidth = horizontalGap;
 childrenTotalWidth = Math.max(childCount * childWidth, nodeWidth);
 const startX = x - childrenTotalWidth / 2 + nodeWidth / 2;
 data.children.forEach((child, index) => {
 const childX = startX + index * childWidth;
 const childY = y + verticalGap;
 const result = layoutTree(child.data, childX, childY, depth + 1);
 childrenData.push(result.node);
 childrenEdges.push(...result.edges);
 // 添加边
 const edgePath = `M ${x} ${y + nodeHeight / 2} C ${x} ${y + verticalGap / 2}, ${childX} ${y + verticalGap / 2}, ${childX} ${childY - nodeHeight / 2}`;
 childrenEdges.push({
 path: edgePath,
 label: child.edge_label,
 labelX: (x + childX) / 2,
 labelY: (y + nodeHeight / 2 + childY - nodeHeight / 2) / 2 - 10,
 highlighted: false
 });
 });
 }
 const node: TreeNode = {
 id: data.id,
 x,
 y,
 width: nodeWidth,
 height: nodeHeight,
 label,
 info,
 isLeaf,
 attributeName: data.attributeName,
 infoGain: data.infoGain,
 gainRatio: data.gainRatio,
 entropyBefore: data.entropyBefore,
 entropyAfter: data.entropyAfter,
 sampleCount: data.sampleCount,
 classDistribution: data.classDistribution,
 result: data.result,
 selected: false,
 highlighted: false,
 children: childrenData.length > 0 ? childrenData : undefined
 };
 return {
 node,
 edges: [node, ...childrenData.flat(Infinity), ...childrenEdges].filter((n): n is TreeNode => 'width' in n),
 totalWidth: Math.max(childrenTotalWidth, nodeWidth)
 };
};
const buildTree = (data: VisualizationNode) => {
 const container = chartContainer.value;
 if (!container)
 return;
 const containerWidth = container.clientWidth;
 const result = layoutTree(data, containerWidth / 2, 50, 0);
 const allNodes: TreeNode[] = [];
 const collectNodes = (node: TreeNode) => {
 allNodes.push(node);
 if (node.children) {
 node.children.forEach(collectNodes);
 }
 };
 collectNodes(result.node);
 nodes.value = allNodes;
 edges.value = result.edges.filter((e): e is Edge => 'path' in e);
};
const handleNodeClick = (node: TreeNode) => {
 // 取消其他节点的选中状态
 nodes.value.forEach(n => n.selected = false);
 node.selected = true;
 selectedNode.value = node;
 // 高亮路径
 const pathNodes = findPathToRoot(node);
 nodes.value.forEach(n => n.highlighted = pathNodes.includes(n.id));
 edges.value.forEach(e => {
 const edgeHighlighted = pathNodes.some((id, index) => index < pathNodes.length - 1 &&
 isEdgeConnecting(edges.value, id, pathNodes[index + 1]));
 e.highlighted = edgeHighlighted;
 });
};
const findPathToRoot = (node: TreeNode): string[] => {
 const path = [node.id];
 // 简化：由于我们没有父节点引用，这里只高亮当前节点
 return path;
};
const isEdgeConnecting = (edges: Edge[], fromId: string, toId: string): boolean => {
 return false;
};
const handleSvgClick = () => {
 nodes.value.forEach(n => {
 n.selected = false;
 n.highlighted = false;
 });
 edges.value.forEach(e => e.highlighted = false);
 selectedNode.value = null;
};
const zoomIn = () => {
 scale.value = Math.min(scale.value * 1.2, 3);
 updateTransform();
};
const zoomOut = () => {
 scale.value = Math.max(scale.value / 1.2, 0.3);
 updateTransform();
};
const resetZoom = () => {
 scale.value = 1;
 translateX.value = 0;
 translateY.value = 0;
 updateTransform();
};
const updateTransform = () => {
 if (treeSvg.value) {
 treeSvg.value.style.transform = `translate(${translateX.value}px, ${translateY.value}px) scale(${scale.value})`;
 }
};
watch(() => props.visualizationData, (newData) => {
 if (newData) {
 loading.value = true;
 nextTick(() => {
 buildTree(newData);
 loading.value = false;
 });
 }
}, { immediate: true });
onMounted(() => {
 if (props.visualizationData) {
 buildTree(props.visualizationData);
 }
});
</script>

<style scoped>
.visualizer-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.visualizer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #eee;
}

.visualizer-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.visualizer-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  background: #f5f5f5;
  border: 1px solid #d9d9d9;
  border-radius: 6px;
  padding: 6px 10px;
  cursor: pointer;
  color: #666;
  transition: all 0.2s;
}

.action-btn:hover {
  background: #e8f4fd;
  border-color: #1890ff;
  color: #1890ff;
}

.visualizer-body {
  flex: 1;
  overflow: hidden;
  position: relative;
}

.loading-state, .empty-state {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  color: #999;
}

.loading-icon {
  animation: spin 1s linear infinite;
  color: #1890ff;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.loading-state p, .empty-state p {
  margin-top: 12px;
  font-size: 14px;
}

.tree-container {
  width: 100%;
  height: 100%;
  overflow: auto;
  background: #fafafa;
}

.tree-svg {
  width: 100%;
  height: auto;
  min-height: 100%;
  cursor: pointer;
}

.node-rect {
  cursor: pointer;
  transition: all 0.2s;
}

.node-rect:hover {
  stroke-width: 3;
}

.node-rect.selected {
  stroke-width: 3;
}

.node-label {
  font-size: 12px;
  font-weight: 500;
  fill: #333;
}

.node-info {
  font-size: 11px;
  fill: #666;
}

.edge-label {
  font-size: 11px;
  fill: #999;
  background: #fff;
  padding: 2px 6px;
  border-radius: 4px;
}

.edge-label.highlighted {
  fill: #1890ff;
  font-weight: 500;
}

.node-detail-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: #fff;
  border-radius: 12px;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #eee;
}

.modal-header h4 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  padding: 4px;
}

.close-btn:hover {
  color: #666;
}

.modal-body {
  padding: 20px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
}

.detail-row:last-child {
  border-bottom: none;
}

.detail-label {
  font-size: 13px;
  color: #666;
  font-weight: 500;
}

.detail-value {
  font-size: 13px;
  color: #333;
  font-weight: 600;
}

.detail-value.result {
  color: #52c41a;
}

.distribution-box {
  display: flex;
  gap: 12px;
}

.distribution-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 12px;
  background: #f5f5f5;
  border-radius: 6px;
}

.dist-label {
  font-size: 12px;
  color: #666;
}

.dist-count {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}
</style>