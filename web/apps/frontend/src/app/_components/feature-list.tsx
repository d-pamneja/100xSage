"use client";
import { CheckCircle } from "lucide-react";
import { motion } from "motion/react";

const FeatureList = () => {
  return (
    <motion.div
      className="mt-16 flex flex-col gap-4 text-start"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 1 }}
    >
      <h2 className="text-3xl font-semibold">Made for Modern Cohorts</h2>
      <ul className="mt-4 flex flex-col gap-2 space-y-2 text-gray-400">
        <li className="flex gap-2">
          <CheckCircle /> Students do not need to wait for TAs
        </li>
        <li className="flex gap-2">
          <CheckCircle /> AI answers directly in chat
        </li>
        <li className="flex gap-2">
          <CheckCircle /> Track trends & performance in real-time
        </li>
        <li className="flex gap-2">
          <CheckCircle />
          Identify top contributors and performers
        </li>
      </ul>
    </motion.div>
  );
};

export default FeatureList;
