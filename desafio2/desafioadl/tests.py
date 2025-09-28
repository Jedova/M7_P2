from django.test import TestCase
from io import StringIO
from contextlib import redirect_stdout
from . import services

class ServiciosTest(TestCase):
    def test_flujo_crud_e_impresion(self):
        
        # Crear tareas
        arr = services.crear_nueva_tarea("tarea 1")
        self.assertEqual(len(arr), 1)
        arr = services.crear_nueva_tarea("tarea 2")
        self.assertEqual(len(arr), 2)

        # Ids creados (en orden)
        t1_id, t2_id = arr[0]["tarea_id"], arr[1]["tarea_id"]

        # Subtareas
        arr = services.crear_sub_tarea(t1_id, "sub tarea 1")
        arr = services.crear_sub_tarea(t1_id, "sub tarea 2")
        arr = services.crear_sub_tarea(t2_id, "sub tarea 1")

        # Estructura
        self.assertEqual(len(arr), 2)
        self.assertEqual(len(arr[0]["subtareas"]), 2)
        self.assertEqual(len(arr[1]["subtareas"]), 1)

        # Impresión con formato
        buf = StringIO()
        with redirect_stdout(buf):
            services.imprimir_en_pantalla(arr)
        out = buf.getvalue().splitlines()
        self.assertTrue(out[0].startswith(f"[{t1_id}] "))
        self.assertIn(".... [", out[1])

        # Eliminar una subtarea y una tarea
        st_id = arr[0]["subtareas"][0]["subtarea_id"]
        arr = services.elimina_sub_tarea(st_id)
        self.assertEqual(len(arr[0]["subtareas"]), 1)

        arr = services.elimina_tarea(t2_id)
        self.assertEqual(len(arr), 1)
