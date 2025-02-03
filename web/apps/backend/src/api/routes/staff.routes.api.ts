import { Router } from "express";
import { getObject, removeObject, send_DELETE_SQS, send_POST_SQS, setObject } from "../controllers/staff.controllers.api";

export const staffRouter = Router()

// S3 CRUDs
staffRouter.get('/viewContent',getObject)
staffRouter.post("/createContent",setObject)
staffRouter.delete("deleteContent",removeObject)

// SQS CRUDs
staffRouter.post('/sendPOSTSQS',send_POST_SQS)
staffRouter.delete('/sendDELETESQS',send_DELETE_SQS)

export default {staffRouter}