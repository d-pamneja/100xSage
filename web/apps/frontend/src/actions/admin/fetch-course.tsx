"use server";
import { prisma } from "@/lib/prisma";

const fetchCourse = async ({courseID}:{courseID : number | undefined}) : Promise<any> => {

    if(!courseID){
        return {}
    }
    
    const course = await prisma.course.findUnique({
        where : {
            id : courseID
        }
    })

    if(!course){
        return {}
    }

    return course
}

export default fetchCourse
