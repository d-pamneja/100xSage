"use server";

import { prisma } from "@/lib/prisma";
import bcrypt from "bcrypt";
export const loginUser = async ({
  username,
  password,
}: {
  username: string;
  password: string;
}) => {
  const user = await prisma.user.findUnique({
    where: {
      username,
    },
  });

  if (!user) {
    return {
      status: 404,
      data: {
        message: "User not found",
      },
    };
  }
  const passwordsMatch = await bcrypt.compare(password, user.password);
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const { password: _, ...safeUser } = user;
  if (passwordsMatch) {
    return {
      status: 200,
      data: {
        user: safeUser,
      },
    };
  } else {
    return {
      status: 401,
      data: {
        message: "Invalid  username or password",
      },
    };
  }
};
