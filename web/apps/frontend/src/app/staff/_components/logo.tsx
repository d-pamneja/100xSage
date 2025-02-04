import { cn } from "@/lib/utils";
import { Poppins } from "next/font/google";

const font = Poppins({
  subsets: ["latin"],
  weight: ["600"],
});
const Logo = () => {
  return (
    <div className="flex space-x-2">
      <div
        className={cn(
          "m-y-auto flex items-center text-3xl font-bold text-white",
          font.className,
        )}
      >
        100xSage
      </div>
    </div>
  );
};

export default Logo;
