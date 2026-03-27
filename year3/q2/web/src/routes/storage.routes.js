import { Router } from "express";
import { uploadFile } from "../controllers/storage.controller.js";
import { upload } from "../config/storage.js";

const storageRouter = Router();

storageRouter.post('/', upload.single('file'), uploadFile);

export default storageRouter;