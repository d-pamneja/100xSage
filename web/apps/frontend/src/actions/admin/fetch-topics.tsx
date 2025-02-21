"use server";
import { prisma } from "@/lib/prisma";

export const fetchTopics = async ({courseID}:{courseID : number | undefined}) => {

    if(!courseID){
        return []
    }
    
    const topics = await prisma.topic.findMany({
        where : {
          course_id : courseID
        }
    })

    return topics
}

export default fetchTopics
