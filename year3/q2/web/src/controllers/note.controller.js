import Note from "../models/note.model.js";

export const getNotes = async (req, res) => {
    const notes = await Note.find();
    res.json({
        message: "Notas",
        notes: notes
    })
}

export const getTrash = async (req, res) => {
    const trash = await Note.findDeleted();
    res.json({
        message: "Trash",
        trash: trash
    })
}

export const getNote = async (req, res) => {
    const { id } = req.params;
    const note = await Note.findOne({ _id: id });
    if (note) {
        res.status(404).json(`Nota con ${id} no encontrada`);
    }
    else {
        res.json({
            message: "Note",
            note: note
        })
    }
}

export const createNote = async (req, res) => {
    const note = req.body;
    note["user"] = req.user._id 
    await Note.create(note);
    res.status(201).json({
        message: "Note created",
        note: note
    })
}

export const updateNote = async (req, res) => {
    const { id } = req.params;
    const note = req.body;
    const noteUpdated = await Note.findByIdAndUpdate(id, note, { new: true });
    res.json(noteUpdated);
}

export const softDeleteNote = async (req, res) => {
    const { id } = req.params;
    const deletedNote = await Note.softDeleteById(id);
    res.json(deletedNote);
}

export const restoreNote = async (req, res) => {
    const {id} = req.params;
    const note = await Note.restoreById(id);
    res.json(note)
}

export const hardDeleteNote = async (req, res) => {
    const {id} = req.params;
    const noteDeleted = await Note.hardDelete(id);
    res.json(noteDeleted);
}

export const emptyTrash = async (req, res) => {
    const deleted = await Note.findDeleted();
    for (const note of deleted){
        await Note.hardDelete(note._id);
    }
    res.json("Empty trash");
}