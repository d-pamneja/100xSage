"use server";
import { prisma } from "@/lib/prisma";

export const addCourse = async ({title,description,admin_id}:{title : string ,description : string, admin_id : string}) => {
    
    const addedCourse = await prisma.course.create({
        data : {
            title : title,
            description : description,
            admin_id : admin_id
        }
    })

    return addedCourse
}

export default addCourse

