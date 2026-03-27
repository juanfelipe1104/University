import {Router} from 'express'

import { getAllCursos, getCursosCategoria, getCursosNivel, addCourse, deleteCourse} from '../controllers/cursos.controller.js';
const cursosRouter = Router()

cursosRouter.get('/', getAllCursos)
cursosRouter.get('/nivel/:nivel', getCursosNivel)
cursosRouter.get('/:categoria', getCursosCategoria)
cursosRouter.post('/:categoria', addCourse)
cursosRouter.delete('/:categoria/:id', deleteCourse)

export default cursosRouter;