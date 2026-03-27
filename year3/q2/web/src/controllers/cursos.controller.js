// src/controllers/cursos.controller.js
import { cursos } from '../data/cursos.js';

export const getAllCursos = (req, res) => {
    res.json(cursos);
}

export const getCursosCategoria = (req, res) => {
    const { categoria } = req.params;
    res.json(cursos[categoria]);
}

export const getCursosNivel = (req, res) => {
    const { nivel } = req.params;
    const resultado = [];
    for (const categoria in cursos) {
        resultado.push(...cursos[categoria].filter(curso => curso.nivel === nivel))
    }
    if (resultado.length === 0) {
        res.status(404).json("No encontrado")
    }
    else {
        res.json(resultado)
    }
}

export const addCourse = (req, res) => {
    const { categoria } = req.params;
    const newCourse = req.body;
    if (cursos[categoria]) {
        cursos[categoria].push(newCourse);
        res.status(201).json({
            mensaje: 'Curso creado',
            curso: newCourse
        });
    }
    else {
        res.status(404).json(`Categoria ${categoria} no encontrada`);
    }
}

export const deleteCourse = (req, res) => {
    const {categoria, id} = req.params;
    if(cursos[categoria]){
        const index = cursos[categoria].findIndex(curso => curso.id == id)
        const deletedCourse = cursos[categoria].splice(index, 1);
        res.json({
            mensaje: "Curso eliminado",
            curso: deletedCourse[0]
        })
    }
    else{
        res.status(404).json(`Categoria ${categoria} no encontrada`);
    }
}