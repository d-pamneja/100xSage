"use server";
import { prisma } from "@/lib/prisma";
import bcrypt from "bcrypt";

export async function signUpUser({
  username,
  password,
}: {
  username: string;
  password: string;
}) {
  try {
    await prisma.user.create({
      data: {
        username,
        password: await bcrypt.hash(password, 10),
        role: "ADMIN",
      },
    });
    return {
      status: 200,
    };
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
  } catch (error: any) {
    if (error.name === "PrismaClientKnownRequestError") {
      if (error.code == "P2002") {
        console.log("Error code P2002: Unique constraint violation");
        return { status: 409, error: "Username already taken." };
      }
    }
    return { status: 500, error: "Failed to sign up " };
  }
}
