"use client";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { motion } from "motion/react";
const HeroSection = () => {
  return (
    <motion.div
      className="text-start"
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 2 }}
    >
      <h1 className="text-5xl font-bold">Supercharge Your TAs with AI</h1>
      <p className="mt-4 w-[600px] text-lg text-gray-300">
        Instant responses, automated FAQs, and deep learning
        insights—effortlessly enhance student support.
      </p>
      <div className="mt-6 flex justify-start gap-4">
        <Link href={"/signup"}>
          <Button className="bg-white">Get Started</Button>
        </Link>
        <Link href={"/login"}>
          <Button variant="outline" className="border-gray-300 text-gray-300">
            Login
          </Button>
        </Link>
      </div>
    </motion.div>
  );
};

export default HeroSection;
