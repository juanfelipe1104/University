import { Router } from "express";
import * as movieController from "../controllers/movies.controller.js";

const router = Router();

router.get('/', movieController.getMovies);
router.get('/:id', movieController.getMovie);
router.post('/', movieController.createMovie);
router.patch('/:id/rent', movieController.rentMovie);
router.patch('/:id/return', movieController.returnMovie);
router.get('/stats/top', movieController.getTop5Movies);

export default router;