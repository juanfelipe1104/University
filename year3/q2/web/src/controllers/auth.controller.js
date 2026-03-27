import User from '../models/user.model.js'
import { encrypt } from '../middleware/handlePassword.js';
import { tokenSign } from '../middleware/handleJWT.js';

const checkEmailDuplicated = async (email) => {
    const user = await User.findOne({ email: email });
    if (user) {
        return true
    }
    return false
}

export const registerUser = async (req, res) => {
    const newUser = req.body;
    if (await checkEmailDuplicated(newUser.email)) {
        return res.status(409).json({ message: "Usuario duplicado", user: newUser });
    }
    newUser.password = await encrypt(newUser.password);
    const createdUser = await User.create(newUser);
    const token = tokenSign(createdUser);
    res.status(201).json({ message: "Usuario creado", user: createdUser, token: token })
}

export const loginUser = (req, res) => {
    const { token } = req;
    res.json({
        message: "Usuario logueado",
        token: token
    });
}

export const getUser = (req, res) => {
    const { user } = req;
    res.json({
        message: "Usuario autenticado",
        user: user
    })
}

export const updateUser = async (req, res) => {
    const { name, age } = req.params;
    const { user } = req;
    const userUpdated = await User.updateOne({ _id: user._id }, { name: name, age: age });
    res.status(201).json({
        message: "Usuario actualizado",
        user: userUpdated
    })
}