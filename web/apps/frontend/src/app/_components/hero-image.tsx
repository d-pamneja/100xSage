"use client";
import { motion } from "motion/react";
import Image from "next/image";

const HeroImage = () => {
  return (
    <motion.div
      className="relative mt-20 aspect-video w-full"
      initial={{ opacity: 0, y: -50, x: 60 }}
      animate={{ opacity: 0.5, y: 0, x: 0 }}
      transition={{ duration: 1.5, delay: 1 }}
    >
      <Image
        className="absolute"
        src={"/hero.webp"}
        alt="hero image"
        layout="fill"
        style={{ objectFit: "contain" }}
      />
    </motion.div>
  );
};

export default HeroImage;
