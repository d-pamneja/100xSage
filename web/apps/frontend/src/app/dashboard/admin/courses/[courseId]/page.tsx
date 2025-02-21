import fetchCourse from "@/actions/admin/fetch-course";
import { auth } from "@/lib/auth";
import { AddTopicsSection } from "@/sections/dashboard/admin/topics/addTopics";
import { Topics } from "@/sections/dashboard/admin/topics/topics";

const page = async (props: { params: Promise<{ courseId: string }> }) => {
    const params = await props.params;
    const session = await auth();

    if (!session) {
        return <div>Not authenticated</div>;
    }


    const course = await fetchCourse({ courseID: parseInt(params?.courseId, 10) })
    if(!course){
        return <div>Course not found</div>
    }

    return (
        <div>
            <br /><br />
            <div className='flex flex-col justify-between w-full'>
                <h1 className='text-5xl font-bold mx-4'>{course.title}</h1>
                <h2 className='text-3xl font-semibold mx-4'>{course.description}</h2>
                <AddTopicsSection courseID={parseInt(params?.courseId, 10)} className="lg:justify-end justify-center lg:my-0 my-[20px]"/>
            </div>
            <br /><br />
            <Topics courseID={parseInt(params?.courseId, 10)} />
        </div>
    );
};

export default page;