PENDING = "Pending"
IN_PROGRESS = "In Progress"
WAITING_PARTS = "Waiting for Parts"
COMPLETED = "Completed"
CANCELLED = "Cancelled"

ALLOWED_TRANSITIONS = {
    PENDING: [
        IN_PROGRESS,
        CANCELLED
    ],

    IN_PROGRESS: [
        WAITING_PARTS,
        COMPLETED,
        CANCELLED
    ],

    WAITING_PARTS: [
        IN_PROGRESS,
        CANCELLED
    ],

    COMPLETED: [],

    CANCELLED: []
}


def can_change_status(current_status: str, new_status: str) -> bool:
    """
    Verifica se a transição entre o estado atual e o novo estado é permitida.

    :param current_status: O estado em que o objeto se encontra atualmente.
    :param new_status: O estado para onde se pretende alterar.
    :return: True se a transição for válida, False caso contrário.
    """
    # Procura as trocas permitidas para o estado atual
    allowed_next_statuses = ALLOWED_TRANSITIONS.get(current_status, [])

    # Verifica se o novo estado pertence á lista
    is_allowed = new_status in allowed_next_statuses

    return is_allowed

def is_final_status(status: str) -> bool:
    return status in [COMPLETED, CANCELLED]