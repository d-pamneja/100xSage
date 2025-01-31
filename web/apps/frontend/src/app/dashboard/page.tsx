import { Button } from "@/components/ui/button";
import { auth } from "@/lib/auth";
import logout from "./logout";
const page = async () => {
  const session = await auth();
  if (!session) {
    return <div>Not authenticated</div>;
  }
  return (
    <div>
      Dashbaord {JSON.stringify(session)}{" "}
      <Button onClick={logout}>Log Out</Button>
    </div>
  );
};

export default page;
