'use client'
import { useRouter } from 'next/navigation';
import { CourseCard } from "@/components/ui/courseCard";
import { Session } from "next-auth";
import fetchCourses from "@/actions/admin/fetch-courses";


export const MyCourses = async ({
    session
}: {
    session: Session
}) => {
    const router = useRouter();
    const courses = await fetchCourses({ adminID: session.user?.id })

    return (
        <section className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
            {courses?.map((course) => (
            <CourseCard
                key={course.id}
                course={course}
                onClick={()=>{
                    router.push(`/courses/${course.id}`);
                }}
            />
            ))}
        </section>
    )
}