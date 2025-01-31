import { Suspense } from "react";
import AuthForm from "../_components/auth-form";

export default function Signup() {
  return (
    <Suspense>
      <AuthForm page="signup" />
    </Suspense>
  );
}
