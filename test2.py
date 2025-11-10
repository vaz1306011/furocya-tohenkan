# 引入库
import graphviz

# 创建有向图，不同渲染引擎修改参数engine, e.g. engine='fdp'
dot = graphviz.Digraph(comment="The Round Table")
# 配置全局属性，以 graph 属性为例
# 可以使用弯曲的连接线
dot.graph_attr["splines"] = "true"
# 禁止节点重叠
dot.graph_attr["overlap"] = "false"
# 添加节点
dot.node("A", "King Arthur")
dot.node("B", "Sir Bedevere the Wise")
dot.node("L", "Sir Lancelot the Brave")
# 添加 边
dot.edges(["AB", "AL"])
dot.edge("B", "L", constraint="false")
# 渲染
dot.render()
