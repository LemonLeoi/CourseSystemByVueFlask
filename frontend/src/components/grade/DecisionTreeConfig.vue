<template>
  <div class="config-panel">
    <!-- 操作提示 -->
    <div v-if="showToast" class="toast" :class="toastType">
      <svg v-if="toastType === 'success'" class="toast-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="20 6 9 17 4 12"></polyline>
      </svg>
      <svg v-else-if="toastType === 'error'" class="toast-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="15" y1="9" x2="9" y2="15"></line>
        <line x1="9" y1="9" x2="15" y2="15"></line>
      </svg>
      <span class="toast-message">{{ toastMessage }}</span>
    </div>
    
    <div class="panel-header">
      <div class="header-info">
        <h3 class="panel-title">决策树参数配置</h3>
        <p class="panel-subtitle">调整参数以优化决策树模型的分类效果</p>
      </div>
      <button class="reset-btn" @click="resetConfig" title="重置为默认值">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="23 4 23 10 17 10"></polyline>
          <polyline points="1 20 1 14 7 14"></polyline>
          <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
        </svg>
      </button>
    </div>
    
    <!-- 基础参数区 -->
    <div class="section">
      <div class="section-header">
        <h4 class="section-title">
          <span class="section-icon">⚙️</span>
          基础参数
        </h4>
        <span class="section-hint">影响决策树的整体结构</span>
      </div>
      
      <!-- 最大树深度 -->
      <div class="param-item" :class="{ 'has-error': validationErrors.maxDepth }">
        <div class="param-header">
          <label class="param-label">最大树深度</label>
          <div class="param-value-wrapper">
            <span class="param-value">{{ config.maxDepth }}</span>
            <span class="param-unit">层</span>
          </div>
          <span class="tooltip-wrapper">
            <svg class="tooltip-icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M12 16v-4"></path>
              <path d="M12 8h.01"></path>
            </svg>
            <span class="tooltip-text">决策树的最大层级深度，值越小树越浅，避免过拟合</span>
          </span>
        </div>
        <div class="param-controls">
          <input 
            type="number" 
            v-model.number="config.maxDepth" 
            :min="1" 
            :max="20" 
            class="number-input-small"
          />
          <input 
            type="range" 
            v-model.number="config.maxDepth" 
            :min="1" 
            :max="20" 
            class="slider"
          />
        </div>
        <div class="range-labels">
          <span>1 (浅)</span>
          <span>20 (深)</span>
        </div>
        <div v-if="validationErrors.maxDepth" class="error-message">
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="15" y1="9" x2="9" y2="15"></line>
            <line x1="9" y1="9" x2="15" y2="15"></line>
          </svg>
          {{ validationErrors.maxDepth }}
        </div>
      </div>
      
      <!-- 最小分裂样本数 -->
      <div class="param-item" :class="{ 'has-error': validationErrors.minSamplesSplit }">
        <div class="param-header">
          <label class="param-label">最小分裂样本数</label>
          <div class="param-value-wrapper">
            <span class="param-value">{{ config.minSamplesSplit }}</span>
            <span class="param-unit">个</span>
          </div>
          <span class="tooltip-wrapper">
            <svg class="tooltip-icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M12 16v-4"></path>
              <path d="M12 8h.01"></path>
            </svg>
            <span class="tooltip-text">节点分裂所需的最小样本数，值越大生成的树越简单</span>
          </span>
        </div>
        <div class="param-controls">
          <input 
            type="number" 
            v-model.number="config.minSamplesSplit" 
            :min="2" 
            :max="100" 
            class="number-input-small"
          />
          <input 
            type="range" 
            v-model.number="config.minSamplesSplit" 
            :min="2" 
            :max="100" 
            class="slider"
          />
        </div>
        <div class="range-labels">
          <span>2 (细)</span>
          <span>100 (粗)</span>
        </div>
        <div v-if="validationErrors.minSamplesSplit" class="error-message">
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="15" y1="9" x2="9" y2="15"></line>
            <line x1="9" y1="9" x2="15" y2="15"></line>
          </svg>
          {{ validationErrors.minSamplesSplit }}
        </div>
      </div>
      
      <!-- 算法选择 -->
      <div class="param-item">
        <div class="param-header">
          <label class="param-label">算法类型</label>
          <span class="tooltip-wrapper">
            <svg class="tooltip-icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M12 16v-4"></path>
              <path d="M12 8h.01"></path>
            </svg>
            <span class="tooltip-text">选择决策树构建算法，ID3使用信息增益，C4.5使用信息增益比</span>
          </span>
        </div>
        <div class="radio-group">
          <label class="radio-label" :class="{ active: config.algorithm === 'ID3' }">
            <input type="radio" v-model="config.algorithm" value="ID3" />
            <span class="radio-circle"></span>
            <span class="radio-text">ID3</span>
            <span class="radio-desc">基于信息增益</span>
          </label>
          <label class="radio-label" :class="{ active: config.algorithm === 'C4.5' }">
            <input type="radio" v-model="config.algorithm" value="C4.5" />
            <span class="radio-circle"></span>
            <span class="radio-text">C4.5</span>
            <span class="radio-desc">基于信息增益比</span>
          </label>
        </div>
      </div>
    </div>
    
    <!-- 高级参数区 -->
    <div class="section">
      <div class="section-header">
        <h4 class="section-title">
          <span class="section-icon">🔧</span>
          高级参数
        </h4>
        <span class="section-hint">精细调整分裂行为</span>
      </div>
      
      <!-- 分裂阈值 -->
      <div class="param-item" :class="{ 'has-error': validationErrors.threshold }">
        <div class="param-header">
          <label class="param-label">分裂阈值</label>
          <div class="param-value-wrapper">
            <span class="param-value">{{ config.threshold.toExponential(4) }}</span>
          </div>
          <span class="tooltip-wrapper">
            <svg class="tooltip-icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M12 16v-4"></path>
              <path d="M12 8h.01"></path>
            </svg>
            <span class="tooltip-text">信息增益的最小阈值，小于此值的节点不再分裂</span>
          </span>
        </div>
        <div class="param-controls">
          <input 
            type="number" 
            v-model.number="config.threshold" 
            :min="0.00001" 
            :max="0.1" 
            step="0.00001"
            class="number-input"
          />
        </div>
        <div class="range-labels">
          <span>0.00001</span>
          <span>0.1</span>
        </div>
        <div v-if="validationErrors.threshold" class="error-message">
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="15" y1="9" x2="9" y2="15"></line>
            <line x1="9" y1="9" x2="15" y2="15"></line>
          </svg>
          {{ validationErrors.threshold }}
        </div>
      </div>
    </div>
    
    <!-- 参数说明卡片 -->
    <div class="info-card">
      <h5 class="info-title">💡 参数配置建议</h5>
      <ul class="info-list">
        <li><strong>最大树深度</strong>：建议初学者使用5-10，过深容易过拟合</li>
        <li><strong>最小分裂样本数</strong>：数据集较小时建议使用较小值</li>
        <li><strong>分裂阈值</strong>：值越小树越复杂，默认值0.0001适合大多数场景</li>
        <li><strong>算法选择</strong>：C4.5对特征值较多的数据集更稳定</li>
      </ul>
    </div>

    <!-- 置信度与信息增益 -->
    <div class="section">
      <div class="section-header">
        <h4 class="section-title">
          <span class="section-icon">🎯</span>
          置信度与信息增益
        </h4>
        <span class="section-hint">控制分析结果的置信度和信息增益</span>
      </div>
      
      <!-- 置信度阈值 -->
      <div class="param-item" :class="{ 'has-error': validationErrors.confidenceThreshold }">
        <div class="param-header">
          <label class="param-label">置信度阈值</label>
          <div class="param-value-wrapper">
            <span class="param-value">{{ config.confidenceThreshold }}</span>
          </div>
          <span class="tooltip-wrapper">
            <svg class="tooltip-icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M12 16v-4"></path>
              <path d="M12 8h.01"></path>
            </svg>
            <span class="tooltip-text">低于此置信度的结论将被忽略</span>
          </span>
        </div>
        <div class="param-controls">
          <input 
            type="number" 
            v-model.number="config.confidenceThreshold" 
            :min="0" 
            :max="1" 
            step="0.01"
            class="number-input-small"
          />
          <input 
            type="range" 
            v-model.number="config.confidenceThreshold" 
            :min="0" 
            :max="1" 
            step="0.01"
            class="slider"
          />
        </div>
        <div class="range-labels">
          <span>0</span>
          <span>1</span>
        </div>
        <div v-if="validationErrors.confidenceThreshold" class="error-message">
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="15" y1="9" x2="9" y2="15"></line>
            <line x1="9" y1="9" x2="15" y2="15"></line>
          </svg>
          {{ validationErrors.confidenceThreshold }}
        </div>
      </div>
      
      <!-- 最小置信度要求 -->
      <div class="param-item" :class="{ 'has-error': validationErrors.minConfidence }">
        <div class="param-header">
          <label class="param-label">最小置信度要求</label>
          <div class="param-value-wrapper">
            <span class="param-value">{{ config.minConfidence }}</span>
          </div>
          <span class="tooltip-wrapper">
            <svg class="tooltip-icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M12 16v-4"></path>
              <path d="M12 8h.01"></path>
            </svg>
            <span class="tooltip-text">分析结果的最小置信度要求</span>
          </span>
        </div>
        <div class="param-controls">
          <input 
            type="number" 
            v-model.number="config.minConfidence" 
            :min="0" 
            :max="1" 
            step="0.01"
            class="number-input-small"
          />
          <input 
            type="range" 
            v-model.number="config.minConfidence" 
            :min="0" 
            :max="1" 
            step="0.01"
            class="slider"
          />
        </div>
        <div class="range-labels">
          <span>0</span>
          <span>1</span>
        </div>
        <div v-if="validationErrors.minConfidence" class="error-message">
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="15" y1="9" x2="9" y2="15"></line>
            <line x1="9" y1="9" x2="15" y2="15"></line>
          </svg>
          {{ validationErrors.minConfidence }}
        </div>
      </div>
      
      <!-- 最小信息增益要求 -->
      <div class="param-item" :class="{ 'has-error': validationErrors.minInfoGain }">
        <div class="param-header">
          <label class="param-label">最小信息增益要求</label>
          <div class="param-value-wrapper">
            <span class="param-value">{{ config.minInfoGain }}</span>
          </div>
          <span class="tooltip-wrapper">
            <svg class="tooltip-icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M12 16v-4"></path>
              <path d="M12 8h.01"></path>
            </svg>
            <span class="tooltip-text">节点分裂所需的最小信息增益</span>
          </span>
        </div>
        <div class="param-controls">
          <input 
            type="number" 
            v-model.number="config.minInfoGain" 
            :min="0" 
            :max="1" 
            step="0.01"
            class="number-input-small"
          />
          <input 
            type="range" 
            v-model.number="config.minInfoGain" 
            :min="0" 
            :max="1" 
            step="0.01"
            class="slider"
          />
        </div>
        <div class="range-labels">
          <span>0</span>
          <span>1</span>
        </div>
        <div v-if="validationErrors.minInfoGain" class="error-message">
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="15" y1="9" x2="9" y2="15"></line>
            <line x1="9" y1="9" x2="15" y2="15"></line>
          </svg>
          {{ validationErrors.minInfoGain }}
        </div>
      </div>
    </div>

    <!-- 节点分裂与停止条件 -->
    <div class="section">
      <div class="section-header">
        <h4 class="section-title">
          <span class="section-icon">⚙️</span>
          节点分裂与停止条件
        </h4>
        <span class="section-hint">控制决策树分裂和停止的策略</span>
      </div>
      
      <!-- 分裂方向策略 -->
      <div class="param-item">
        <div class="param-header">
          <label class="param-label">分裂方向策略</label>
          <span class="tooltip-wrapper">
            <svg class="tooltip-icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M12 16v-4"></path>
              <path d="M12 8h.01"></path>
            </svg>
            <span class="tooltip-text">选择节点分裂时的方向策略</span>
          </span>
        </div>
        <div class="radio-group">
          <label class="radio-label" :class="{ active: config.splitDirection === 'max_gain' }">
            <input type="radio" v-model="config.splitDirection" value="max_gain" />
            <span class="radio-circle"></span>
            <span class="radio-text">最大增益</span>
            <span class="radio-desc">总是选择信息增益最大的方向</span>
          </label>
          <label class="radio-label" :class="{ active: config.splitDirection === 'balanced' }">
            <input type="radio" v-model="config.splitDirection" value="balanced" />
            <span class="radio-circle"></span>
            <span class="radio-text">平衡</span>
            <span class="radio-desc">平衡考虑各分支的样本数</span>
          </label>
          <label class="radio-label" :class="{ active: config.splitDirection === 'random' }">
            <input type="radio" v-model="config.splitDirection" value="random" />
            <span class="radio-circle"></span>
            <span class="radio-text">随机</span>
            <span class="radio-desc">随机选择分裂方向</span>
          </label>
        </div>
      </div>
      
      <!-- 停止条件 -->
      <div class="param-item">
        <div class="param-header">
          <label class="param-label">停止条件</label>
          <span class="tooltip-wrapper">
            <svg class="tooltip-icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M12 16v-4"></path>
              <path d="M12 8h.01"></path>
            </svg>
            <span class="tooltip-text">决策树停止生长的条件</span>
          </span>
        </div>
        <div class="radio-group">
          <label class="radio-label" :class="{ active: config.stopCriteria === 'all' }">
            <input type="radio" v-model="config.stopCriteria" value="all" />
            <span class="radio-circle"></span>
            <span class="radio-text">全部</span>
            <span class="radio-desc">所有条件都满足时停止</span>
          </label>
          <label class="radio-label" :class="{ active: config.stopCriteria === 'max_depth' }">
            <input type="radio" v-model="config.stopCriteria" value="max_depth" />
            <span class="radio-circle"></span>
            <span class="radio-text">最大深度</span>
            <span class="radio-desc">仅根据最大深度停止</span>
          </label>
          <label class="radio-label" :class="{ active: config.stopCriteria === 'min_samples' }">
            <input type="radio" v-model="config.stopCriteria" value="min_samples" />
            <span class="radio-circle"></span>
            <span class="radio-text">最小样本</span>
            <span class="radio-desc">仅根据最小样本数停止</span>
          </label>
          <label class="radio-label" :class="{ active: config.stopCriteria === 'info_gain' }">
            <input type="radio" v-model="config.stopCriteria" value="info_gain" />
            <span class="radio-circle"></span>
            <span class="radio-text">信息增益</span>
            <span class="radio-desc">仅根据信息增益停止</span>
          </label>
        </div>
      </div>
      
      <!-- 缺失值处理策略 -->
      <div class="param-item">
        <div class="param-header">
          <label class="param-label">缺失值处理策略</label>
          <span class="tooltip-wrapper">
            <svg class="tooltip-icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M12 16v-4"></path>
              <path d="M12 8h.01"></path>
            </svg>
            <span class="tooltip-text">数据存在缺失值时的处理方式</span>
          </span>
        </div>
        <div class="radio-group">
          <label class="radio-label" :class="{ active: config.missingValueStrategy === 'mean_mode' }">
            <input type="radio" v-model="config.missingValueStrategy" value="mean_mode" />
            <span class="radio-circle"></span>
            <span class="radio-text">均值/众数</span>
            <span class="radio-desc">用均值或众数填充缺失值</span>
          </label>
          <label class="radio-label" :class="{ active: config.missingValueStrategy === 'drop' }">
            <input type="radio" v-model="config.missingValueStrategy" value="drop" />
            <span class="radio-circle"></span>
            <span class="radio-text">删除</span>
            <span class="radio-desc">删除包含缺失值的样本</span>
          </label>
          <label class="radio-label" :class="{ active: config.missingValueStrategy === 'ignore' }">
            <input type="radio" v-model="config.missingValueStrategy" value="ignore" />
            <span class="radio-circle"></span>
            <span class="radio-text">忽略</span>
            <span class="radio-desc">忽略缺失值继续处理</span>
          </label>
        </div>
      </div>
    </div>
    
    <!-- 得分率配置区 -->
    <div class="section">
      <div class="section-header">
        <h4 class="section-title">
          <span class="section-icon">📊</span>
          得分率设置
        </h4>
        <span class="section-hint">配置各科总分及权重，用于计算得分率</span>
      </div>
      
      <!-- 是否使用得分率 -->
      <div class="param-item">
        <div class="param-header">
          <label class="param-label">使用得分率评估</label>
        </div>
        <div class="radio-group">
          <label class="radio-label" :class="{ active: scoreRateConfig.use_score_rate }">
            <input type="radio" v-model="scoreRateConfig.use_score_rate" :value="true" />
            <span class="radio-circle"></span>
            <span class="radio-text">是</span>
            <span class="radio-desc">按得分率进行评估</span>
          </label>
          <label class="radio-label" :class="{ active: !scoreRateConfig.use_score_rate }">
            <input type="radio" v-model="scoreRateConfig.use_score_rate" :value="false" />
            <span class="radio-circle"></span>
            <span class="radio-text">否</span>
            <span class="radio-desc">按原始分数进行评估</span>
          </label>
        </div>
      </div>
      
      <!-- 语言科目总分 -->
      <div class="param-item">
        <div class="param-header">
          <label class="param-label">语言科目总分（语文、数学、外语）</label>
          <div class="param-value-wrapper">
            <span class="param-value">{{ scoreRateConfig.language_total }}</span>
            <span class="param-unit">分</span>
          </div>
          <span class="tooltip-wrapper">
            <svg class="tooltip-icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M12 16v-4"></path>
              <path d="M12 8h.01"></path>
            </svg>
            <span class="tooltip-text">语文、数学、外语三科的单科满分分值</span>
          </span>
        </div>
        <div class="param-controls">
          <input 
            type="number" 
            v-model.number="scoreRateConfig.language_total" 
            :min="0" 
            :max="300" 
            class="number-input-small"
          />
          <input 
            type="range" 
            v-model.number="scoreRateConfig.language_total" 
            :min="0" 
            :max="300" 
            class="slider"
          />
        </div>
        <div class="range-labels">
          <span>0</span>
          <span>300</span>
        </div>
      </div>
      
      <!-- 理科科目总分 -->
      <div class="param-item">
        <div class="param-header">
          <label class="param-label">理科科目总分（物理、化学、生物等）</label>
          <div class="param-value-wrapper">
            <span class="param-value">{{ scoreRateConfig.science_total }}</span>
            <span class="param-unit">分</span>
          </div>
          <span class="tooltip-wrapper">
            <svg class="tooltip-icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M12 16v-4"></path>
              <path d="M12 8h.01"></path>
            </svg>
            <span class="tooltip-text">物理、化学、生物等理科科目单科满分分值</span>
          </span>
        </div>
        <div class="param-controls">
          <input 
            type="number" 
            v-model.number="scoreRateConfig.science_total" 
            :min="0" 
            :max="300" 
            class="number-input-small"
          />
          <input 
            type="range" 
            v-model.number="scoreRateConfig.science_total" 
            :min="0" 
            :max="300" 
            class="slider"
          />
        </div>
        <div class="range-labels">
          <span>0</span>
          <span>300</span>
        </div>
      </div>
      
      <!-- 得分率计算公式说明 -->
      <div class="info-card small">
        <h5 class="info-title">📝 得分率计算公式</h5>
        <div class="formula">
          <p>得分率 = (实际得分 ÷ 科目总分) × 100%</p>
        </div>
        <div class="example">
          <p><strong>示例：</strong>语文135分（满分150分）→ 得分率 = (135 ÷ 150) × 100% = 90%</p>
        </div>
      </div>
    </div>
    
    <!-- 班级类型配置区 -->
    <div class="section">
      <div class="section-header">
        <h4 class="section-title">
          <span class="section-icon">🏫</span>
          班级类型分类标准
        </h4>
        <span class="section-hint">定义基础薄弱班、普通班、重点班的划分规则</span>
      </div>
      
      <!-- 基础薄弱班评分率阈值 -->
      <div class="param-item" :class="{ 'has-error': classTypeErrors.thresholdLow }">
        <div class="param-header">
          <label class="param-label">基础薄弱班评分率阈值</label>
          <div class="param-value-wrapper">
            <span class="param-value">{{ classTypeConfig.thresholdLow }}</span>
            <span class="param-unit">%</span>
          </div>
          <span class="tooltip-wrapper">
            <svg class="tooltip-icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M12 16v-4"></path>
              <path d="M12 8h.01"></path>
            </svg>
            <span class="tooltip-text">评分率低于此值的班级将被划分为基础薄弱班</span>
          </span>
        </div>
        <div class="param-controls">
          <input 
            type="number" 
            v-model.number="classTypeConfig.thresholdLow" 
            :min="0" 
            :max="100" 
            class="number-input-small"
          />
          <input 
            type="range" 
            v-model.number="classTypeConfig.thresholdLow" 
            :min="0" 
            :max="100" 
            class="slider"
          />
        </div>
        <div class="range-labels">
          <span>0%</span>
          <span>100%</span>
        </div>
        <div v-if="classTypeErrors.thresholdLow" class="error-message">
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="15" y1="9" x2="9" y2="15"></line>
            <line x1="9" y1="9" x2="15" y2="15"></line>
          </svg>
          {{ classTypeErrors.thresholdLow }}
        </div>
      </div>
      
      <!-- 重点班评分率阈值 -->
      <div class="param-item" :class="{ 'has-error': classTypeErrors.thresholdHigh }">
        <div class="param-header">
          <label class="param-label">重点班评分率阈值</label>
          <div class="param-value-wrapper">
            <span class="param-value">{{ classTypeConfig.thresholdHigh }}</span>
            <span class="param-unit">%</span>
          </div>
          <span class="tooltip-wrapper">
            <svg class="tooltip-icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M12 16v-4"></path>
              <path d="M12 8h.01"></path>
            </svg>
            <span class="tooltip-text">评分率高于此值的班级将被划分为重点班</span>
          </span>
        </div>
        <div class="param-controls">
          <input 
            type="number" 
            v-model.number="classTypeConfig.thresholdHigh" 
            :min="0" 
            :max="100" 
            class="number-input-small"
          />
          <input 
            type="range" 
            v-model.number="classTypeConfig.thresholdHigh" 
            :min="0" 
            :max="100" 
            class="slider"
          />
        </div>
        <div class="range-labels">
          <span>0%</span>
          <span>100%</span>
        </div>
        <div v-if="classTypeErrors.thresholdHigh" class="error-message">
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="15" y1="9" x2="9" y2="15"></line>
            <line x1="9" y1="9" x2="15" y2="15"></line>
          </svg>
          {{ classTypeErrors.thresholdHigh }}
        </div>
      </div>
      
      <!-- 分类方法 -->
      <div class="param-item">
        <div class="param-header">
          <label class="param-label">分类方法</label>
          <span class="tooltip-wrapper">
            <svg class="tooltip-icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M12 16v-4"></path>
              <path d="M12 8h.01"></path>
            </svg>
            <span class="tooltip-text">选择使用平均评分率或中位数评分率进行班级类型划分</span>
          </span>
        </div>
        <div class="radio-group">
          <label class="radio-label" :class="{ active: classTypeConfig.method === 'average' }">
            <input type="radio" v-model="classTypeConfig.method" value="average" />
            <span class="radio-circle"></span>
            <span class="radio-text">平均评分率</span>
            <span class="radio-desc">使用班级平均评分率</span>
          </label>
          <label class="radio-label" :class="{ active: classTypeConfig.method === 'median' }">
            <input type="radio" v-model="classTypeConfig.method" value="median" />
            <span class="radio-circle"></span>
            <span class="radio-text">中位数评分率</span>
            <span class="radio-desc">使用班级评分率中位数</span>
          </label>
        </div>
      </div>
      
      <!-- 当前分类规则说明 -->
      <div class="info-card small">
        <h5 class="info-title">📊 当前分类规则</h5>
        <div class="class-type-rules">
          <div class="rule-item weak">
            <span class="rule-label">基础薄弱班:</span>
            <span class="rule-desc">{{ classTypeDescription.weakClass }}</span>
          </div>
          <div class="rule-item normal">
            <span class="rule-label">普通班:</span>
            <span class="rule-desc">{{ classTypeDescription.normalClass }}</span>
          </div>
          <div class="rule-item key">
            <span class="rule-label">重点班:</span>
            <span class="rule-desc">{{ classTypeDescription.keyClass }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 操作按钮 -->
    <div class="actions">
      <button class="btn btn-secondary" @click="resetConfig">
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="23 4 23 10 17 10"></polyline>
          <polyline points="1 20 1 14 7 14"></polyline>
          <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
        </svg>
        重置配置
      </button>
      <button class="btn btn-primary" @click="saveConfig" :disabled="isSaving">
        <svg v-if="isSaving" class="loading-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <path d="M12 6v6l4 2"></path>
        </svg>
        {{ isSaving ? '保存中...' : '应用配置' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue';
import { decisionTreeService, gradeService } from '@/services/gradeService';
import type { DecisionTreeParams, ClassTypeConfig } from '@/services/gradeService';

const emit = defineEmits<{
  (e: 'configUpdated', params: DecisionTreeParams): void;
}>();

const config = reactive<DecisionTreeParams>({
  maxDepth: 5,
  minSamplesSplit: 2,
  threshold: 0.0001,
  algorithm: 'C4.5',
  // 新增参数
  confidenceThreshold: 0.7,
  minInfoGain: 0.01,
  splitDirection: 'max_gain',
  stopCriteria: 'all',
  missingValueStrategy: 'mean_mode',
  minConfidence: 0.6
});

const classTypeConfig = reactive<ClassTypeConfig>({
  thresholdLow: 60,
  thresholdHigh: 80,
  method: 'average',
  description: {
    weakClass: '',
    normalClass: '',
    keyClass: ''
  }
});

const scoreRateConfig = reactive({
  use_score_rate: false,
  language_total: 150,
  science_total: 100
});

const isSaving = ref(false);
const showToast = ref(false);
const toastType = ref<'success' | 'error'>('success');
const toastMessage = ref('');

const defaultConfig = {
  maxDepth: 5,
  minSamplesSplit: 2,
  threshold: 0.0001,
  algorithm: 'C4.5' as const,
  // 新增参数
  confidenceThreshold: 0.7,
  minInfoGain: 0.01,
  splitDirection: 'max_gain' as const,
  stopCriteria: 'all' as const,
  missingValueStrategy: 'mean_mode' as const,
  minConfidence: 0.6
};

const defaultClassTypeConfig = {
  thresholdLow: 60,
  thresholdHigh: 80,
  method: 'average' as const
};

const defaultScoreRateConfig = {
  use_score_rate: false,
  language_total: 150,
  science_total: 100
};

const validationErrors = reactive({
  maxDepth: '',
  minSamplesSplit: '',
  threshold: '',
  confidenceThreshold: '',
  minInfoGain: '',
  minConfidence: ''
});

const classTypeErrors = reactive({
  thresholdLow: '',
  thresholdHigh: ''
});

const classTypeDescription = computed(() => ({
  weakClass: `评分率低于${classTypeConfig.thresholdLow}%为基础薄弱班`,
  normalClass: `评分率在${classTypeConfig.thresholdLow}%-${classTypeConfig.thresholdHigh}%为普通班`,
  keyClass: `评分率高于${classTypeConfig.thresholdHigh}%为重点班`
}));

const showNotification = (type: 'success' | 'error', message: string) => {
  toastType.value = type;
  toastMessage.value = message;
  showToast.value = true;
  setTimeout(() => {
    showToast.value = false;
  }, 3000);
};

const validateParams = (): boolean => {
  let isValid = true;
  
  // 验证最大树深度
  if (config.maxDepth < 1 || config.maxDepth > 20) {
    validationErrors.maxDepth = '请输入1-20之间的整数';
    isValid = false;
  } else {
    validationErrors.maxDepth = '';
  }
  
  // 验证最小分裂样本数
  if (config.minSamplesSplit < 2 || config.minSamplesSplit > 100) {
    validationErrors.minSamplesSplit = '请输入2-100之间的整数';
    isValid = false;
  } else {
    validationErrors.minSamplesSplit = '';
  }
  
  // 验证分裂阈值
  if (config.threshold <= 0.00001 || config.threshold > 0.1) {
    validationErrors.threshold = '请输入0.00001-0.1之间的数值';
    isValid = false;
  } else {
    validationErrors.threshold = '';
  }
  
  // 验证置信度阈值
  if (config.confidenceThreshold < 0 || config.confidenceThreshold > 1) {
    validationErrors.confidenceThreshold = '请输入0-1之间的数值';
    isValid = false;
  } else {
    validationErrors.confidenceThreshold = '';
  }
  
  // 验证最小置信度
  if (config.minConfidence < 0 || config.minConfidence > 1) {
    validationErrors.minConfidence = '请输入0-1之间的数值';
    isValid = false;
  } else {
    validationErrors.minConfidence = '';
  }
  
  // 验证最小信息增益
  if (config.minInfoGain < 0 || config.minInfoGain > 1) {
    validationErrors.minInfoGain = '请输入0-1之间的数值';
    isValid = false;
  } else {
    validationErrors.minInfoGain = '';
  }
  
  // 验证班级类型配置
  if (classTypeConfig.thresholdLow < 0 || classTypeConfig.thresholdLow > 100) {
    classTypeErrors.thresholdLow = '请输入0-100之间的整数';
    isValid = false;
  } else {
    classTypeErrors.thresholdLow = '';
  }
  
  if (classTypeConfig.thresholdHigh < 0 || classTypeConfig.thresholdHigh > 100) {
    classTypeErrors.thresholdHigh = '请输入0-100之间的整数';
    isValid = false;
  } else if (classTypeConfig.thresholdLow >= classTypeConfig.thresholdHigh) {
    classTypeErrors.thresholdHigh = '基础薄弱班分数线必须小于重点班分数线';
    isValid = false;
  } else {
    classTypeErrors.thresholdHigh = '';
  }
  
  return isValid;
};

onMounted(() => {
  loadConfig();
});

const loadConfig = async () => {
  try {
    const [dtResponse, classTypeResponse, scoreRateResponse] = await Promise.all([
      decisionTreeService.getDecisionTreeConfig(),
      gradeService.getClassTypeConfig(),
      gradeService.getScoreRateConfig()
    ]);
    
    if (dtResponse.params) {
      config.maxDepth = dtResponse.params.maxDepth;
      config.minSamplesSplit = dtResponse.params.minSamplesSplit;
      config.threshold = dtResponse.params.threshold;
      config.algorithm = dtResponse.params.algorithm;
      // 加载新增参数，使用默认值作为后备
      config.confidenceThreshold = dtResponse.params.confidenceThreshold ?? 0.7;
      config.minInfoGain = dtResponse.params.minInfoGain ?? 0.01;
      config.splitDirection = dtResponse.params.splitDirection ?? 'max_gain';
      config.stopCriteria = dtResponse.params.stopCriteria ?? 'all';
      config.missingValueStrategy = dtResponse.params.missingValueStrategy ?? 'mean_mode';
      config.minConfidence = dtResponse.params.minConfidence ?? 0.6;
    }
    
    if (classTypeResponse.config) {
      classTypeConfig.thresholdLow = classTypeResponse.config.thresholdLow;
      classTypeConfig.thresholdHigh = classTypeResponse.config.thresholdHigh;
      classTypeConfig.method = classTypeResponse.config.method;
      classTypeConfig.description = classTypeResponse.config.description;
    }
    
    if (scoreRateResponse.config) {
      scoreRateConfig.use_score_rate = scoreRateResponse.config.use_score_rate;
      scoreRateConfig.language_total = scoreRateResponse.config.language_total;
      scoreRateConfig.science_total = scoreRateResponse.config.science_total;
    }
    
    showNotification('success', '配置加载成功');
  } catch (error) {
    console.error('加载配置失败:', error);
    showNotification('error', '加载配置失败，使用默认值');
  }
};

const resetConfig = () => {
  config.maxDepth = defaultConfig.maxDepth;
  config.minSamplesSplit = defaultConfig.minSamplesSplit;
  config.threshold = defaultConfig.threshold;
  config.algorithm = defaultConfig.algorithm;
  config.confidenceThreshold = defaultConfig.confidenceThreshold;
  config.minInfoGain = defaultConfig.minInfoGain;
  config.splitDirection = defaultConfig.splitDirection;
  config.stopCriteria = defaultConfig.stopCriteria;
  config.missingValueStrategy = defaultConfig.missingValueStrategy;
  config.minConfidence = defaultConfig.minConfidence;
  validationErrors.maxDepth = '';
  validationErrors.minSamplesSplit = '';
  validationErrors.threshold = '';
  validationErrors.confidenceThreshold = '';
  validationErrors.minInfoGain = '';
  validationErrors.minConfidence = '';
  
  classTypeConfig.thresholdLow = defaultClassTypeConfig.thresholdLow;
  classTypeConfig.thresholdHigh = defaultClassTypeConfig.thresholdHigh;
  classTypeConfig.method = defaultClassTypeConfig.method;
  classTypeErrors.thresholdLow = '';
  classTypeErrors.thresholdHigh = '';
  
  scoreRateConfig.use_score_rate = defaultScoreRateConfig.use_score_rate;
  scoreRateConfig.language_total = defaultScoreRateConfig.language_total;
  scoreRateConfig.science_total = defaultScoreRateConfig.science_total;
  
  showNotification('success', '已恢复默认配置');
};

const saveConfig = async () => {
  // 前端验证
  if (!validateParams()) {
    showNotification('error', '请修正红色标记的参数错误');
    return;
  }
  
  isSaving.value = true;
  try {
    // 保存决策树参数
    await decisionTreeService.updateDecisionTreeConfig({
      maxDepth: config.maxDepth,
      minSamplesSplit: config.minSamplesSplit,
      threshold: config.threshold,
      algorithm: config.algorithm,
      confidenceThreshold: config.confidenceThreshold,
      minInfoGain: config.minInfoGain,
      splitDirection: config.splitDirection,
      stopCriteria: config.stopCriteria,
      missingValueStrategy: config.missingValueStrategy,
      minConfidence: config.minConfidence
    });
    
    // 保存班级类型配置
    await gradeService.updateClassTypeConfig({
      thresholdLow: classTypeConfig.thresholdLow,
      thresholdHigh: classTypeConfig.thresholdHigh,
      method: classTypeConfig.method
    });
    
    // 保存评分率配置
    await gradeService.updateScoreRateConfig({
      use_score_rate: scoreRateConfig.use_score_rate,
      language_total: scoreRateConfig.language_total,
      science_total: scoreRateConfig.science_total
    });
    
    showNotification('success', '配置保存成功');
    emit('configUpdated', { ...config });
  } catch (error) {
    console.error('保存配置失败:', error);
    showNotification('error', '保存配置失败');
  } finally {
    isSaving.value = false;
  }
};
</script>

<style scoped>
.config-panel {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  position: relative;
}

.toast {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 12px 20px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
  z-index: 1000;
  animation: slideIn 0.3s ease;
}

.toast.success {
  background: #f6ffed;
  border: 1px solid #b7eb8f;
  color: #52c41a;
}

.toast.error {
  background: #fff2f0;
  border: 1px solid #ffccc7;
  color: #ff4d4f;
}

.toast-icon {
  flex-shrink: 0;
}

.toast-message {
  font-size: 14px;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.header-info {
  flex: 1;
}

.panel-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0 0 4px 0;
}

.panel-subtitle {
  font-size: 12px;
  color: #999;
  margin: 0;
}

.reset-btn {
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  padding: 8px;
  border-radius: 6px;
  transition: all 0.2s;
}

.reset-btn:hover {
  background: #f5f5f5;
  color: #666;
}

.section {
  margin-bottom: 20px;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 15px;
}

.section-title {
  font-size: 14px;
  font-weight: 500;
  color: #666;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-icon {
  font-size: 16px;
}

.section-hint {
  font-size: 12px;
  color: #bbb;
}

.param-item {
  margin-bottom: 20px;
  padding: 15px;
  background: #fafafa;
  border-radius: 8px;
  transition: all 0.2s;
}

.param-item.has-error {
  background: #fff2f0;
  border: 1px solid #ffccc7;
}

.param-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.param-label {
  font-size: 13px;
  color: #444;
  font-weight: 500;
  flex: 1;
}

.param-value-wrapper {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.param-value {
  font-size: 14px;
  color: #1890ff;
  font-weight: 600;
  min-width: 60px;
  text-align: right;
}

.param-unit {
  font-size: 12px;
  color: #999;
}

.tooltip-wrapper {
  position: relative;
  cursor: help;
}

.tooltip-icon {
  color: #999;
}

.tooltip-text {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  background: #333;
  color: #fff;
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 12px;
  white-space: nowrap;
  opacity: 0;
  visibility: hidden;
  transition: all 0.2s;
  z-index: 100;
  margin-bottom: 8px;
  max-width: 300px;
}

.tooltip-wrapper:hover .tooltip-text {
  opacity: 1;
  visibility: visible;
}

.tooltip-text::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border: 6px solid transparent;
  border-top-color: #333;
}

.param-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

.number-input-small {
  width: 80px;
  padding: 6px 10px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  font-size: 13px;
  text-align: center;
  outline: none;
  transition: border-color 0.2s;
}

.number-input-small:focus {
  border-color: #1890ff;
}

.number-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #d9d9d9;
  border-radius: 6px;
  font-size: 13px;
  outline: none;
  transition: border-color 0.2s;
}

.number-input:focus {
  border-color: #1890ff;
}

.slider {
  flex: 1;
  height: 6px;
  -webkit-appearance: none;
  appearance: none;
  background: #e8f4fd;
  border-radius: 3px;
  outline: none;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 18px;
  height: 18px;
  background: #1890ff;
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid #fff;
  box-shadow: 0 2px 6px rgba(24, 144, 255, 0.4);
}

.slider::-moz-range-thumb {
  width: 18px;
  height: 18px;
  background: #1890ff;
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid #fff;
  box-shadow: 0 2px 6px rgba(24, 144, 255, 0.4);
}

.range-labels {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

.error-message {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #ff4d4f;
  margin-top: 8px;
}

.radio-group {
  display: flex;
  gap: 15px;
}

.radio-label {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 10px 15px;
  background: #fff;
  border: 1px solid #d9d9d9;
  border-radius: 6px;
  transition: all 0.2s;
}

.radio-label:hover {
  border-color: #1890ff;
}

.radio-label.active {
  background: #e8f4fd;
  border-color: #1890ff;
}

.radio-label input[type="radio"] {
  display: none;
}

.radio-circle {
  width: 16px;
  height: 16px;
  border: 2px solid #d9d9d9;
  border-radius: 50%;
  position: relative;
  transition: all 0.2s;
}

.radio-label.active .radio-circle {
  border-color: #1890ff;
}

.radio-label.active .radio-circle::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 8px;
  height: 8px;
  background: #1890ff;
  border-radius: 50%;
}

.radio-text {
  font-size: 14px;
  font-weight: 500;
  color: #444;
}

.radio-label.active .radio-text {
  color: #1890ff;
}

.radio-desc {
  font-size: 12px;
  color: #999;
  margin-left: auto;
}

.info-card {
  background: #fffbe6;
  border: 1px solid #ffe58f;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 20px;
}

.info-title {
  font-size: 13px;
  font-weight: 500;
  color: #faad14;
  margin: 0 0 10px 0;
}

.info-list {
  margin: 0;
  padding-left: 20px;
}

.info-list li {
  font-size: 12px;
  color: #8c8c8c;
  margin-bottom: 6px;
}

.info-list li:last-child {
  margin-bottom: 0;
}

.info-list strong {
  color: #595959;
}

.actions {
  display: flex;
  gap: 12px;
  margin-top: 10px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.btn {
  flex: 1;
  padding: 12px 20px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border: none;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: #1890ff;
  color: #fff;
}

.btn-primary:hover:not(:disabled) {
  background: #40a9ff;
}

.btn-secondary {
  background: #f5f5f5;
  color: #666;
  border: 1px solid #d9d9d9;
}

.btn-secondary:hover {
  background: #eee;
}

.loading-icon {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>