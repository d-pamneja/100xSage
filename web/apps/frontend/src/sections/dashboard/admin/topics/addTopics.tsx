'use client'
import { z } from "zod"
import { zodResolver } from "@hookform/resolvers/zod"
import { cn } from "@/lib/utils";
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
import addTopic from "@/actions/admin/add-topic";


export const AddTopicsSection = ({courseID,className} : {courseID : number ,className? : string} )=> {
    // Course Form and Functionalities
    const topicFormSchema = z.object({
      title: z.string().min(1, "Kindly enter a valid title."),
      description : z.string().min(1,"Kindly enter a valid description"),
    });
    
    type TopicFormValues = z.infer<typeof topicFormSchema>;
    
    const addTopicOnSubmitHandler: SubmitHandler<TopicFormValues> = async (data) => {
      const { title, description } = data;
      try {
        const res = await addTopic({title : title,description : description,courseID : courseID})

        if (res) {
        toast.success('Content Added Successfully', { id: 'addTopic' });
        setTimeout(() => {
            window.location.reload();
            }, 1000);
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

    
    const topicForm = useForm<z.infer<typeof topicFormSchema>>({
      resolver: zodResolver(topicFormSchema),
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
                    Add Topic
                </Button>
            </DialogTrigger>
            <DialogContent className="md:max-w-[600px] sm:max-w-[425px] max-w-[325px] rounded-xl">
              <form onSubmit={topicForm.handleSubmit(addTopicOnSubmitHandler,errorHandler)}>
                <DialogHeader>
                  <DialogTitle>Add Topic</DialogTitle>
                  <DialogDescription>
                    Go ahead and add a new topic in your course!!
                  </DialogDescription>
                </DialogHeader>
                <div className="grid gap-4 py-4">
                  {/* Title */}
                  <div className="grid grid-cols-4 items-center gap-2">
                    <Label htmlFor="title" className="text-left">
                      Title
                    </Label>
                    <Input id="title" {...topicForm.register("title")} className="col-span-3" />
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
                    <Input id="description" {...topicForm.register("description")} className="col-span-3" />
                  </div>
                </div>
                {/* Footer */}
                <DialogFooter>
                  <Button size="lg" type="submit"> Add Topic</Button>
                </DialogFooter>
              </form>
              </DialogContent>
        </Dialog>
      </div>
        
    )
}

export default {AddTopicsSection}