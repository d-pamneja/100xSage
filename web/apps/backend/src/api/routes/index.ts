import { Router,Request,Response } from "express";
import { adminRouter } from "./admin.routes.api";
import { staffRouter } from "./staff.routes.api";
import { topicRouter } from "./topics.routes.api";


export const appRouter = Router()

appRouter.get("/",(req : Request, res : Response)=>{
    res.send("100xSage backend is live!!")
})

appRouter.use('/admin',adminRouter)
appRouter.use('/staff',staffRouter)
appRouter.use('/topic',topicRouter)

export default appRouter