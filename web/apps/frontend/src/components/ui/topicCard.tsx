'use client';
import { Card, CardContent } from "@/components/ui/card";

export const TopicCard = ({
  topic,
  onClick,
}: {
  topic: any;
  onClick?: () => void;
}) => {

  return (
    <Card className="w-full max-w-sm overflow-hidden transition-all hover:shadow-lg cursor-pointer" onClick={onClick}>
      <CardContent className="p-4">
        <h3 className="text-lg font-semibold text-primary mb-2 line-clamp-2">
          {topic.title}
        </h3>
        <p>{topic.description}</p>
      </CardContent>
    </Card>
  );
};