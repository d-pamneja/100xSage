'use client';
import { Card, CardContent } from "@/components/ui/card";

export const CourseCard = ({
  course,
  onClick,
}: {
  course: any;
  onClick?: () => void;
}) => {

  return (
    <Card className="w-full max-w-sm overflow-hidden transition-all hover:shadow-lg cursor-pointer" onClick={onClick}>
      <CardContent className="p-4">
        <h3 className="text-lg font-semibold text-primary mb-2 line-clamp-2">
          {course.title}
        </h3>
        <p>{course.description}</p>
      </CardContent>
    </Card>
  );
};