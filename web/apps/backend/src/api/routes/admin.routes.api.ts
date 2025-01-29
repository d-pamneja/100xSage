import { Router } from "express";
import { getObject, removeObject, send_DELETE_SQS, send_POST_SQS, setObject } from "../controllers/admin.controllers.api";

export const adminRouter = Router()

// S3 CRUDs
adminRouter.get('/viewContent',getObject)
adminRouter.post("/createContent",setObject)
adminRouter.delete("deleteContent",removeObject)

// SQS CRUDs
adminRouter.post('/sendPOSTSQS',send_POST_SQS)
adminRouter.delete('/sendDELETESQS',send_DELETE_SQS)

export default {adminRouter}

