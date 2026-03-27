import multer from 'multer';
import { extname, join } from 'node:path';

const __dirname = import.meta.dirname

const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        const uploadPath = join(__dirname, '../../storage');
        cb(null, uploadPath);
    },
    filename: (req, file, cb) => {
        const uniqueSuffix = `${Date.now()}-${Math.round(Math.random() * 1E9)}`;
        const ext = extname(file.originalname).toLowerCase();
    }
})

const fileFilter = (req, file, cb) => {
    const allowedMimes = [
        'image/jpeg',
        'image/png',
        'image/gif',
        'image/webp',
        'audio/mpeg',
        'audio/wav',
        'application/pdf'
    ];

    if (allowedMimes.includes(file.mimetype)) {
        cb(null, true);
    } else {
        cb(new Error('Tipo de archivo no permitido'), false);
    }
};

export const upload = multer({ dest: 'fotos/' });