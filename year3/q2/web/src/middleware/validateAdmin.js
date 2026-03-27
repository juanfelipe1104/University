import { AppError } from "./errorHandler.js";

export const validateAdmin = (req, res, next) => {
    const user = req.user;
    if(user.role == "admin"){
        next()
    }
    return AppError.badRequest("No admin");
}