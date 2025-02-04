import { auth } from "@/lib/auth";
const page = async () => {
  const session = await auth();
  if (!session) {
    return <div>Not authenticated</div>;
  }
  return <div>Dashbaord {JSON.stringify(session)}</div>;
};

export default page;
