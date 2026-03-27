import User from "../models/user.model.js";

export const getAllUsers = async (req, res) => {
    const users = await User.find();
    res.json(users); 
}

export const addUser = async (req, res) => {
    const user = req.body;
    await User.create(user);
    res.status(201).json({
        message: 'Usuario creado',
        user: user
    })
} 