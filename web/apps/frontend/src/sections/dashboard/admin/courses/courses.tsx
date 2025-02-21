import fetchCourses from "@/actions/admin/fetch-courses";
import { Session } from "next-auth";
import MyCourses from "@/components/ui/myCourses";

export const Courses = async ({ session }: { session: Session }) => {
    const courses = await fetchCourses({ adminID: session.user?.id });

    return <MyCourses courses={courses} />;
};