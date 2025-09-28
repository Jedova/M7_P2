
from typing import List, Dict
from django.db import transaction
from .models import Tarea, SubTarea

def _estructura() -> List[Dict]:
    data: List[Dict] = []
    for t in Tarea.objects.prefetch_related("subtareas").order_by("id"):
        data.append({
            "tarea_id": t.id,
            "descripcion": t.descripcion,
            "subtareas": [
                {"subtarea_id": st.id, "descripcion": st.descripcion}
                for st in t.subtareas.all().order_by("id")
            ],
        })
    return data

def recupera_tareas_y_sub_tareas() -> List[Dict]:
    return _estructura()

@transaction.atomic
def crear_nueva_tarea(descripcion: str) -> List[Dict]:
    Tarea.objects.create(descripcion=descripcion)
    return _estructura()

@transaction.atomic
def crear_sub_tarea(tarea_id: int, descripcion: str) -> List[Dict]:
    t = Tarea.objects.get(id=tarea_id)
    SubTarea.objects.create(tarea=t, descripcion=descripcion)
    return _estructura()

@transaction.atomic
def elimina_tarea(tarea_id: int) -> List[Dict]:
    Tarea.objects.filter(id=tarea_id).delete()
    return _estructura()

@transaction.atomic
def elimina_sub_tarea(sub_tarea_id: int) -> List[Dict]:
    SubTarea.objects.filter(id=sub_tarea_id).delete()
    return _estructura()

def imprimir_en_pantalla(arreglo: List[Dict]) -> None:
    for t in arreglo:
        print(f"[{t['tarea_id']}] {t['descripcion']}")
        for st in t["subtareas"]:
            print(f".... [{st['subtarea_id']}] {st['descripcion']}")
