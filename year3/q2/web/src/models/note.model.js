import mongoose from "mongoose";
import softDeletePlugin from "../plugins/softDelete.plugin.js";

const noteSchema = new mongoose.Schema(
    {
        user: {
            type: mongoose.Schema.Types.ObjectId,
            ref: 'User',
            required: true
        },
        title: {
            type: String,
            required: true,
            trim: true,
            unique: true
        },
        content: {
            type: String,
            required: true
        },
        color: {
            type: String,
            enum: {
                values: ["red", "blue"]
            },
            default: "red"
        },
        pinned: {
            type: Boolean,
            default: false
        }
    }
)

noteSchema.plugin(softDeletePlugin);

const Note = mongoose.model('Note', noteSchema);

export default Note