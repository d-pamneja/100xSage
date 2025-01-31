import NextAuth from "next-auth";
import Credentials from "next-auth/providers/credentials";

import authConfig from "@/auth.config";
import { LoginSchema } from "@/schemas/login-schema";
import { loginUser } from "@/actions/auth/login-user";

export const { handlers, signIn, signOut, auth } = NextAuth({
  ...authConfig,
  secret: process.env.AUTH_SECRET!,
  session: {
    strategy: "jwt",
  },
  pages: {
    signIn: "/login",
  },
  providers: [
    Credentials({
      credentials: {
        username: {},
        password: {},
      },
      authorize: async (credentials) => {
        const { username, password } = credentials;
        const validatedFields = LoginSchema.safeParse({ username, password });

        if (validatedFields.success) {
          const { username, password } = validatedFields.data;

          const response = await loginUser({ username, password });

          if (response.status != 200) {
            return null;
          } else {
            const { user } = response.data;
            if (user) {
              return user;
            }
            return null;
          }
        }
        return null;
      },
    }),
  ],
});
