import Author from "../models/author.model.js";
import Book from "../models/book.model.js";

export const getAuthors = async (req, res) => {
    const authors = await Author.find()
    res.json(authors);
}

export const createAuthor = async (req, res) => {
    const author = req.body;
    await Author.create(author);
    res.status(201).json({
        author: author
    });
}

export const getBooksFromAuthor = async (req, res) => {
    const { id } = req.params;
    const books = await Book.find({author: id})
    res.json(books);
}