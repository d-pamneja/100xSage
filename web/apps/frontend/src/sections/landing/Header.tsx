"use client";
import { motion } from "motion/react";
import Title from "@/app/_components/header/title";
import Logo from "@/app/_components/header/logo";
import Buttons from "@/app/_components/header/buttons";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { useMediaQuery } from "react-responsive";

export const HomePageNavItems = [
    {
        name : "FEATURES",
        href : "#features-section"
    },
    {
        name : "PRICING",
        href : "#pricing-section"
    },
    {
        name : "TESTIMONIALS",
        href : "#testimonials-section"
    }
]

export const Header = () => {
    const [isMobileNavOpen,setMobileNavOpen] = useState(false);

    const isSmall = useMediaQuery({maxWidth : 639})
    const isMedium = useMediaQuery({minWidth: 640, maxWidth : 1023})
    const size = isSmall ? "sm" : isMedium ? "md" : "lg"

    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 2 }}
        >
        
            <header className="flex justify-between items-center md:px-4 px-2 md:py-2 py-1 bg-black text-white w-full z-40 border-b-2">
                <div id="logo-section" className="flex md:gap-2 gap-1 items-center">
                    <Logo />
                    <Title />
                </div>

                {size == 'lg' && (
                        <nav id="navigation-section" className="flex items-center justify-center flex-1 space-x-8">
                        {HomePageNavItems.map(({ name, href }) => (
                            <a key={href} href={href} className="font-bold px-3">
                                {name}
                            </a>
                        ))}
                    </nav>
                )}

                {size != 'lg' && (
                    <div id="flex-grow" className="flex-grow mx-auto">
                    </div>
                )}

                <div id="buttons-section" className="flex mx-4">
                    <Buttons isMobileNavOpen={isMobileNavOpen} setMobileNavOpen={setMobileNavOpen}/>
                </div>
            </header>

            {isMobileNavOpen && (
                <div className="container">
                    <nav className="flex flex-col items-center gap-4 py-8 my-4">
                        {HomePageNavItems.map(({ name, href }) => (
                            <a key={href} href={href}>
                                {name}
                            </a>
                        ))}

                        <div id="buttons-section" className="flex gap-4 mx-4">
                            <Button variant={"gradient"}>
                                LOGIN
                            </Button>
                            <Button>
                                SIGN UP
                            </Button>
                        </div>
                    </nav>    
                </div>
            )}
        </motion.div>
    );
};

export default Header