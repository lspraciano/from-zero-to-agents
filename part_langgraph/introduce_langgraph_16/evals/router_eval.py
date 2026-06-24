from pathlib import Path

from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langfuse.langchain import CallbackHandler

from part_langgraph.introduce_langgraph_16.evals.eval_cases import EvalCase, eval_cases
from part_langgraph.introduce_langgraph_16.graphs.graph_1 import graph_compiled
from part_langgraph.introduce_langgraph_16.observability.langfuse_handler import (
    get_langfuse_handler,
)
from part_langgraph.introduce_langgraph_16.pipelines.ingestion_pipeline import (
    run_ingestion_pipeline,
)

current_file_path: Path = Path(__file__)
module_directory: Path = current_file_path.parent.parent
documents_directory: Path = module_directory / "documents"
knowledge_base_file_str: str = str(documents_directory / "knowledge_base.txt")

run_ingestion_pipeline(file_path=knowledge_base_file_str)

langfuse_handler: CallbackHandler = get_langfuse_handler()


def run_router_eval() -> None:
    total: int = len(eval_cases)
    passed: int = 0

    print("=" * 60)
    print("ROUTER EVAL")
    print("=" * 60)

    case: EvalCase
    for i, case in enumerate(eval_cases, start=1):
        result: dict = graph_compiled.invoke(
            input={"messages": [HumanMessage(content=case.user_message)]},
            config=RunnableConfig(
                configurable={"thread_id": f"eval-{i}"},
                callbacks=[langfuse_handler],
            ),
        )

        actual: str = result["router_destination"]
        ok: bool = actual == case.expected_destination
        passed += int(ok)
        status: str = "PASS" if ok else "FAIL"

        print(f"[{status}] {case.user_message!r}")

        if not ok:
            print(f"       esperado : {case.expected_destination}")
            print(f"       obtido   : {actual}")

    print("-" * 60)
    print(f"Resultado: {passed}/{total} casos corretos ({100 * passed // total}%)")
    print("=" * 60)


if __name__ == "__main__":
    run_router_eval()
