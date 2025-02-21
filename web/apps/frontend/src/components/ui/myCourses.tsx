"use client";
import { useRouter } from "next/navigation";
import { CourseCard } from "@/components/ui/courseCard";

const MyCourses = ({ courses }: { courses: any[] }) => {
    const router = useRouter();

    return (
        <section className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
            {courses?.map((course) => (
                <CourseCard
                    key={course.id}
                    course={course}
                    onClick={() => {
                        router.push(`/dashboard/admin/courses/${course.id}`);
                    }}
                />
            ))}
        </section>
    );
};

export default MyCourses;