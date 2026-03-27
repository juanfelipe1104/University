import mongoose from "mongoose";

const movieSchema = new mongoose.Schema(
    {
        name: {
            type: String,
            required: true,
            unique: true,
            trim: true
        },
        genre: {
            type: String,
            enum:{
                values: ["Drama", "Comedy"],
                message: "Debe ser drama o comedy"
            }
        },
        timesRented:{
            type: Number,
            default: 0
        },
        isAvailable:{
            type: Boolean,
            default: true
        }
    }
)

const Movie = mongoose.model('Movie', movieSchema);

export default Movie;