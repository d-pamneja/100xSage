"use server";
import { prisma } from "@/lib/prisma";

export const fetchCourses = async ({adminID}:{adminID : string | undefined}) => {

    if(!adminID){
        return []
    }
    
    const courses = await prisma.course.findMany({
        where : {
          admin_id : adminID
        }
    })

    return courses
}

export default fetchCourses
