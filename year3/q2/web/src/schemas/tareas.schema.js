import { z } from "zod";

export const getAllToDoSchema = z.object({
    query: z.object({
        completed: z.string().regex(/^(true|false)$/, 'completed debe ser true o false').optional(),
        priority: z.enum(["low", "medium", "high"]).optional()
    })
})

export const getIDToDoSchema = z.object({
    params: z.object({
        id: z.string().regex(/^\d+$/, 'ID debe ser numérico')
    })
})

export const newToDoSchema = z.object({
    body: z.object({
        title: z.string()
            .min(3, "El titulo debe tener minimo 3 caracteres")
            .max(100, "El titulo puede tener maximo 100 caracteres"),
        description: z.string().optional(),
        completed: z.boolean().default(false),
        priority: z.enum(["low", "medium", "high"]).default("medium")
    })
})

export const toggleToDoSchema = z.object({
    params: z.object({
        toggle: z.string().regex(/^(true|false)$/, 'toggle debe ser true o false')
    })
})
