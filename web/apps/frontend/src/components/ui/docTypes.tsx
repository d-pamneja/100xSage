"use client";
import { useRouter } from "next/navigation";
import { TypeCard } from "@/components/ui/typeCard";

const MyTypes = ({ courseID,topicID,types }: { courseID : number, topicID : number, types: any[] }) => {
    const router = useRouter();

    return (
        <section className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
            {types?.map((type) => (
                <TypeCard
                    key={type.id}
                    type={type}
                    onClick={() => {
                        router.push(`/dashboard/admin/courses/${courseID}/topics/${topicID}/types/${type.id}`);
                    }}
                />
            ))}
        </section>
    );
};

export default MyTypes;