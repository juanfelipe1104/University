import * as bookController from "../controllers/book.controller.js"
import { Router } from "express";

const router = Router();

router.get('/', bookController.getBooks);
router.post('/', bookController.createBook);

export default router;