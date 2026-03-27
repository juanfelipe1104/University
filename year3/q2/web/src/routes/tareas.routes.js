import { Router } from "express";
import * as tareasController from "../controllers/tareas.controller.js"
import * as tareasSchemas from "../schemas/tareas.schema.js"
import { validate } from "../middleware/validateReques.js";
const tareasRouter = Router();

tareasRouter.get('/', validate(tareasSchemas.getAllToDoSchema), tareasController.getAllToDos);
tareasRouter.get('/:id', validate(tareasSchemas.getIDToDoSchema), tareasController.getToDo);
tareasRouter.post('/', validate(tareasSchemas.newToDoSchema), tareasController.addToDo);
tareasRouter.put('/:id', validate(tareasSchemas.getIDToDoSchema), validate(tareasSchemas.newToDoSchema), tareasController.replaceToDo);
tareasRouter.delete('/:id', validate(tareasSchemas.getIDToDoSchema), tareasController.deleteToDo);
tareasRouter.patch('/:id/:toggle', validate(tareasSchemas.getIDToDoSchema), validate(tareasSchemas.toggleToDoSchema), tareasController.toggleToDo);

export default tareasRouter;