"use client";

import LoginForm from "./login-form";
import NavTab from "./nav-tab";

import SignupForm from "./signup-form";

const AuthForm = ({ page }: { page: string }) => {
  return (
    <div className="flex w-full flex-col items-center justify-center overflow-auto rounded-2xl bg-white px-[20px] py-[40px]">
      <div className="m-auto flex w-[380px] flex-col gap-5 overflow-auto">
        <NavTab page={page} />
        {page == "login" ? <LoginForm /> : <SignupForm />}
      </div>
    </div>
  );
};

export default AuthForm;
