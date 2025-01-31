"use client";

import { motion } from "motion/react";

const Title = () => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 2 }}
    >
      <h1 className="my-20 text-start text-7xl font-medium underline">
        100xSage
      </h1>
    </motion.div>
  );
};

export default Title;
