"use server";
import { prisma } from "@/lib/prisma";
import bcrypt from 'bcryptjs';

export async function signUpUser({
  username,
  password,
}: {
  username: string;
  password: string;
}) {
  try {
    const hashedPassword = await bcrypt.hash(password, 10);

    const user = await prisma.user.create({
      data: {
        username,
        password: hashedPassword,
        role: "ADMIN",
        admin_id: ""
      },
    });

    if (user.role === "ADMIN") {
      await prisma.$transaction([
        prisma.user.update({
          where: { id: user.id },
          data: { admin_id: user.id },
        }),
        prisma.admin.create({
          data: {
            id: user.id,
          },
        }),
      ]);      
    }



    return { status: 200, user };
  } catch (error: any) {
    if (error.code === "P2002") {
      return { status: 409, error: "Username already taken.",details : error.message };
    }
    return { status: 500, error: "Internal server error",details : error.message };
  }
}
