import { ZodError } from 'zod';
import { AppError } from './errorHandler.js';

export const validate = (schema) => async (req, res, next) => {
    try {
        await schema.parseAsync({
            body: req.body,
            query: req.query,
            params: req.params
        });
        next();
    } catch (error) {
        if (error instanceof ZodError) {
            const errors = error.issues.map(err => ({
                campo: err.path.join('.'),
                mensaje: err.message
            }));

            return AppError.badRequest('Error de validación', errors);
        }
        next(error);
    }
};