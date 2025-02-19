import { Button } from "@/components/ui/button";
import { Dispatch, SetStateAction } from "react";
import Link from "next/link";
import { twMerge } from "tailwind-merge";


export const Buttons = ({isMobileNavOpen,setMobileNavOpen} : {isMobileNavOpen : boolean ,setMobileNavOpen :  Dispatch<SetStateAction<boolean>>}) => {
    return (
       <>
            <div id="buttons" className="hidden lg:flex gap-4 mx-4">
                <Link href='/login'>
                    <Button variant={"gradient"}>
                        LOGIN
                    </Button>
                </Link>
                <Link href='/signup'>
                    <Button>
                        SIGN UP
                    </Button>
                </Link>
            </div>
            <div id="hamburger-menu" className="lg:hidden my-4">
                <button className="size-10 rounded-lg border-2 border-transparent 
                    [background:linear-gradient(black,black)_content-box,conic-gradient(from_45deg,var(--color-violet-400),var(--color-fuchsia-400))_border-box] relative"
                    onClick={()=> setMobileNavOpen((curr : boolean) => !curr)}
                >
                    <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">
                        <div className={twMerge("w-4 h-0.5 bg-gray-100 -translate-y-1", isMobileNavOpen && 'translate-y-0 rotate-45 transition duration-500' )}>
                        </div>
                    </div>
                    <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">
                        <div className={twMerge("w-4 h-0.5 bg-gray-100 translate-y-1", isMobileNavOpen && 'translate-y-0 -rotate-45 transition duration-500' )}>
                        </div>
                    </div>
                </button>
            </div>
            
       </>
    )
}

export default Buttons;