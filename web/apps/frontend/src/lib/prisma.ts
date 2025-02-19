import { prisma, Prisma } from "@web/db";
import dotenv from "dotenv";

dotenv.config({ path: require("path").resolve(__dirname, "../.env") });

export { prisma, Prisma };