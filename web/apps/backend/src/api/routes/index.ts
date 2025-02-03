import { Router,Request,Response } from "express";
import { adminRouter } from "./admin.routes.api";
import { staffRouter } from "./staff.routes.api";


export const appRouter = Router()

appRouter.get("/",(req : Request, res : Response)=>{
    res.send("100xSage backend is live!!")
})

appRouter.use('/admin',adminRouter)
appRouter.use('/staff',staffRouter)

export default appRouter