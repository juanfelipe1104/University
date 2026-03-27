import { Router } from "express";
import * as noteController from "../controllers/note.controller.js";
import { validateAdmin } from "../middleware/validateAdmin.js";
import { validateUser } from "../middleware/validateUser.js";

const router = Router();

router.get("/", validateUser, noteController.getNotes);
router.get("/trash", validateUser, noteController.getTrash);
router.get("/:id", validateUser, noteController.getNote);
router.post("/", validateUser, noteController.createNote);
router.put("/:id", noteController.updateNote);
router.delete("/:id", noteController.softDeleteNote);
router.post("/:id/restore", noteController.restoreNote);
router.delete("/:id/permanent", noteController.hardDeleteNote);
router.delete("/trash/empty", noteController.emptyTrash);

export default router;