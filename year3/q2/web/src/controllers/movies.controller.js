import Movie from "../models/movie.model.js";

export const getMovies = async (req, res) => {
    let { genre } = req.query;
    const availableGenres = ["Drama", "Comedy"];
    if (!(genre in availableGenres)) {
        genre = {}
    }
    const movies = await Movie.find(genre);
    res.json(movies);
}

export const getMovie = async (req, res) => {
    const { id } = req.params;
    const movie = await Movie.findById(id);
    res.json(movie);
}

export const createMovie = async (req, res) => {
    const movie = req.body;
    await Movie.create(movie);
    res.status(201).json({
        message: "Pelicula creada",
        movie: movie
    })
}

export const returnMovie = async (req, res) => {
    const {id} = req.params;
    const movie = await Movie.findByIdAndUpdate(id, {isAvailable: true}, );
    res.json({
        message: "Pelicula devuelta",
        movieUpdated: movie 
    })
}

export const rentMovie = async (req, res) => {
    const {id} = req.params;
    const movie = await Movie.findByIdAndUpdate(id, {isAvailable: false, $inc: {'timesRented': 1}})
    res.json({
        message: "Pelicula alquilada",
        movieUpdated: movie
    })
}

export const getTop5Movies = async (req, res) => {
    const movies = await Movie.find().sort({timesRented: -1}).limit(5);
    res.json({
        message: "Top 5 peliculas",
        top5: movies
    })
}