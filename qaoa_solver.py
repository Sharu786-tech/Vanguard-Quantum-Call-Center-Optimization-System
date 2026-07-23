class QAOASolverUnavailable(RuntimeError):
    pass


def solve_qubo_with_qaoa(qubo):
    """
    Extension point for a QAOA backend.

    In a production version, this function can be connected to Qiskit, Azure Quantum,
    or another quantum runtime. The project uses a classical fallback in the main
    pipeline so it remains runnable without specialized quantum dependencies.
    """
    raise QAOASolverUnavailable(
        "QAOA backend is not configured. Use optimization.staffing_qubo as fallback."
    )
