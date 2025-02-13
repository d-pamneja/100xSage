import { Router } from "express";
import { getTopics } from "../controllers/topics.controllers";

export const topicRouter = Router()

topicRouter.get('/getTopics',getTopics)

export default {topicRouter}