import { PrismaClient } from "@prisma/client";
import env from "./env.js";

const NODE_ENV = env.NODE_ENV;

const prisma = new PrismaClient({
    log: NODE_ENV === 'development' ? ['query', 'info', 'warn', 'error'] : ['error']
}).$extends({
    query: {
        $allModels : {
            $allOperations: async ({operation, model, args, query}) => {
                const before = Date.now();
                const result = await query(args);
                const after = Date.now();
                console.log(`Query ${model}.${operation} took ${after - before}ms`);
            }
        }
    }
});

export default prisma;