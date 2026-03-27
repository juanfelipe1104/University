import Book from "../models/book.model.js";

const stringToBool = (string) => {
    if (string === "true")
        return true
    else
        return false
}

export const getBooks = async (req, res) => {
    const { genre, available } = req.query;
    const boolAvailable = stringToBool(available)
    const books = await Book.find({ genre: genre, available: boolAvailable }).populate("author");
    res.json(books);
}

export const createBook = async(req, res) => {
    const book = req.body;
    await Book.create(book);
    res.status(201).json({
        message: "Libro creado",
        book: book
    });
}