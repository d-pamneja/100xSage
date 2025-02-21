import fetchTopics from "@/actions/admin/fetch-topics";
import MyTopics from "@/components/ui/myTopics";

export const Topics = async ({ courseID }: { courseID: number }) => {
    const topics = await fetchTopics({ courseID: courseID });

    return <MyTopics courseID={courseID} topics={topics} />;
};