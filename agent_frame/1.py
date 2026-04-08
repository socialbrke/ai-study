from typing import TypedDict,List
from langgraph.graph import StateGraph,END

class agentstate(TypedDict):
    messages:list[str]
    current_task:str
    final_answer:str

def planning_node(state:agentstate) -> agentstate:
    current_task = state["current_task"]
    plan = f"为任务 '{current_task}' 生成的计划..."
    state["messages"].append(plan)
    return state

def exector_node(state:agentstate) -> agentstate:
    latest_plan = state["messages"][-1]
    result = f"执行计划{latest_plan}的结果..."
    state["messages"].append(result)
    return state

def should_continue(state:agentstate) -> str:
    """条件函数：根据状态决定下一步路由。"""
    if len(state["messages"]) < 3:
        return "continue_to_planner"
    else:
        state["final_answer"] = state["messages"][-1]
        return "end_workflow"

work_flow = StateGraph(agentstate)

work_flow.add_node("planner",planning_node)
work_flow.add_node("exector",exector_node)

work_flow.set_entry_point("planner")

work_flow.add_edge("planner","exector")

work_flow.add_conditional_edges("exector",should_continue,{"continue_to_planner":"planner","end_workflow":END})

app = work_flow.compile()

input = {"current_task":"分析最近的AI新闻","messages":[]}
for event in app.stream(input):
    print(event)