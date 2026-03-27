import * as authorController from "../controllers/authors.controller.js";
import { Router } from "express";

const router = Router();

router.get('/', authorController.getAuthors);
router.post('/', authorController.createAuthor);
router.get('/:id/books', authorController.getBooksFromAuthor);
export default router;