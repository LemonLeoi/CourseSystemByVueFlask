# Analysis result explainer module

class AnalysisExplainer:
    """分析结果解释器"""
    
    def __init__(self):
        """初始化解释器"""
        pass
    
    def explain_feature_importance(self, feature_importance, analysis_type):
        """生成特征重要性排序的理论依据
        
        Args:
            feature_importance: 特征重要性字典
            analysis_type: 分析类型（如'personal', 'class', 'grade'）
            
        Returns:
            解释文本
        """
        explanations = []
        
        explanations.append("特征重要性排序基于以下理论依据：")
        explanations.append("")
        
        if analysis_type == 'personal':
            explanations.append("1. 方差分析（ANOVA）：通过比较不同特征对成绩变异的贡献，识别对个人成绩影响最大的因素。")
            explanations.append("2. 相关性分析：计算各特征与成绩的相关系数，衡量线性关系强度。")
            explanations.append("3. 决策树重要性：基于决策树算法中特征的分裂次数和信息增益，评估特征的预测能力。")
        elif analysis_type == 'class':
            explanations.append("1. 组间差异分析：比较不同班级在各特征上的表现差异，识别对班级整体成绩影响显著的因素。")
            explanations.append("2. 回归分析：构建多元回归模型，量化各特征对班级平均成绩的影响程度。")
            explanations.append("3. 主成分分析（PCA）：降维并识别解释班级成绩变异的主要成分。")
        elif analysis_type == 'grade':
            explanations.append("1. 多层次模型：考虑年级、班级、学生三个层次的变异，评估各层次因素的重要性。")
            explanations.append("2. 时间序列分析：分析年级成绩的时间趋势，识别影响成绩变化的关键因素。")
            explanations.append("3. 聚类分析：将学生或班级按特征分组，分析不同群体的特征重要性差异。")
        
        explanations.append("")
        explanations.append("具体重要性排序：")
        for feature, importance in sorted(feature_importance.items(), key=lambda x: x[1], reverse=True):
            explanations.append(f"- {feature}: {importance:.4f}")
        
        return '\n'.join(explanations)
    
    def explain_model_parameters(self, model_name, parameters):
        """生成模型参数选择的理由说明
        
        Args:
            model_name: 模型名称
            parameters: 模型参数字典
            
        Returns:
            解释文本
        """
        explanations = []
        
        explanations.append(f"{model_name}模型参数选择理由：")
        explanations.append("")
        
        if model_name == 'decision_tree':
            explanations.append("1. 决策树参数选择依据：")
            if 'max_depth' in parameters:
                explanations.append(f"   - 最大深度（max_depth）：设置为{parameters['max_depth']}，平衡模型复杂度和过拟合风险。")
            if 'min_samples_split' in parameters:
                explanations.append(f"   - 最小分裂样本数（min_samples_split）：设置为{parameters['min_samples_split']}，确保分裂后的节点具有统计意义。")
            if 'criterion' in parameters:
                explanations.append(f"   - 分裂准则（criterion）：选择'{parameters['criterion']}'，基于信息增益或基尼系数评估分裂质量。")
            explanations.append("   - 算法选择（ID3/C4.5）：C4.5算法通过信息增益比避免了偏向于取值较多的特征。")
        elif model_name == 'linear_regression':
            explanations.append("1. 线性回归参数选择依据：")
            if 'regularization' in parameters:
                explanations.append(f"   - 正则化（regularization）：使用'{parameters['regularization']}'，防止过拟合。")
            if 'alpha' in parameters:
                explanations.append(f"   - 正则化强度（alpha）：设置为{parameters['alpha']}，平衡模型复杂度和拟合度。")
        elif model_name == 'kmeans':
            explanations.append("1. K-means聚类参数选择依据：")
            if 'n_clusters' in parameters:
                explanations.append(f"   - 聚类数量（n_clusters）：设置为{parameters['n_clusters']}，基于肘部法则和业务需求确定。")
            if 'max_iter' in parameters:
                explanations.append(f"   - 最大迭代次数（max_iter）：设置为{parameters['max_iter']}，确保算法收敛。")
        
        explanations.append("")
        explanations.append("参数调优过程：")
        explanations.append("- 通过交叉验证评估不同参数组合的性能")
        explanations.append("- 选择在验证集上表现最佳的参数组合")
        explanations.append("- 考虑计算效率和模型可解释性")
        
        return '\n'.join(explanations)
    
    def explain_statistical_methods(self, method_name, data):
        """生成统计方法的理论依据
        
        Args:
            method_name: 统计方法名称
            data: 相关数据
            
        Returns:
            解释文本
        """
        explanations = []
        
        explanations.append(f"{method_name}方法的理论依据：")
        explanations.append("")
        
        if method_name == 'average':
            explanations.append("1. 算术平均值：")
            explanations.append("   - 定义：所有数据值的总和除以数据个数")
            explanations.append("   - 理论基础：中心极限定理，当样本量足够大时，平均值近似服从正态分布")
            explanations.append("   - 适用场景：数据分布相对对称，无极端值的情况")
            explanations.append("   - 局限性：对极端值敏感")
        elif method_name == 'median':
            explanations.append("1. 中位数：")
            explanations.append("   - 定义：将数据按大小排序后位于中间位置的值")
            explanations.append("   - 理论基础：顺序统计量，不受极端值影响")
            explanations.append("   - 适用场景：数据分布不对称，存在极端值的情况")
            explanations.append("   - 优点：稳健性强，能更好地反映数据的中心趋势")
        elif method_name == 'standard_deviation':
            explanations.append("1. 标准差：")
            explanations.append("   - 定义：数据偏离平均值的平均程度的平方根")
            explanations.append("   - 理论基础：方差分析，衡量数据的离散程度")
            explanations.append("   - 适用场景：评估数据的一致性和稳定性")
            explanations.append("   - 与平均值配合使用：均值±标准差可以描述数据的分布范围")
        elif method_name == 'score_distribution':
            explanations.append("1. 成绩分布分析：")
            explanations.append("   - 定义：将成绩划分为不同等级并统计各等级的人数")
            explanations.append("   - 理论基础：教育测量学中的成绩分级标准")
            explanations.append("   - 适用场景：评估整体学习效果，识别成绩分布的偏态情况")
            explanations.append("   - 标准：优秀(90-100)、良好(80-89)、中等(70-79)、及格(60-69)、不及格(0-59)")
        
        explanations.append("")
        explanations.append("计算过程：")
        if method_name == 'average':
            if data:
                explanations.append(f"   - 数据个数：{len(data)}")
                explanations.append(f"   - 数据总和：{sum(data)}")
                explanations.append(f"   - 平均值：{sum(data)/len(data):.2f}")
        elif method_name == 'median':
            if data:
                sorted_data = sorted(data)
                n = len(sorted_data)
                if n % 2 == 0:
                    median = (sorted_data[n//2-1] + sorted_data[n//2])/2
                else:
                    median = sorted_data[n//2]
                explanations.append(f"   - 排序后数据：{sorted_data}")
                explanations.append(f"   - 中位数：{median:.2f}")
        
        return '\n'.join(explanations)
    
    def explain_analysis_steps(self, analysis_type, steps):
        """生成分析步骤的解释文档
        
        Args:
            analysis_type: 分析类型
            steps: 分析步骤列表
            
        Returns:
            解释文本
        """
        explanations = []
        
        explanations.append(f"{analysis_type}分析步骤解释：")
        explanations.append("")
        
        for i, step in enumerate(steps, 1):
            explanations.append(f"{i}. {step['name']}")
            explanations.append(f"   - 目的：{step['purpose']}")
            explanations.append(f"   - 方法：{step['method']}")
            if 'details' in step:
                explanations.append(f"   - 详细说明：{step['details']}")
            explanations.append("")
        
        explanations.append("分析流程说明：")
        explanations.append("- 数据获取：从数据库中提取相关成绩数据")
        explanations.append("- 数据预处理：清洗、转换和标准化数据")
        explanations.append("- 统计分析：计算各种统计指标")
        explanations.append("- 模型构建：根据需要构建预测或分类模型")
        explanations.append("- 结果解释：生成分析报告和可视化结果")
        explanations.append("- 结论建议：基于分析结果提出改进建议")
        
        return '\n'.join(explanations)
    
    def explain_correlation(self, correlation_matrix, variables):
        """生成相关性分析的解释
        
        Args:
            correlation_matrix: 相关系数矩阵
            variables: 变量列表
            
        Returns:
            解释文本
        """
        explanations = []
        
        explanations.append("相关性分析解释：")
        explanations.append("")
        explanations.append("1. 相关系数含义：")
        explanations.append("   - 取值范围：[-1, 1]")
        explanations.append("   - 正相关：值接近1，表示两个变量同向变化")
        explanations.append("   - 负相关：值接近-1，表示两个变量反向变化")
        explanations.append("   - 无相关：值接近0，表示两个变量无线性关系")
        explanations.append("")
        
        explanations.append("2. 相关系数矩阵：")
        # 简单展示相关系数矩阵
        explanations.append("   " + "	".join(variables))
        for i, row in enumerate(correlation_matrix):
            row_str = [f"{val:.2f}" for val in row]
            explanations.append(f"{variables[i]}" + "	" + "	".join(row_str))
        explanations.append("")
        
        explanations.append("3. 教育意义解读：")
        explanations.append("   - 学科间相关性：了解不同学科之间的关联程度，为课程安排提供依据")
        explanations.append("   - 成绩与其他因素的相关性：识别影响成绩的关键因素")
        explanations.append("   - 相关性不等于因果关系：需要进一步研究变量间的因果关系")
        
        return '\n'.join(explanations)
    
    def explain_anomaly_detection(self, anomalies, method):
        """生成异常值检测的解释
        
        Args:
            anomalies: 异常值列表
            method: 检测方法
            
        Returns:
            解释文本
        """
        explanations = []
        explanations.append("异常值检测解释：")
        explanations.append("")
        
        explanations.append(f"1. 检测方法：{method}")
        if method == 'z-score':
            explanations.append("   - 原理：基于正态分布，计算数据点与均值的距离（以标准差为单位）")
            explanations.append("   - 阈值：通常使用|z-score| > 3作为异常值判断标准")
        elif method == 'IQR':
            explanations.append("   - 原理：基于四分位数，计算上下界（Q1-1.5*IQR, Q3+1.5*IQR）")
            explanations.append("   - 阈值：超出上下界的数据点被视为异常值")
        
        explanations.append("")
        explanations.append("2. 检测结果：")
        explanations.append(f"   - 检测到{len(anomalies)}个异常值")
        if anomalies:
            explanations.append("   - 异常值：" + ", ".join(map(str, anomalies[:10])) + ("..." if len(anomalies) > 10 else ""))
        
        explanations.append("")
        explanations.append("3. 异常值处理策略：")
        explanations.append("   - 验证：确认异常值是否为数据录入错误")
        explanations.append("   - 保留：如果是真实数据，保留并单独分析")
        explanations.append("   - 替换：使用均值、中位数或插值方法替换")
        explanations.append("   - 删除：如果是明显错误且影响分析结果，考虑删除")
        
        return '\n'.join(explanations)

# 全局解释器实例
explainer = AnalysisExplainer()