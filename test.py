from graphviz import Digraph

g = Digraph("flow")

g.node("A", "開始", shape="circle")
g.node("B", "處理", shape="box")
g.node("C", "判斷", shape="diamond")
g.node("D", "結束", shape="oval")
g.node("E", "備註", shape="note")

g.edge("A", "B")
g.edge("B", "C")
g.edge("C", "D")
g.edge("C", "E", label="是")
g.edge("E", "D")

g.render("flowchart", format="pdf", view=False)
