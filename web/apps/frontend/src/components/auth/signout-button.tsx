"use client";
import { signOut } from "next-auth/react";
import { Button } from "../ui/button";
const SignoutButton = () => {
  async function logout() {
    signOut();
  }
  return <Button onClick={logout}>Log Out</Button>;
};

export default SignoutButton;
