"use client";
import robotImg from '../../../public/assets/robot.jpg'
import { LoaderCircle } from 'lucide-react';
import Image from 'next/image';
import { motion } from "motion/react";
import { Button } from '@/components/ui/button';

export const Hero = () => {
    return (
        <motion.section 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 2 }}
        >
            <div className="container px-4 py-12"> 
                <div className="py-24 rounded-lg shadow-lg text-center">
                        <h1 className="text-4xl font-bold text-gray-100 text-center leading-tight">
                            🚀 AI-Powered Support, Smarter & Faster by Sage
                        </h1>
                        <p className="text-center text-lg mt-6">
                            Transform the way you handle queries with our intelligent AI bot. 
                            From retrieving past solutions to RAG-powered responses and automated ticketing, 
                            our system ensures seamless support for every user. Let AI take charge, so you can focus on what truly matters.
                        </p>

                        <div className='flex justify-center mt-4'>
                            <Button>
                                Start Now
                            </Button>
                        </div>
    
                        <div className="relative mt-16 rounded-2xl overflow-hidden border-gradient">
                            <div className="relative">
                                <Image 
                                    src={robotImg} 
                                    alt="Robot Image" 
                                    className="block w-full rounded-2xl" 
                                    width={1400} 
                                />
                            </div>
                        </div>
                </div>
            </div>
        </motion.section>
    )
}

export default Hero