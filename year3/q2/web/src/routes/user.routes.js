import { Router } from "express";
import { getAllUsers, addUser } from "../controllers/users.controller.js";

const usersRouter = Router();

usersRouter.get('/', getAllUsers);
usersRouter.post('/', addUser);

export default usersRouter;