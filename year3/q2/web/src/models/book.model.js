import mongoose from "mongoose";

const bookSchema = new mongoose.Schema({
    title: {
        type: String,
        required: [true, 'El titulo es requerido'],
        trim: true,
        minlength: [2, 'Mínimo 2 caracteres'],
        maxlength: [100, 'Máximo 100 caracteres']
    },
    isbn: {
        type: Number,
        required: [true, 'El isbn es requerido'],
        unique: true,
    },
    author:{
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Author',
        required: true
    },
    genre:{
        type: String,
        enum: {
            values: ["fantasy", "adventure"]
        },
        default: "adventure"
    },
    publishedYear: {
        type: Date,
        default: Date()
    },
    pages: {
        type: Number,
        required: true
    },
    available: {
        type: Boolean,
        default: true
    }
})

const Book = mongoose.model('Book', bookSchema);

export default Book;