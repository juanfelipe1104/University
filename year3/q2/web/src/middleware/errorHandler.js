export class AppError extends Error {
    constructor(message, statusCode = 500, code = null) {
        super(message);
        this.statusCode = statusCode;
        this.code = code;
        this.isOperational = true;

        Error.captureStackTrace(this, this.constructor);
    }

    static badRequest(message = 'Solicitud inválida', code = 'BAD_REQUEST') {
        return new AppError(message, 400, code);
    }

    static unauthorized(message = 'No autorizado', code = 'UNAUTHORIZED') {
        return new AppError(message, 401, code);
    }

    static forbidden(message = 'Acceso prohibido', code = 'FORBIDDEN') {
        return new AppError(message, 403, code);
    }

    static notFound(resource = 'Recurso', code = 'NOT_FOUND') {
        return new AppError(`${resource} no encontrado`, 404, code);
    }

    static conflict(message = 'Conflicto con recurso existente', code = 'CONFLICT') {
        return new AppError(message, 409, code);
    }

    static validation(message = 'Error de validación', details = []) {
        const error = new AppError(message, 400, 'VALIDATION_ERROR');
        error.details = details;
        return error;
    }

    static tooManyRequests(message = 'Demasiadas peticiones', code = 'RATE_LIMIT') {
        return new AppError(message, 429, code);
    }

    static internal(message = 'Error interno del servidor', code = 'INTERNAL_ERROR') {
        return new AppError(message, 500, code);
    }
}

export const notFoundHandler = (req, res, next) => {
    res.status(404).json({
        error: 'Ruta no encontrada',
        path: req.originalUrl,
        method: req.method
    });
};

export const errorHandler = (err, req, res, next) => {
    console.error('Error:', err);

    if (err.isOperational) {
        return res.status(err.statusCode).json({
            error: err.message,
            ...(err.details && { detalles: err.details })
        });
    }

    const isDev = process.env.NODE_ENV === 'development';
    res.status(500).json({
        error: 'Error interno del servidor',
        ...(isDev && { stack: err.stack, message: err.message })
    });
};