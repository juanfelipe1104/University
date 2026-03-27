import mongoose from 'mongoose';

const authorSchema = new mongoose.Schema(
    {
        name: {
            type: String,
            required: [true, 'El nombre es requerido'],
            trim: true,
            minlength: [2, 'Mínimo 2 caracteres'],
            maxlength: [100, 'Máximo 100 caracteres']
        },
        nationality: {
            type: String,
            required: [true, 'La nacionalidad es requerida'],
            trim: true,
            minlength: [2, 'Mínimo 2 caracteres'],
            maxlength: [100, 'Máximo 100 caracteres']
        },
        birthDate: {
            type: Date,
            required: [true, 'La fecha de nacimiento es requerida'],
        },
        bio: {
            type: String
        }
    }
)

const Author = mongoose.model('Author', authorSchema);

export default Author;