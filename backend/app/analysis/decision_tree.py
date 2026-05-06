# Decision tree analysis module

class Node:
    '''''Represents a decision tree node. 
    
    '''  
    def __init__(self, parent = None, dataset = None):  
        self.dataset = dataset # 落在该结点的训练实例集  
        self.result = None # 结果类标签  
        self.attr = None # 该结点的分裂属性ID  
        self.childs = {} # 该结点的子树列表，key-value pair: (属性attr的值, 对应的子树)  
        self.parent = parent # 该结点的父亲结点  
        self.info_gain = None # 信息增益  
        self.gain_ratio = None # 信息增益比
        self.split_criteria = None # 分裂依据  
        self.node_id = None # 节点ID  
        self.depth = 0 # 节点深度  
        self.sample_count = 0 # 样本数量
        self.class_distribution = {} # 类别分布
        self.entropy_before = None # 分裂前熵值
        self.entropy_after = None # 分裂后熵值
        

def entropy(props):  
    if (not isinstance(props, (tuple, list))):  
        return None  
    
    from math import log  
    log2 = lambda x:log(x)/log(2) # 计算经验熵
    e = 0.0  
    for p in props:  
        e -= p * log2(p)  
    return e  


def info_gain(D, A, T = -1, return_ratio = False):  
    '''''特征A对训练数据集D的信息增益 g(D,A) 
    
    g(D,A)=entropy(D) - entropy(D|A) 
            假设数据集D的每个元组的最后一个特征为类标签 
    T为目标属性的ID，-1表示元组的最后一个元素为目标
    
    Returns:
        dict: 包含信息增益、熵值等详细信息
    '''  
    if (not isinstance(D, (set, list))):  
        return None  
    if (not type(A) is int):  
        return None  
    C = {} # 结果计数字典  
    DA = {} # 属性A的取值计数字典  
    CDA = {} # 结果和属性A的不同组合的取值计数字典  
    for t in D:  
        C[t[T]] = C.get(t[T], 0) + 1  #统计目标属性各种取值下的个数，用户经验熵的计算
        DA[t[A]] = DA.get(t[A], 0) + 1  #统计属性列下各种取值的个数，用于计算经验条件熵
        CDA[(t[T], t[A])] = CDA.get((t[T], t[A]), 0) + 1  #统计（属性列，目标列）下各种组合取值的个数，例如（女，合格）（男、合格）（）
    
    PC = map(lambda x : x / len(D), C.values()) # 类别的概率列表
    entropy_D = entropy(tuple(PC)) # map返回的对象类型为map，需要强制类型转换为元组  


    PCDA = {} # 特征A的每个取值给定的条件下各个类别的概率（条件概率）  
    for key, value in CDA.items():  
        a = key[1] # 特征A的取值
        pca = value / DA[a]  
        PCDA.setdefault(a, []).append(pca)  
    
    condition_entropy = 0.0  
    for a, v in DA.items():  
        p = v / len(D)  
        e = entropy(PCDA[a])  
        condition_entropy += e * p  #计算经验条件熵
    
    info_gain_value = entropy_D - condition_entropy
    
    if (return_ratio):  
        gain_ratio_value = info_gain_value / entropy_D if entropy_D > 0 else 0
        return {
            'gain': gain_ratio_value,
            'info_gain': info_gain_value,
            'entropy_before': entropy_D,
            'entropy_after': condition_entropy,
            'gain_type': 'gain_ratio'
        }
    else:  
        return {
            'gain': info_gain_value,
            'info_gain': info_gain_value,
            'entropy_before': entropy_D,
            'entropy_after': condition_entropy,
            'gain_type': 'info_gain'
        }
    
def get_result(D, T = -1):  
    '''''获取数据集D中实例数最大的目标特征T的值'''  
    if (not isinstance(D, (set, list))):  
        return None  
    if (not type(T) is int):  
        return None  
    count = {}  
    for t in D:  
        count[t[T]] = count.get(t[T], 0) + 1  
    max_count = 0  
    for key, value in count.items():  
        if (value > max_count):  
            max_count = value  
            result = key  
    return result   


def devide_set(D, A):  
    '''''根据特征A的值把数据集D分裂为多个子集'''  
    #判断D的数据类型是set和list类型
    if (not isinstance(D, (set, list))):  
        return None
    #判断A的数据类型是否是int型
    if (not type(A) is int):  
        return None  
    subset = {}
    '''''根据特征A的结果划分数据集'''  
    for t in D:  
        subset.setdefault(t[A], []).append(t)  
    return subset


def build_tree(D, A, threshold = 0.0001, T = -1, Tree = None, algo = "C4.5", analysis_id=None, node_id=0, depth=0, max_depth=10, min_samples_split=2, params=None, attr_names=None, calculation_steps=None, feature_ranking=None):
    '''''根据数据集D和特征集A构建决策树. 
    
    T为目标属性在元组中的索引 . 目前支持ID3和C4.5两种算法
    analysis_id: 分析ID，用于存储中间结果
    node_id: 节点ID
    depth: 节点深度
    max_depth: 最大树深度
    min_samples_split: 最小分裂样本数
    params: 决策树参数配置
    attr_names: 属性名称列表
    calculation_steps: 计算步骤列表（用于记录）
    feature_ranking: 特征增益排序列表（用于记录）''' 
    # 判断最大深度限制
    if depth >= max_depth:
        Tree = Node(None, D) if Tree is None else Tree
        Tree.node_id = node_id
        Tree.depth = depth
        Tree.result = get_result(D)
        Tree.sample_count = len(D)
        
        # 计算类别分布
        class_dist = {}
        for t in D:
            class_dist[t[T]] = class_dist.get(t[T], 0) + 1
        Tree.class_distribution = class_dist
        
        if analysis_id:
            from app.analysis.intermediate_results import storage
            storage.save_result(
                analysis_id,
                'decision_tree_node',
                {
                    'node_id': Tree.node_id,
                    'depth': Tree.depth,
                    'result': Tree.result,
                    'is_leaf': True,
                    'sample_count': Tree.sample_count,
                    'class_distribution': Tree.class_distribution,
                    'reason': '达到最大深度'
                },
                f'叶子节点，达到最大深度: {Tree.result}'
            )
        return Tree
    
    # 判断最小样本数限制
    if len(D) < min_samples_split:
        Tree = Node(None, D) if Tree is None else Tree
        Tree.node_id = node_id
        Tree.depth = depth
        Tree.result = get_result(D)
        Tree.sample_count = len(D)
        
        # 计算类别分布
        class_dist = {}
        for t in D:
            class_dist[t[T]] = class_dist.get(t[T], 0) + 1
        Tree.class_distribution = class_dist
        
        if analysis_id:
            from app.analysis.intermediate_results import storage
            storage.save_result(
                analysis_id,
                'decision_tree_node',
                {
                    'node_id': Tree.node_id,
                    'depth': Tree.depth,
                    'result': Tree.result,
                    'is_leaf': True,
                    'sample_count': Tree.sample_count,
                    'class_distribution': Tree.class_distribution,
                    'reason': '样本数小于最小分裂样本数'
                },
                f'叶子节点，样本数不足: {Tree.result}'
            )
        return Tree
    
    # 判断Tree是否存在和Tree是否是节点
    if (Tree != None and not isinstance(Tree, Node)):
        return None
    # 判断数据集D的类型是否是set集合和list集合的一种，如果不是直接返回
    if (not isinstance(D, (set, list))):
        return None
    # 判断特征集A的类型是否是一个set集合
    if (not type(A) is set):
        return None
    
    if (None == Tree):
        Tree = Node(None, D)
        Tree.node_id = node_id
        Tree.depth = depth
    else:
        Tree.node_id = node_id
        Tree.depth = depth
    
    # 设置样本数量
    Tree.sample_count = len(D)
    
    # 计算类别分布
    class_dist = {}
    for t in D:
        class_dist[t[T]] = class_dist.get(t[T], 0) + 1
    Tree.class_distribution = class_dist
    
    subset = devide_set(D, T)   # 根据特征T的取值拆分数据集
    if (len(subset) <= 1):  # 如果该特征T的取值为一个时，则这个唯一取值为这个节点的结果
        for key in subset.keys():
            Tree.result = key
        del(subset)
        # 记录叶子节点信息
        if analysis_id:
            from app.analysis.intermediate_results import storage
            from app.analysis.analysis_logger import logger
            
            # 记录节点分裂日志
            logger.log_node_split(
                analysis_id=analysis_id,
                node_id=Tree.node_id,
                depth=Tree.depth,
                attribute=None,
                entropy_before=None,
                entropy_after=None,
                info_gain=None,
                gain_ratio=None,
                sample_count=Tree.sample_count,
                class_distribution=Tree.class_distribution
            )
            
            storage.save_result(
                analysis_id,
                'decision_tree_node',
                {
                    'node_id': Tree.node_id,
                    'depth': Tree.depth,
                    'result': Tree.result,
                    'is_leaf': True,
                    'sample_count': Tree.sample_count,
                    'class_distribution': Tree.class_distribution
                },
                f'叶子节点，类别: {Tree.result}'
            )
        return Tree
    if (len(A) <= 0):  # 当特征个数小于等于0的时候，返回
        Tree.result = get_result(D)
        # 记录叶子节点信息
        if analysis_id:
            from app.analysis.intermediate_results import storage
            from app.analysis.analysis_logger import logger
            
            logger.log_node_split(
                analysis_id=analysis_id,
                node_id=Tree.node_id,
                depth=Tree.depth,
                attribute=None,
                entropy_before=None,
                entropy_after=None,
                info_gain=None,
                gain_ratio=None,
                sample_count=Tree.sample_count,
                class_distribution=Tree.class_distribution
            )
            
            storage.save_result(
                analysis_id,
                'decision_tree_node',
                {
                    'node_id': Tree.node_id,
                    'depth': Tree.depth,
                    'result': Tree.result,
                    'is_leaf': True,
                    'sample_count': Tree.sample_count,
                    'class_distribution': Tree.class_distribution
                },
                f'叶子节点，多数类别: {Tree.result}'
            )
        return Tree
    
    use_gain_ratio = False if algo == "ID3" else True  # 是要实现ID3还是C4.5算法
    max_gain = 0.0
    attr_id = None
    gain_values = []
    
    # 计算所有特征的信息增益
    for a in A:
        gain_result = info_gain(D, a, return_ratio = use_gain_ratio)
        if gain_result is None:
            continue
        
        gain = gain_result['gain']
        info_gain_val = gain_result['info_gain']
        entropy_before = gain_result['entropy_before']
        entropy_after = gain_result['entropy_after']
        
        attr_name = attr_names[a] if attr_names and a < len(attr_names) else f'属性{a}'
        
        gain_values.append({
            "attribute": a,
            "attribute_name": attr_name,
            "gain": gain,
            "info_gain": info_gain_val,
            "entropy_before": entropy_before,
            "entropy_after": entropy_after,
            "gain_type": gain_result['gain_type']
        })
        
        if (gain > max_gain):
            max_gain = gain
            attr_id = a  # 获取信息增益最大的特征
    
    # 记录特征增益排序
    if feature_ranking is not None and attr_id is not None:
        for gv in gain_values:
            feature_ranking.append({
                "attribute": gv['attribute'],
                "attribute_name": gv['attribute_name'],
                "gain": gv['gain'],
                "info_gain": gv['info_gain']
            })
        # 按增益排序
        feature_ranking.sort(key=lambda x: x['gain'], reverse=True)
    
    # 记录信息增益计算过程
    if analysis_id:
        from app.analysis.intermediate_results import storage
        from app.analysis.analysis_logger import logger
        
        # 记录计算步骤
        if calculation_steps is not None and attr_id is not None:
            selected_attr_name = attr_names[attr_id] if attr_names and attr_id < len(attr_names) else f'属性{attr_id}'
            selected_gain = next((gv for gv in gain_values if gv['attribute'] == attr_id), None)
            
            calculation_steps.append({
                "step": "feature_selection",
                "node_id": Tree.node_id,
                "feature_id": attr_id,
                "feature_name": selected_attr_name,
                "entropy_before": selected_gain['entropy_before'] if selected_gain else None,
                "entropy_after": selected_gain['entropy_after'] if selected_gain else None,
                "info_gain": selected_gain['info_gain'] if selected_gain else None,
                "gain_ratio": selected_gain['gain'] if selected_gain and use_gain_ratio else None,
                "sample_count": Tree.sample_count,
                "class_distribution": Tree.class_distribution
            })
        
        storage.save_result(
            analysis_id,
            'decision_tree_gain_calculation',
            {
                'node_id': Tree.node_id,
                'gain_values': gain_values,
                'selected_attribute': attr_id,
                'max_gain': max_gain,
                'algorithm': algo,
                'sample_count': Tree.sample_count,
                'class_distribution': Tree.class_distribution
            },
            f'节点 {Tree.node_id} 的信息增益计算'
        )
    
    if (max_gain < threshold):  # 判断信息增益比是否小于阈值
        Tree.result = get_result(D)
        # 记录叶子节点信息
        if analysis_id:
            from app.analysis.intermediate_results import storage
            from app.analysis.analysis_logger import logger
            
            logger.log_node_split(
                analysis_id=analysis_id,
                node_id=Tree.node_id,
                depth=Tree.depth,
                attribute=None,
                entropy_before=None,
                entropy_after=None,
                info_gain=None,
                gain_ratio=None,
                sample_count=Tree.sample_count,
                class_distribution=Tree.class_distribution
            )
            
            storage.save_result(
                analysis_id,
                'decision_tree_node',
                {
                    'node_id': Tree.node_id,
                    'depth': Tree.depth,
                    'result': Tree.result,
                    'is_leaf': True,
                    'max_gain': max_gain,
                    'threshold': threshold,
                    'sample_count': Tree.sample_count,
                    'class_distribution': Tree.class_distribution
                },
                f'叶子节点，信息增益小于阈值: {Tree.result}'
            )
        return Tree
    
    # 获取选中属性的增益详情
    selected_gain = next((gv for gv in gain_values if gv['attribute'] == attr_id), None)
    
    Tree.attr = attr_id
    Tree.info_gain = max_gain
    Tree.gain_ratio = selected_gain['gain'] if selected_gain else None
    Tree.entropy_before = selected_gain['entropy_before'] if selected_gain else None
    Tree.entropy_after = selected_gain['entropy_after'] if selected_gain else None
    Tree.split_criteria = f'信息增益: {max_gain:.4f}'
    
    # 记录非叶子节点信息
    if analysis_id:
        from app.analysis.intermediate_results import storage
        from app.analysis.analysis_logger import logger
        
        logger.log_node_split(
            analysis_id=analysis_id,
            node_id=Tree.node_id,
            depth=Tree.depth,
            attribute=attr_id,
            entropy_before=Tree.entropy_before,
            entropy_after=Tree.entropy_after,
            info_gain=Tree.info_gain,
            gain_ratio=Tree.gain_ratio,
            sample_count=Tree.sample_count,
            class_distribution=Tree.class_distribution
        )
        
        storage.save_result(
            analysis_id,
            'decision_tree_node',
            {
                'node_id': Tree.node_id,
                'depth': Tree.depth,
                'attribute': attr_id,
                'attribute_name': attr_names[attr_id] if attr_names and attr_id < len(attr_names) else None,
                'info_gain': max_gain,
                'gain_ratio': Tree.gain_ratio,
                'entropy_before': Tree.entropy_before,
                'entropy_after': Tree.entropy_after,
                'is_leaf': False,
                'sample_count': Tree.sample_count,
                'class_distribution': Tree.class_distribution
            },
            f'非叶子节点，分裂属性: {attr_id}, 信息增益: {max_gain:.4f}'
        )
    
    subD = devide_set(D, attr_id)
    del(D[:])  # 删除中间数据,释放内存
    Tree.dataset = None
    A.discard(attr_id)  # 从特征集中排查已经使用过的特征
    
    # 递归构建子树
    child_node_id = node_id + 1
    for key in subD.keys():
        tree = Node(Tree, subD.get(key))
        Tree.childs[key] = tree
        child_node = build_tree(
            subD.get(key), 
            A.copy(), 
            threshold, 
            T, 
            tree, 
            algo, 
            analysis_id, 
            child_node_id, 
            depth + 1,
            max_depth,
            min_samples_split,
            params,
            attr_names,
            calculation_steps,
            feature_ranking
        )
        child_node_id += len(child_node.childs) + 1
    
    # 记录决策树构建完成
    if analysis_id and depth == 0:
        from app.analysis.intermediate_results import storage
        from app.analysis.analysis_logger import logger
        
        # 记录完整的计算日志
        logger.log_decision_tree_calculation(
            analysis_id=analysis_id,
            params=params,
            calculation_steps=calculation_steps or [],
            feature_ranking=feature_ranking or [],
            result='success',
            user_id='system'
        )
        
        storage.save_result(
            analysis_id,
            'decision_tree_build',
            {
                'tree_structure': get_tree_structure(Tree),
                'algorithm': algo,
                'threshold': threshold,
                'max_depth': max_depth,
                'min_samples_split': min_samples_split,
                'params': params,
                'calculation_steps': calculation_steps,
                'feature_ranking': feature_ranking
            },
            '决策树构建完成'
        )
    
    return Tree


def build_tree_with_params(data, attr_names=None, params=None):
    """使用配置参数构建决策树
    
    Args:
        data: 数据集
        attr_names: 属性名称列表
        params: 决策树参数配置（可选）
        
    Returns:
        tuple: (tree, calculation_steps, feature_ranking)
    """
    # 默认参数
    default_params = {
        'min_samples_split': 2,
        'max_depth': 5,
        'threshold': 0.0001,
        'algorithm': 'C4.5'
    }
    
    # 合并用户参数和默认参数
    effective_params = {**default_params, **(params or {})}
    
    # 提取特征集
    if len(data) > 0 and isinstance(data[0], (list, tuple)):
        num_features = len(data[0]) - 1  # 最后一列是标签
        features = set(range(num_features))
    else:
        features = set()
    
    # 初始化计算步骤和特征排序
    calculation_steps = []
    feature_ranking = []
    
    # 构建决策树
    tree = build_tree(
        D=data,
        A=features,
        threshold=effective_params['threshold'],
        T=-1,
        algo=effective_params['algorithm'],
        max_depth=effective_params['max_depth'],
        min_samples_split=effective_params['min_samples_split'],
        params=effective_params,
        attr_names=attr_names,
        calculation_steps=calculation_steps,
        feature_ranking=feature_ranking
    )
    
    return tree, calculation_steps, feature_ranking

def get_tree_structure(tree):
    """获取决策树结构，用于可视化"""
    if tree.result is not None:
        return {
            'node_id': tree.node_id,
            'depth': tree.depth,
            'result': tree.result,
            'is_leaf': True,
            'sample_count': tree.sample_count,
            'class_distribution': tree.class_distribution
        }
    else:
        childs = {}
        for key, child in tree.childs.items():
            childs[key] = get_tree_structure(child)
        return {
            'node_id': tree.node_id,
            'depth': tree.depth,
            'attribute': tree.attr,
            'info_gain': tree.info_gain,
            'gain_ratio': tree.gain_ratio,
            'entropy_before': tree.entropy_before,
            'entropy_after': tree.entropy_after,
            'is_leaf': False,
            'sample_count': tree.sample_count,
            'class_distribution': tree.class_distribution,
            'childs': childs
        }  


def print_brance(brance, target, attr_names):  #输出结果
    odd = 0    
    for i, e in enumerate(brance):          
        if odd == 0:
            print(attr_names[e], end = '=')  
        else:
            print(e, end = ' ∧ ')
        odd = 1 - odd  
    print(f"目标 = {target}")  


def print_tree(Tree, stack = [], attr_names = None):   
    if (None == Tree):  
        return  
    if (None != Tree.result):  
        print_brance(stack, Tree.result, attr_names)  
        return
    stack.append(Tree.attr)  
    for key, value in Tree.childs.items():  
        stack.append(key)
        print_tree(value, stack, attr_names)  
        stack.pop()  
    stack.pop()  

def visualize_tree(Tree, attr_names=None):
    """生成决策树可视化数据
    
    Args:
        Tree: 决策树
        attr_names: 属性名称列表
        
    Returns:
        可视化数据
    """
    def build_visualization(node):
        if node.result is not None:
            # 叶子节点
            return {
                'id': str(node.node_id),
                'label': f'类别: {node.result}',
                'type': 'leaf',
                'depth': node.depth,
                'result': node.result,
                'sample_count': node.sample_count,
                'class_distribution': node.class_distribution
            }
        else:
            # 非叶子节点
            children = []
            for key, child in node.childs.items():
                child_data = build_visualization(child)
                children.append({
                    'id': str(child.node_id),
                    'parent_id': str(node.node_id),
                    'edge_label': str(key),
                    'data': child_data
                })
            
            attr_name = attr_names[node.attr] if attr_names and node.attr < len(attr_names) else f'属性{node.attr}'
            
            return {
                'id': str(node.node_id),
                'label': f'{attr_name}\n信息增益: {node.info_gain:.4f}',
                'type': 'node',
                'depth': node.depth,
                'attribute': node.attr,
                'attribute_name': attr_name,
                'info_gain': node.info_gain,
                'gain_ratio': node.gain_ratio,
                'entropy_before': node.entropy_before,
                'entropy_after': node.entropy_after,
                'sample_count': node.sample_count,
                'class_distribution': node.class_distribution,
                'children': children
            }
    
    return build_visualization(Tree)

# 数据预处理
def preprocess_data(data):
    # 定义属性名称
    attr_names = ['学号', '性别', '班级', '年级', '考试类型', '学科', '分数范围']
    
    # 转换数据格式
    processed_data = []
    for row in data:
        # 转换分数为离散值
        score = row[6]
        score_range = ''
        if score >= 90:
            score_range = '优秀'
        elif score >= 80:
            score_range = '良好'
        elif score >= 70:
            score_range = '中等'
        elif score >= 60:
            score_range = '及格'
        else:
            score_range = '不及格'
        
        # 构建数据行
        processed_row = [
            row[0],        # 学号
            row[1],        # 性别
            row[2],        # 班级
            row[3],        # 年级
            row[4],        # 考试类型
            row[5],        # 学科
            score_range    # 分数范围（目标变量）
        ]
        processed_data.append(processed_row)
    
    return processed_data, attr_names