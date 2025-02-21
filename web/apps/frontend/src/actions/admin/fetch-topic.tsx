"use server";
import { prisma } from "@/lib/prisma";

const fetchTopic = async ({topicID}:{topicID : number | undefined}) : Promise<any> => {

    if(!topicID){
        return {}
    }
    
    const topic = await prisma.topic.findUnique({
        where : {
            id : topicID
        }
    })

    if(!topic){
        return {}
    }

    return topic
}

export default fetchTopic