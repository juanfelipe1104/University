import { verifyToken } from "./handleJWT.js";
import { AppError } from "./errorHandler.js";
import User from "../models/user.model.js";
import Note from "../models/note.model.js";

export const validateUser = async (req, res, next) => {
    try {
        const authHeader = req.headers.authorization;

        if (!authHeader || !authHeader.startsWith('Bearer ')) {
            return next(AppError.unauthorized('Authorization token required'));
        }

        const token = authHeader.split(' ')[1];
        const userData = verifyToken(token);

        if (!userData) {
            return next(AppError.unauthorized('Wrong authorization token'));
        }

        const user = await User.findById(userData._id);

        if (!user) {
            return next(AppError.unauthorized('User not found'));
        }

        req.user = user;
        req.token = token;

        return next();
    } catch (error) {
        return next(error);
    }
};

export const validateUserNote = async (req, res, next) => {
    const { id } = req.params;
    const note = await Note.findById(id);
    if ((note.user == req.user._id) || (req.user.role == "admin")) {
        next()
    }
    return AppError.badRequest("")
}