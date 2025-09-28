from django.db import models

class Tarea(models.Model):
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return f"[{self.id}] {self.descripcion}"

class SubTarea(models.Model):
    descripcion = models.CharField(max_length=255)
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name="subtareas")

    def __str__(self):
        return f"[{self.id}] {self.descripcion}"