"use client";
import { useRouter } from "next/navigation";
import { TopicCard } from "@/components/ui/topicCard";

const MyTopics = ({ courseID,topics }: { courseID : number, topics: any[] }) => {
    const router = useRouter();

    return (
        <section className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
            {topics?.map((topic) => (
                <TopicCard
                    key={topic.id}
                    topic={topic}
                    onClick={() => {
                        router.push(`/dashboard/admin/courses/${courseID}/topics/${topic.id}`);
                    }}
                />
            ))}
        </section>
    );
};

export default MyTopics;