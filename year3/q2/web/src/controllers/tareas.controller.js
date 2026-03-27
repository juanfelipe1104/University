import data from "../data/tareas.js";
import { AppError } from "../middleware/errorHandler.js";

export const getAllToDos = (req, res) => {
    let completed = req.query.completed;
    const priority = req.query.priority;
    let resultado = data.tareas;
    if (completed !== undefined) {
        completed = (completed === "true")
        resultado = resultado.filter(tarea => tarea.completed === completed);
    }
    if (priority !== undefined) {
        resultado = resultado.filter(tarea => tarea.priority === priority);
    }
    res.json(resultado);
}

export const getToDo = (req, res) => {
    const id = parseInt(req.params.id);
    const toDo = data.tareas.find(tarea => tarea.id === id);
    if (toDo) {
        res.json(toDo);
    }
    else {
        throw AppError.notFound(`id ${id} no encontrado`);
    }
}

export const addToDo = (req, res) => {
    const toDo = req.body;
    toDo["id"] = ++data.idCounter;
    toDo["createdAt"] = new Date().toISOString();
    data.tareas.push(toDo);
    res.status(201).json({
        mensaje: "Tarea añadida",
        toDo: toDo
    })
}

export const replaceToDo = (req, res) => {
    const id = parseInt(req.params.id);
    const newToDo = req.body;
    const index = data.tareas.findIndex(tarea => tarea.id === id);
    if (index !== -1) {
        data.tareas[index] = newToDo;
        res.json({
            mensaje: "Tarea actualizada",
            newToDo: newToDo
        })
    }
    else {
        throw AppError.notFound(`id ${id} no encontrado`);
    }
}

export const deleteToDo = (req, res) => {
    const id = parseInt(req.params.id);
    const index = data.tareas.findIndex(tarea => tarea.id === id);
    if (index !== -1) {
        const deletedToDo = data.tareas.splice(index, 1);
        res.json({
            mensaje: "Tarea eliminada",
            deletedToDo: deletedToDo
        })
    }
    else {
        throw AppError.notFound(`id ${id} no encontrado`);
    }
}

export const toggleToDo = (req, res) => {
    const id = parseInt(req.params.id);
    const toggle = (req.params.toggle === "true")
    const index = data.tareas.findIndex(tarea => tarea.id === id);
    if (index !== -1) {
        data.tareas[index].completed = toggle;
        res.json({
            mensaje: "Estado de tarea actualizado",
            updatedToDo: data.tareas[index]
        })
    }
    else {
        throw AppError.notFound(`id ${id} no encontrado`);
    }
}