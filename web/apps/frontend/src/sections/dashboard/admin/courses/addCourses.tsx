'use client'
import { z } from "zod"
import { zodResolver } from "@hookform/resolvers/zod"
import { cn } from "@/lib/utils";
import { IoIosAdd } from "react-icons/io";
import { useMediaQuery } from "react-responsive";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { toast } from 'react-hot-toast';
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog"
import { useForm,SubmitHandler } from "react-hook-form"
import { Session } from "next-auth";
import addCourse from "@/actions/admin/add-course";


export const AddCoursesSection = ({session,className} : {session: Session, className? : string} )=> {
    // Course Form and Functionalities
    const courseFormSchema = z.object({
      title: z.string().min(1, "Kindly enter a valid title."),
      description : z.string().min(1,"Kindly enter a valid description"),
    });
    
    type CourseFormValues = z.infer<typeof courseFormSchema>;
    
    const addCourseOnSubmitHandler: SubmitHandler<CourseFormValues> = async (data) => {
      const { title, description } = data;
      try {
        if(session.user?.id){
          const res = await addCourse({title : title,description : description,admin_id : session.user?.id})

          if (res) {
            toast.success('Content Added Successfully', { id: 'addCourse' });
            setTimeout(() => {
                window.location.reload();
              }, 1000);
            }
          }
      } catch (error : any){
        if(error.status===400){
          console.log(error)
          return toast.error(`Could not add the content : ${error.response.data.message} `, { id: 'addCourse' });
        }
      }
    };
    
    const errorHandler = (errors: any) => {
      let errorsArray: string[] = [];
      Object.keys(errors).forEach((field) => {
        errorsArray.push(errors[field]?.message || "Invalid input");
      });
    
      if (errorsArray.length > 0) {
        toast.error(errorsArray[0]); 
      }
    };

    
    const courseForm = useForm<z.infer<typeof courseFormSchema>>({
      resolver: zodResolver(courseFormSchema),
      defaultValues: {
        title: "",
        description : ""
      },
    });
    
    
    // Button Size Control
    const isSmall = useMediaQuery({maxWidth : 639})
    const isMedium = useMediaQuery({minWidth: 640, maxWidth : 1023})
    const size = isSmall ? "sm" : isMedium ? "md" : "lg"

    
    return (
      <div className={cn("flex",className)}>
        <Dialog>
            <DialogTrigger asChild>
                <Button size={size}>
                    Add Course
                </Button>
            </DialogTrigger>
            <DialogContent className="md:max-w-[600px] sm:max-w-[425px] max-w-[325px] rounded-xl">
              <form onSubmit={courseForm.handleSubmit(addCourseOnSubmitHandler,errorHandler)}>
                <DialogHeader>
                  <DialogTitle>Add Course</DialogTitle>
                  <DialogDescription>
                    Go ahead and create a new course for your students!!
                  </DialogDescription>
                </DialogHeader>
                <div className="grid gap-4 py-4">
                  {/* Title */}
                  <div className="grid grid-cols-4 items-center gap-2">
                    <Label htmlFor="title" className="text-left">
                      Title
                    </Label>
                    <Input id="title" {...courseForm.register("title")} className="col-span-3" />
                  </div>

                  {/* Description */}
                  <div className="grid grid-cols-4 items-center gap-2">
                    <Label 
                      htmlFor="description" 
                      className="text-left"
                      style={{
                        maxWidth: `calc(100%)`, 
                        wordBreak: 'break-word', 
                    }}
                    >
                      Description
                    </Label>
                    <Input id="description" {...courseForm.register("description")} className="col-span-3" />
                  </div>
                </div>
                {/* Footer */}
                <DialogFooter>
                  <Button size="lg" type="submit"> Add Course</Button>
                </DialogFooter>
              </form>
              </DialogContent>
        </Dialog>
      </div>
        
    )
}

export default {AddCoursesSection}