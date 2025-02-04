import NextAuth from "next-auth";
import { NextResponse } from "next/server";
import { getToken } from "next-auth/jwt";
import authConfig, { CustomUser } from "@/auth.config";

export default NextAuth(authConfig).auth(async (req) => {
  const { nextUrl } = req;
  const isLoggedIn = !!req.auth;

  const user = req.auth?.user as CustomUser | undefined;
  const role = user?.role;

  const isStaff = role?.toLowerCase() === "staff";

  const isPublicRoute = ["/"].includes(nextUrl.pathname);
  const isAuthRoute = ["/login", "/signup"].includes(nextUrl.pathname);

  if (req.nextUrl.pathname.startsWith("/api/auth")) {
    return NextResponse.next();
  } else if (nextUrl.pathname.startsWith("/api")) {
    const secret = process.env.AUTH_SECRET;
    const token = await getToken({ req, secret });
    const res = NextResponse.next();

    if (token) {
      res.headers.set("x-user-id", token.sub || "");
    }

    return res;
  }

  if (isAuthRoute) {
    if (isLoggedIn) {
      if (!role) {
        return Response.redirect(new URL("/login", nextUrl));
      }
      if (isStaff) {
        return Response.redirect(new URL("/staff/dashboard", nextUrl));
      }
      return Response.redirect(new URL("/admin/dashboard", nextUrl));
    }
    return undefined;
  }

  if (!isLoggedIn && !isPublicRoute) {
    return Response.redirect(
      nextUrl.origin + "/login?callbackUrl=" + nextUrl.href,
    );
  }

  if (isLoggedIn && nextUrl.pathname === "/") {
    if (isStaff) {
      return Response.redirect(new URL("/staff/dashboard", nextUrl));
    }
    return Response.redirect(nextUrl.origin + "/admin/dashboard");
  }
  if (isLoggedIn && isStaff && nextUrl.pathname.startsWith("/admin")) {
    return Response.redirect(nextUrl.origin + "/staff/dashboard");
  }
  if (isLoggedIn && !isStaff && nextUrl.pathname.startsWith("/staff")) {
    return Response.redirect(nextUrl.origin + "/admin/dashboard");
  }

  return undefined;
});

export const config = {
  matcher: [
    "/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)",
    "/api/:path*",
  ],
};
