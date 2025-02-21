import fetchTopic from "@/actions/admin/fetch-topic";
import { auth } from "@/lib/auth";
import { Types } from "@/sections/dashboard/admin/topics/types/types";

const page = async (props: { params: Promise<{ courseId : string, topicId: string }> }) => {
    const params = await props.params;
    const session = await auth();

    if (!session) {
        return <div>Not authenticated</div>;
    }

    const topic = await fetchTopic({ topicID: parseInt(params?.topicId, 10) })
    if(!topic){
        return <div>Topic not found</div>
    }

    return (
        <div>
            <br /><br />
            <div className='flex flex-col justify-between w-full'>
                <h1 className='text-5xl font-bold mx-4'>{topic.title}</h1>
                <h2 className='text-3xl font-semibold mx-4'>{topic.description}</h2>
                {/* <AddTopicsSection courseID={parseInt(params?.courseId, 10)} className="lg:justify-end justify-center lg:my-0 my-[20px]"/> */}
            </div>
            <br /><br />
            <Types courseID={parseInt(params?.courseId, 10)} topicID={parseInt(params?.topicId, 10)}/>
        </div>
    );
};

export default page;