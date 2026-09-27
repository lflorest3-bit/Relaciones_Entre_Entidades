# HelpDesk EDU

Sistema de tickets de soporte tecnico del curso Programacion / Desarrollo de Software
(Universidad Mariano Galvez de Guatemala).

Estudiante: Luis Daniel Flores Tunche

## Estructura

```
app/
  models/     # User, Ticket, Comment, Assignment, Category, enums
  services/   # TicketService, UserService (logica de negocio)
tests/        # pruebas por semana con pytest
docs/         # guia del curso
```

## Relaciones de un ticket

| Campo          | Pregunta del negocio             |
|----------------|----------------------------------|
| `requester_id` | Quien reporto el problema        |
| `assignee_id`  | Que tecnico lo atiende           |
| `category`     | A que area pertenece el caso     |
| `status`       | En que punto del proceso esta    |
| `comments`     | Como se le ha dado seguimiento   |

## Ejecutar pruebas

```bash
uv run pytest -q
```

## Flujo Git

- `main`: version estable.
- `developer`: integracion semanal.
- `feature/*`: una rama por incremento, se integra a `developer` con Pull Request.
