"use server";
import { prisma } from "@/lib/prisma";

export const addTopic = async ({title,description,courseID}:{title : string ,description : string, courseID : number}) => {
    
    const addedTopic = await prisma.topic.create({
        data : {
            title : title,
            description : description,
            course_id : courseID
        }
    })

    return addedTopic
}

export default addTopic