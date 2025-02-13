import { Request,Response,NextFunction } from "express";
import { prisma } from "../../lib/prisma";

import dotenv from 'dotenv'; 
dotenv.config()

export const getTopics = async (req : Request, res : Response, next : NextFunction) : Promise<any> => {
    try{
        const courseID = req.body.courseID

        const response = prisma.topic.findMany({
            where : {
                course_id : courseID
            }
        })

        if(!response){
            return res.status(404).json({message : "Could not fetch the topics"})
        }

        return res.status(200).json({message : "All topics for the given course fetched successfully",response})
    }
    catch (error : any){
        return res.status(500).json({message : "Internal Server Error",error})
    }
}

export default {getTopics}