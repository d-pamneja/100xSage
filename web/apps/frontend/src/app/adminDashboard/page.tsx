import { Button } from "@/components/ui/button";
import { auth } from "@/lib/auth";
import { MyCourses } from "@/sections/adminDashboard/courses";
import logout from "./logout";
import { ButtonDiv } from "@/sections/adminDashboard/buttonsDiv";

const page = async () => {
  const session = await auth();

  if (!session) {
    return <div>Not authenticated</div>;
  }


  return (
    <div>
      Dashbaord {JSON.stringify(session)}{" "}
      <br></br><br></br>
      <div className='flex lg:flex-row flex-col lg:justify-between w-full'>
        <h1 className='text-5xl font-bold mx-4'>Workspace</h1>
        <ButtonDiv session={session} className="lg:justify-end justify-center lg:my-0 my-[20px]"/>
      </div>
      <MyCourses session={session}/>
      <br></br><br></br>
      <Button onClick={logout}>Log Out</Button>
    </div>
  );
};

export default page;
