import { z } from 'zod';

export const newProductSchema = z.object({
    body: z.object({
        name: z.string(),
        price: z.float64().refine,
        category: z.enum(["ropa", "electronica", "hogar"])
    })
})